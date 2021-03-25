# from src.log_cfg import logger

import numpy as np
import geopandas as gpd
from rasterio.features import bounds as featurebounds
from rio_tiler.io import STACReader, COGReader
from rio_tiler.mosaic import mosaic_reader
from rio_tiler.models import ImageData
from datetime import date
from satsearch import Search
from satstac import Item
import csv
import os
import sys

ELEMENT84_URL = "https://earth-search.aws.element84.com/v0/search/"
SENTINEL_L2A_COLLECTION = 'sentinel-s2-l2a-cogs'
CDL_PATH = "CDL_2019/CDL_2019_clip_20201217154034_1060751160.tif"

"""For CLI command control, it could be field level or county level """
#TODO: need to determine what parameters needed(county? state? shapefile? crop tpye?)
if len(sys.argv) > 4:
    print('You have specified too many arguments, please specify the shapefile path, CDL path and the date range for data(mm/dd/yyyy-mm/dd/yyyy) ')
    sys.exit()
if len(sys.argv) < 4:
    print('You need to specify the shapefile path, CDL path and the date range for data(mm/dd/yyyy-mm/dd/yyyy)')
    sys.exit()

shape_file_path = sys.argv[1]
CDL_PATH = sys.argv[2]
date_range = sys.argv[3]
# print("shape file path is: " + shape_file_path)
# print("CDL path is: " + CDL_PATH)
# print("date range to query the data is: " + date_range)


def main(shapefile, datetime: date) -> object:
    county_shapefile = gpd.read_file(shapefile)
    county_shapefile = county_shapefile.to_crs({'init': 'epsg:4326'})
    """list to store all the ndvi and bands values"""
    data_records = []

    """variables for inquiry sentinel data"""
    start_time = ""
    end_time = ""

    """create yield county list, contains counties that has specified crop yield data"""
    yield_county_list = []
    crop_type = ""
    with open('', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                yield_county_list.append(row[0])

    data = gpd.read_file(CDL_PATH)
    counties = county_geometries(county_shapefile)

    """iterate each county in a state CDL
       add ndvi and each bands value to list if county is in the yield county list"""
    for county in counties:
        if county in yield_county_list:
            item_list = search(county, start_time, end_time)

            #this function would return the ndvi value ndarry with cdl and cloud mask applied
            ndvi_value = ndvi(county, item_list)

            record = []
            record.append(county)
            record.append(ndvi_value)

            # add band 2 - 8 (B01 - B08 covers: Blue, Green, Red, VRE1, VRE2, VRE3, NIR)
            record.append(get_band(county, item_list, "B02"))
            record.append(get_band(county, item_list, "B03"))
            record.append(get_band(county, item_list, "B04"))
            record.append(get_band(county, item_list, "B05"))
            record.append(get_band(county, item_list, "B06"))
            record.append(get_band(county, item_list, "B07"))
            record.append(get_band(county, item_list, "B08"))
            data_records.append(record)

    with open("satellite_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(record)

def search(geometry: dict, start: str, end: str) -> object:
    kwargs = {
        'bbox': geometry,
        'datetime': f"{start}/{end}",
        'collections': [SENTINEL_L2A_COLLECTION]
    }
    search = Search(url=ELEMENT84_URL, **kwargs)
    return search.items()
    

def cdl_mask(geometry: tuple, crop_type: int, height: int, width: int):
    with COGReader(CDL_PATH) as cog:
        cdl = cog.part(geometry, resampling_method="nearest", height=height, width=width)
        return np.ma.where((cdl.data == crop_type), 1, 0)
    
    
def cloud_mask(asset_url: str, geometry: tuple, height: float, width: float):
    with STACReader(asset_url) as stac:
        scl_band, _ = stac.part(
            geometry,
            resampling_method="nearest",
            height=height,
            width=width,
            assets="SCL",
            max_size=None
        )
    # 0 - 4 are shadows, while pixels greater than 6 are cloud probable.
    cloud_mask = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)
    return cloud_mask
    
        
def ndvi(geometry: tuple, scenes: ItemCollection) -> ImageData:
    sceneid = [scene.id for scene in scenes]
    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    stac_assets = [stac_item.format(sceneid=scene) for scene in sceneid]
    
    def ndvi_tiler(asset, *args, **kwargs):
        with STACReader(asset) as stac:
            ndvi, _ = stac.part(geometry, expression="(B08-B04)/(B08+B04)")
            cloud_msk = cloud_mask(asset, geometry=geometry, height=ndvi.shape[1], width=ndvi.shape[2])
            cdl = cdl_mask(geometry, 1, ndvi.shape[1], ndvi.shape[2])
            
            # Cloud mask + CDL mask
            overlay = np.logical_and(cloud_msk, cdl)
            return ImageData(ndvi, overlay)
        
    ndvi, _ = mosaic_reader(stac_assets, ndvi_tiler)
    ndvi_masked = ndvi.as_masked()
    return ndvi_masked


def get_band(geometry: tuple, scenes: ItemCollection, bandnum: str) -> ImageData:
    sceneid = [scene.id for scene in scenes]
    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    stac_assets = [stac_item.format(sceneid=scene) for scene in sceneid]
    
    def nir_tiler(asset, *args, **kwargs):
        with STACReader(asset) as stac:
            nir, _ = stac.part(geometry, assets="B08")
            cloud_msk = cloud_mask(asset, geometry=geometry, height=ndvi.shape[1], width=ndvi.shape[2])
            cdl = cdl_mask(geometry, 1, nir.shape[1], nir.shape[2])
            
            overlay = np.logical_and(cloud_msk, cdl)
            return ImageData(nir, overlay)
        
    nir, _ = mosaic_reader(stac_assets, nir_tiler)
    nir_masked = nir.as_masked()
    return nir_masked
        
    
def process_images(geometry: tuple, start: date, end: date) -> object:
    try:
        scenes = search(geometry, start, end)
        ndvi = ndvi(geometry, scenes)
        nir = get_band(geometry, scenes, bandnum)
        
    except StopIteration:
        raise Exception("No collection found for date range.")


def county_geometries(counties_df: GeoDataFrame) -> dict:
    """ Takes a DataFrame and returns a Dict with the county name and converted tuple coordinates.

    Args:
        counties_df (GeoDataFrame): Counties GeoDataFrame from shapefile.

    Returns:
        dict: County names and tuple of geometries: {"County": "(36.5, ...) }.
    """
    counties = dict(zip(counties_df.COUNTY_NAM, counties_df.geometry))
    for key, value in counties.items():
        counties[key] = featurebounds(value)
    return counties

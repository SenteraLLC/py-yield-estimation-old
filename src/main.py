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

ELEMENT84_URL = "https://earth-search.aws.element84.com/v0/search/"
SENTINEL_L2A_COLLECTION = 'sentinel-s2-l2a-cogs'
CDL_PATH = "CDL_2019/CDL_2019_clip_20201217154034_1060751160.tif"

def main(shapefile, datetime: date) -> object:
    county_shapefile = gpd.read_file(shapefile)
    county_shapefile = county_shapefile.to_crs({'init': 'epsg:4326'})
    

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
    
    
def ndvi(geometry: tuple, scenes: ItemCollection) -> ImageData: 
    sceneid = [scene.id for scene in scenes]
    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    stac_assets = [stac_item.format(sceneid=scene) for scene in sceneid]
    
    def ndvi_tiler(asset, *args, **kwargs):
        with STACReader(asset) as stac:
            return stac.part(geometry, expression="(B08-B04)/(B08+B04)")
        
    ndvi, _ = mosaic_reader(stac_assets, ndvi_tiler)
    
    mask = cdl_mask(geometry, 1, ndvi.data.shape[1], ndvi.data.shape[2])
    ndvi_masked = ImageData(ndvi.data, mask).as_masked()
        
    return ndvi_masked        


def cloud_mask(asset_url: str, geometry: tuple, height: float, width: float):
    # TODO: STACReader or COGReader? 
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
        
        
def process_images(geometry: tuple, start: date, end: date) -> object:
    try:
        scenes = search(geometry, start, end)
        ndvi = ndvi(geometry, scenes)

    except StopIteration:
        raise Exception("No collection found for date range.")


def county_geometries(counties_df: GeoDataFrame) -> dict:
    """ Takes a DataFrame and returns a Dict with the converted tuple coordinates. 

    Args:
        counties_df (GeoDataFrame): Counties GeoDataFrame from shapefile.

    Returns:
        dict: County names and tuple of geometries: {"County": "(36.5, ...) }.
    """
    counties = dict(zip(counties_df.COUNTY_NAM, counties_df.geometry))
    for key, value in counties.items():
        counties[key] = featurebounds(value)
    return counties


# def yield_estimation(geojson):
#     scenes = fetch_stac_scenes(geojson)
#     best_scene = least_cloud_cover_date(scenes, geojson)

#     # Scene path from the AWS URL for element84 query. ex: S2B_14TQN_20200708_0_L2A
#     scene_path = urlparse(best_scene).path.split("/")[-2]

#     stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
#     stac_asset = stac_item.format(sceneid=scene_path)

#     bounds = featurebounds(geojson)

#     with STACReader(stac_asset) as cog:
#         ndvi, _ = cog.part(bounds, expression="(B08-B04)/(B08+B04)")
#         # Crop and resample scene classification band
#         scl_band, mask = cog.part(
#             bounds,
#             resampling_method="nearest",
#             height=ndvi.shape[1],
#             width=ndvi.shape[2],
#             assets="SCL",
#             max_size=None,
#         )

#     # Apply cloud mask
#     masked = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)

#     # NDVI as a MaskedArray
#     ndvi_masked = ImageData(ndvi, masked).as_masked()

#     # print("\nMax NDVI: {m}".format(m=ndvi_masked.max()))
#     # print("Mean NDVI: {m}".format(m=ndvi_masked.mean()))
#     # print("Median NDVI: {m}".format(m=np.median(ndvi_masked.data)))
#     # print("Min NDVI: {m}".format(m=ndvi_masked.min()))

#     yield_estimate = 11.359 * math.exp(3.1 * ndvi_masked.mean())

#     return yield_estimate

import intake
import pycrs
import rasterio.warp
from rasterio.mask import mask
from rasterio.io import MemoryFile

import geopandas as gpd
from src.log_cfg import logger

def getFeatures(gdf):
    """Parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def create_memory_file(data, west_bound, north_bound, cellsize, driver='GTIFF'):
    #data is a numpy array
    if data.ndim ==2: # Handle 2 or 3D input arrays
        data = np.expand_dims(data, axis=0)
    dtype = data.dtype
    shape = data.shape
    transform = rasterio.transform.from_origin(west_bound, north_bound, cellsize, cellsize)
    with MemoryFile() as memfile:
        dataset = memfile.open(
                driver=driver, width=shape[2], height = shape[1],
                transform=transform, count=shape[0], dtype=dtype)
        dataset.write(data)
        return dataset

def crop_scl_band(catalog, gjson):
    scl_band = rasterio.open(item.SCL().metadata['href'])

    gdf = gpd.GeoDataFrame.from_features(gjson['features'], crs="ESPG:4326")
    gdf = gdf.to_crs(crs=scl_band.crs.data)

    out_coords = getFeatures(gdf)

    out_img, out_transform = mask(dataset=scl_band, shapes=out_coords, crop=True)
    out_meta = scl_band.meta.copy()

    espg_code = int(scl_band.crs.data['init'][5:])

    out_meta.update({"driver": "GTiff",
                     "height": out_img.shape[1],
                     "width": out_img.shape[2],
                     "transform": out_transform,
                     "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})
    return out_img


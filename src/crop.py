import rasterio
import geopandas as gpd

from src.log_cfg import logger

from rasterio.plot import show
from rasterio.mask import mask

def crop(catalog):
    """
    return: Array of cropped tiffs?
    """
    bands = ['SCL']
    tiffs = []
    # Get band endpoints from the catalog
    for band in bands:
        tiffs.extend([catalog[item][band].metadata['href'] for item in catalog])
    
    arrs = []
    for tiff in tiffs:
        with rasterio.open(tiff) as src:
            #mask_shp = [feature['geometry'] for feature in json.loads(gdf)['features']]
            gdf = gpd.GeoDataFrame.from_features(geojson["features"],crs="EPSG:4326")
            gdf = gdf.to_crs(crs=src.crs.data)
            out_coords = json.loads(gdf.to_json())['features'][0]['geometry']
            #for index in range(len(mask_shp)):
            out_image, out_transform = rasterio.mask.mask(src, out_coords, crop=True, nodata=np.nan)

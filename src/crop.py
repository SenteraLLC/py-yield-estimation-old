import intake
import rioxarray
import xarray
import geojson
import json

from src.log_cfg import logger

def crop_scl_band(catalog, gjson):
    """
    return: xArray of cropped tiffs
    """

    # Get tiff SCL bands for date range. Yeah, I don't understand this line either. 
    tiffs = [catalog[item].SCL().metadata['href'] for item in catalog]

    out_coords = json.loads(gjson)['features'][0]['geometry']
    geometries = json.dumps(out_coords)
    cropping_geometries = [geojson.loads(geometries)]

    for band in tiffs:
        arr = rioxarray.open_rasterio(band)

    cropped = arr.rio.clip(geometries=cropping_geometries, crs=4326)
    return cropped 
    
    # for tiff in tiffs:
    #     with rasterio.open(tiff) as src:
    #         #mask_shp = [feature['geometry'] for feature in json.loads(gdf)['features']]
    #         gdf = gpd.GeoDataFrame.from_features(geojson["features"],crs="EPSG:4326")
    #         gdf = gdf.to_crs(crs=src.crs.data)
    #         out_coords = json.loads(gdf.to_json())['features'][0]['geometry']
    #         #for index in range(len(mask_shp)):
    #         out_image, out_transform = rasterio.mask.mask(src, out_coords, crop=True, nodata=np.nan)

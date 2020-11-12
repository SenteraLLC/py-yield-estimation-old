import intake
import satsearch

from src.log_cfg import logger
from src.api import fetch_stac_collections

from rio_tiler.io import COGReader, STACReader

def yield_detection(geojson):
    dates = '2020-07-20/2020-08-05'
    URL='https://earth-search.aws.element84.com/v0'
    results = satsearch.Search.search(url=URL,
                                  collections=['sentinel-s2-l2a-cogs'],
                                  datetime=dates,
                                  bbox=bounds,    
                                  sort=['<datetime'])

    catalog = intake.open_stac_item_collection(results.items())

    # TODO: select the best catalog from the date range
    #select_catalog = catalog['S2A_14TQN_20200802_0_L2A']

    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    
    # URLs of catalogs - STACReader doesn't like StacItemCollections
    stac_assets = [stac_item.format(sceneid=scene) for scene in catalog]

    # for loop is pointless since it'll only calculate for the last catalog TODO
    for item in stac_assets:
        with STACReader(item) as cog:
            ndvi = cog.part(bounds, 
                           resampling_method="bilinear", 
                           dst_crs="epsg:4326", 
                           expression="(B08-B04)/(B08+B04)", 
                           max_size=None)
    
    # ndvi is of type ImageData (from rio-tiler), data_as_image() converts it to an ndarray.
    imshow(ndvi.data_as_image())
    print('\nMax NDVI: {m}'.format(m=ndvi.data.max()))
    print('Mean NDVI: {m}'.format(m=ndvi.data.mean()))
    print('Median NDVI: {m}'.format(m=np.median(ndvi.data)))
    print('Min NDVI: {m}'.format(m=ndvi.data.min()))

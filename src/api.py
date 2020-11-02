import json
import datetime
import satsearch
import intake

from rasterio.features import bounds as featureBounds

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search"

def fetch_stac_collections(geojson):
    # Dates from event body? Hardcoded for now.
    dates = '2020-07-31/2020-08-05'

    # TODO: Catch error if bad request passed to event 
    bounds = list(featureBounds(geojson))

    results = satsearch.Search.search(url=STAC_API_ENDPOINT,
                                      collections=['sentinel-s2-l2a-cogs'],
                                      datetime=dates,
                                      bbox=bounds,    
                                      sort=['<datetime'])
    #print('%s items' % results.found())
    catalog = intake.open_stac_item_collection(results.items())

    return catalog
  
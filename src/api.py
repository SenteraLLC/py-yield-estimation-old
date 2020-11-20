import json
import datetime
import satsearch
import intake

from rasterio.features import bounds as featureBounds

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search/"

def fetch_stac_scenes(geojson):
    # date format:
    dates = '2019-07-20/2019-08-05'
    #dates = start_date + '/' + end_date
    # TODO: Catch error if bad request passed to event 
    bounds = list(featureBounds(geojson))

    results = satsearch.Search.search(url=STAC_API_ENDPOINT,
                                      collections=['sentinel-s2-l2a-cogs'],
                                      datetime=dates,
                                      bbox=bounds,    
                                      sort=['<datetime'])
    
    scenes = intake.open_stac_item_collection(results.items())

    return list(scenes)


    


  
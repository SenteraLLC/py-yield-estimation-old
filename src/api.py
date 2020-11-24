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

def find_best_date(scenes):
    best_ratio = 0
    # find the best scene with the least cloud cover. 
    scl_dates = [catalog[item].SCL().metadata['href'] for item in catalog]

    for date in scl_dates: 
        with COGReader(date) as cog:
            valid_pixels = 0
            for row in range(len(cog.dataset)):
                for col in range(len(band[row])):
                    if band[row][col] == 4 or band[row][col] == 5 or band[row][col] == 6:
                        valid_pixels += 1
                    else:
                        continue
            ratio = valid_pixels / (cog.data.shape[0] * cog.data.shape[1])
            if ratio > best_ratio:
                best_scene = date
                best_ratio = ratio
    
    return best_scene







    


  
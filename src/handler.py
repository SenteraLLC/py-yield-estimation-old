import os
import json
import boto3
import datetime

import itertools
import urllib.parse
import satsearch
import intake

from src.api import fetch_stac_collections

#from lambda_proxy.proxy import API
from rasterio.features import bounds as featureBounds

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search"

def main_handler(event, context):
    # dates = start_date + '/' + end_date

    # # TODO: Catch error if bad request passed to event 
    # bounds = list(featureBounds(geojson))

    # results = satsearch.Search.search(url=STAC_API_ENDPOINT,
    #                                   collections=['sentinel-s2-l2a-cogs'],
    #                                   datetime=dates,
    #                                   bbox=bounds,    
    #                                   sort=['<datetime'])
    
    # collection = intake.open_stac_item_collection(results.items())

    # catalog_assets = find_best_collection(collection)









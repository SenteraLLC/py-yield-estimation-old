import os
import json
import boto3
import datetime

import itertools
import urllib.parse
import satsearch
import intake

#from lambda_proxy.proxy import API
from rasterio.features import bounds as featureBounds

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search"

def main_handler(event, context):
    # Dates from event body?
    dates = '2020-07-31/2020-08-05'

    # TODO: Catch error if bad request passed to event 
    bounds = list(featureBounds(event))

    results = satsearch.Search.search(url=STAC_API_ENDPOINT,
                                      collections=['sentinel-s2-l2a-cogs'],
                                      datetime=dates,
                                      bbox=bounds,    
                                      sort=['<datetime'])
    print('%s items' % results.found())
    items = results.items()
    catalog = intake.open_stac_item_collection(items)

    return json.dumps(list(catalog))

def download_assets(results):
    items = results.items()
    keys = set([k for i in items for k in i.assets])
    
    # TODO: Use py-aws-utils for uploading to S3?
    for key in keys:
        upload_asset = items.download(key=key, filename_template='downloads/${date}/${id}')



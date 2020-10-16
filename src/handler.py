# import os
import json
# import base64
# import requests
# import datetime
# import itertools
# import urllib.parse
# import satsearch

# from lambda_proxy.proxy import API
# from rasterio.features import bounds as featureBounds

# STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search"

# Hardcoded for the time being
# DATE_MIN = "2020-08-05"
# DATE_MAX = "2020-07-26"

# Some API Gateway endpoint
# APP = API(name="sentinel-stac")

# @APP.route(
#     "/",
#     methods=["POST"],
#     cors=True,
#     payload_compression_method="gzip",
#     binary_b64encode=True,
# )
def main_handler(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
    
    # start = datetime.datetime.strptime(DATE_MIN, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00Z")
    # end = datetime.datetime.strptime(DATE_MAX, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59Z")

    # bounds = list(featureBounds(geojson))

    # # TODO: might just use a normal request object
    # results = satsearch.Search.search(url=URL,
    #                                   collections=['sentinel-s2-l2a-cogs'],
    #                                   datetime=dates,
    #                                   bbox=bounds,    
    #                                   sort=['<datetime'])



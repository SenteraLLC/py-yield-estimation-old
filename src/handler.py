import os
import json
import boto3
import datetime

from src.api import fetch_stac_collections
from src.main import yield_detection

from lambda_proxy.proxy import API

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search"

def main_handler(event, context):
    version = os.getenv("VERSION", "unknown")
    logger.info(f"Handling lambda invocation to sentinel-stac ({version})")
    
    return yield_detection(event)









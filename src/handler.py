import os
import json
import datetime
import geojson
from lambda_proxy.proxy import API

from src.main import ndvi_mean

APP = API(name='yield-estimation')

def lambda_handler(event, context):
    version = os.getenv('VERSION', 'unknown')
    logger.info(f'Handling lambda invocation to yield-estimation ({version})')

    return yield_estimation(event)


@APP.route(
    '/yield',
    methods=["POST"],
    cors=True,
    binary_b64encode=True
)
def main_handler(body):
    version = os.getenv('VERSION', 'unknown')
    logger.info(f'Handling lambda invocation to yield-estimation ({version})')

    geo = geojson.loads(body)
    
    try:

        yield_estimator = ndvi_mean(geo) 

        return ('OK', 'application/json', json.dumps(ndvi_mean))

    except Exception as e:
        return ('ERROR', 'application/json', json.dumps({'errorMessage': str(e)}))



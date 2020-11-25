import os
import json
import datetime
import geojson

from lambda_proxy.proxy import API

APP = API(name='yield-estimation')

def lambda_handler(event, context):
    version = os.getenv("VERSION", "unknown")
    logger.info(f"Handling lambda invocation to yield-estimation ({version})")

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
        scene = best_dated_scene(geo)
        yield_estimator = yield_estimation(scene, geo)

        return ("OK", "application/json", json.dumps(yield_estimator))

    except Exception as e:
        return ("ERROR", "application/json", json.dumps({"errorMessage": str(e)}))










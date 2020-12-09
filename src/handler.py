import json
import os

import geojson
from lambda_proxy.proxy import API

from src.log_cfg import logger
from src.main import yield_estimation

APP = API(name="yield-estimation")


def lambda_handler(event, context):
    version = os.getenv("VERSION", "unknown")
    logger.info(f"Handling lambda invocation to yield-estimation ({version})")

    return yield_estimation(event)


@APP.route("/yield-estimate", methods=["POST"], cors=True, binary_b64encode=True)
def main_handler(body, context):
    """Note: If invoking locally with the Serverless framework,
    comment out the geojson.loads() line and pass body directly to ndvi_mean()
    since we pass the body as a string from the terminal.
    """
    version = os.getenv("VERSION", "unknown")
    logger.info(f"Handling lambda invocation to yield-estimation ({version})")

    geo = geojson.loads(body)

    try:

        yield_estimator = yield_estimation(geo)

        return ("OK", "application/json", json.dumps(yield_estimator))

    except Exception as e:
        return ("ERROR", "application/json", json.dumps({"errorMessage": str(e)}))

# from src.log_cfg import logger
import math
from urllib.parse import urlparse

import numpy as np
from rasterio.features import bounds as featurebounds
from rio_tiler.io import STACReader
from rio_tiler.models import ImageData

from src.api import fetch_stac_scenes, least_cloud_cover_date


def yield_estimation(geojson):

    scenes = fetch_stac_scenes(geojson)

    best_scene = least_cloud_cover_date(scenes, geojson)

    # Scene path from the AWS URL for element84 query. ex: S2B_14TQN_20200708_0_L2A
    scene_path = urlparse(best_scene).path.split("/")[-2]

    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    stac_asset = stac_item.format(sceneid=scene_path)

    bounds = featurebounds(geojson)

    with STACReader(stac_asset) as cog:
        ndvi, _ = cog.part(bounds, expression="(B08-B04)/(B08+B04)")
        # Crop and resample scene classification band
        scl_band, mask = cog.part(
            bounds,
            resampling_method="nearest",
            height=ndvi.shape[1],
            width=ndvi.shape[2],
            assets="SCL",
            max_size=None,
        )

    # Apply cloud mask
    masked = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)

    # NDVI as a MaskedArray
    ndvi_masked = ImageData(ndvi, masked).as_masked()

    # print("\nMax NDVI: {m}".format(m=ndvi_masked.max()))
    # print("Mean NDVI: {m}".format(m=ndvi_masked.mean()))
    # print("Median NDVI: {m}".format(m=np.median(ndvi_masked.data)))
    # print("Min NDVI: {m}".format(m=ndvi_masked.min()))

    yield_estimate = 11.359 * math.exp(3.1 * ndvi_masked.mean())

    return yield_estimate

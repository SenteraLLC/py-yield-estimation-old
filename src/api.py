import intake
import numpy as np
from datetime import date
import logging
from satsearch import Search
from rasterio.features import bounds as featurebounds
from rio_tiler.io import COGReader


def least_cloud_cover_date(scenes, geojson):
    best_ratio = 0
    bounds = featurebounds(geojson)

    # find the best scene with the least cloud cover.
    scl_dates = [scenes[item].SCL().metadata["href"] for item in scenes]

    for date in scl_dates:
        with COGReader(date) as cog:
            band, mask = cog.part(bounds)

            valid_pixels = np.count_nonzero((band == 4) | (band == 5) | (band == 6))

            ratio = valid_pixels / (band.shape[0] * band.shape[1])

            if ratio > best_ratio:
                best_scene = date
                best_ratio = ratio

    return best_scene

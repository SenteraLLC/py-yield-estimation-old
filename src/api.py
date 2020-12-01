import intake
import numpy as np
import satsearch
from rasterio.features import bounds as featurebounds
from rio_tiler.io import COGReader

STAC_API_ENDPOINT = "https://earth-search.aws.element84.com/v0/search/"


def fetch_stac_scenes(geojson):
    # date format:
    dates = "2019-07-20/2019-08-05"
    # dates = start_date + '/' + end_date
    # TODO: Catch error if bad request passed to event
    bounds = list(featurebounds(geojson))

    results = satsearch.Search.search(
        url=STAC_API_ENDPOINT,
        collections=["sentinel-s2-l2a-cogs"],
        datetime=dates,
        bbox=bounds,
        sort=["<datetime"],
    )

    scenes = intake.open_stac_item_collection(results.items())

    return scenes


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

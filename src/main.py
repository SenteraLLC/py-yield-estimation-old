from src.log_cfg import logger

import numpy as np
from rio_tiler.io import COGReader, STACReader
from rio_tiler.profiles import img_profiles
from rio_tiler.models import ImageData, Metadata

from rasterio.features import bounds as featureBounds

def yield_estimation(scene, geojson):
    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    stac_asset = stac_item.format(sceneid=scene)

    bounds = featureBounds(geojson)

    with STACReader(stac_asset) as cog:
        ndvi, _ = cog.part(bounds, expression='(B08-B04)/(B08+B04)')
        # Grab the resampled SCL layer
        scl_band, mask = cog.part(bounds, 
                            resampling_method="nearest", 
                            height=ndvi.shape[1], 
                            width=ndvi.shape[2], 
                            assets='SCL',
                            max_size=None)

    # Apply cloud mask
    sc = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)

    # NDVI as a MaskedArray
    ndvi_masked = ImageData(ndvi, sc).as_masked()
    
    print('\nMax NDVI: {m}'.format(m=ndvi_masked.max()))
    print('Mean NDVI: {m}'.format(m=ndvi_masked.mean()))
    print('Median NDVI: {m}'.format(m=np.median(ndvi_masked.data)))
    print('Min NDVI: {m}'.format(m=ndvi_masked.min()))
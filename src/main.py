import intake
import satsearch

from src.log_cfg import logger
from src.api import fetch_stac_collections

from rio_tiler.io import COGReader, STACReader

def yield_prediction(geojson):
    dates = '2020-07-20/2020-08-05'
    stac_item = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/{sceneid}"
    
    stac_asset = stac_item.format(sceneid='S2A_14TQN_20200802_0_L2A')

    with STACReader(stac_asset) as cog:
        ndvi, _ = cog.part(bounds, expression='(B08-B04)/(B08+B04)')
        # Grab the resampled SCL
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
import rasterio
from src.log_cfg import logger

def crop(catalog, band):
    """
    return: Array of cropped tiffs?
    """
    hrefs = [catalog[item][band].metadata['href'] for item in catalog]

    for i in hrefs:
        data = rasterio.open(i)
        print(data.crs)
    
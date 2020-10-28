from src.log_cfg import logger
from src.api import fetch_stac_collections

def yield_detection(geojson):
  """
  :param geojson: Any GeoJSON
  :return: The cropped and masked raster (eventually)
  """
  # cropping = foo(collectionItems)
  # masking = bar(overlay)

  return fetch_stac_collections(geojson)
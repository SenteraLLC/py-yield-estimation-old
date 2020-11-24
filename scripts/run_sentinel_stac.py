import os
import json

from src.api import fetch_stac_scenes
from src.main import yield_estimation

geojson_path = os.path.join(os.path.dirname(__file__), "geojson.json")
with open(geojson_path) as f:
    geojson = json.load(f)

try:
    scenes = fetch_stac_scenes(geojson)
    print(list(scenes))
    # Just run yield estimation on the first date in the collection for now. 
    #yield_estimation(scenes[0], geojson)
except Exception as e:
    print(e)
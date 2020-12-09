import json
import os

from src.main import yield_estimation

geojson_path = os.path.join(os.path.dirname(__file__), "geojson.json")
with open(geojson_path) as f:
    geojson = json.load(f)

try:
    scenes = yield_estimation(geojson)

except Exception as e:
    print(e)

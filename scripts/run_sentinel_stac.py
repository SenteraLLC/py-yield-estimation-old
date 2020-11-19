import os
import json

from src.main import yield_detection

geojson_path = os.path.join(os.path.dirname(__file__), "geojson.json")
with open(geojson_path) as f:
    geojson = json.load(f)

try:
    collections = yield_prediction(geojson)
except Exception as e:
    print(e)
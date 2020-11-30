import os
import json

from src.main import ndvi_mean

geojson_path = os.path.join(os.path.dirname(__file__), "geojson.json")
with open(geojson_path) as f:
    geojson = json.load(f)

try:
    scenes = ndvi_mean(geojson)

except Exception as e:
    print(e)
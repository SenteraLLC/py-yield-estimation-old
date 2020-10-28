import os
import json

from src.main import yield_detection

def download_assets(results):
    """
    Pass collections to this function to download datasets locally
    """
    items = results.items()
    keys = set([k for i in items for k in i.assets])
    for key in keys:
        items.download(key=key, filename_template='datasets/${date}/${id}')

geojson_path = os.path.join(os.path.dirname(__file__), "geojson.json")
with open(geojson_path) as f:
    geojson = json.load(f)

try:
    collections = yield_detection(geojson)
    print("Collection returned from API successfully ", collections)
except Exception as e:
    print(e)
import numpy as np
import click
from rasterio.features import bounds as featurebounds
from rio_tiler.io import COGReader
from rio_tiler.models import ImageData
from datetime import date
from rasterio.plot import reshape_as_image
import geojson
from satsearch import Search
from pathlib import Path
import imageio

ELEMENT84_URL = "https://earth-search.aws.element84.com/v0/search/"
SENTINEL_L2A_COLLECTION = 'sentinel-s2-l2a-cogs'

"""
python main.py field.json --start_time 2020-07-20 --end_time 2020-07-30
The geojson is assumed to be WGS84 (epsg:4326).
"""

def search(bbox: dict, start: str, end: str) -> object:
    """
    Query Element84 API for scenes given a bounding box and a date range.
    :param bbox: The bounding box for the given area of interest. 
    :param start: A starting date string in the format: YYYY-MM-DD
    :param end: An ending date string in the format: YYYY-MM-DD
    :return: A STAC-spec ItemCollection object containing the scenes. 
    See:
    https://github.com/radiantearth/stac-api-spec/blob/master/fragments/itemcollection/README.md
    for more details. 
    """
    kwargs = {
        'bbox': bbox,
        'datetime': f"{start}/{end}",
        'collections': [SENTINEL_L2A_COLLECTION]
    }
    search = Search(url=ELEMENT84_URL, **kwargs)
    print('Found: ', len(search.items()))
    return search.items()
   
      
def cloud_mask(asset_url: str, bbox: tuple, height: float, width: float):
    """
    A Basic implementation of a cloud mask based on Sentinel-2's Scene Classification Layer. 
    Pixels assigned with values 0-4 are considered to be shadows, while pixels greater than 6 are 
    cloud probable. In most cases, the SCL will need to be reprojected to the correct resolution 
    for the mask to be applied, so we pass both the height and width of the receieving 
    band in order to reproject the this band correctly. 
    
    Args:
        asset_url (str): The URL of the Scene classification layer. 
        bbox (tuple): The bounding box for the given area of interest. 
        height (float): height of the desired reprojection for the classification layer. 
        width (float): Width of the desired reprojection for the classification layer. 

    Returns:
        [numpy.ma.masked_array]: SCL layer with masked cloud pixels. 
    """
    with COGReader(asset_url) as cog:
        scl_band, _ = cog.part(
            bbox,
            resampling_method="nearest",
            height=height, 
            width=width
        )
    cloud_mask = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)
    return cloud_mask


def process_scenes(scenes, bands, bbox):
    """
    Process each scene, applying the cloud mask,
    for the given bands for a bounding box. 

    Args:
        scenes (ItemCollection): Collection of scenes for a given date range. 
        bands (list): The bands to be processed from the command line. 
        bbox ([tuple]): The bounding box for the given area of interest. 
    """
    for scene in scenes:
        # Set the SCL for the cloud mask. 
        scl_url = scene.asset('SCL')['href']
        for band in bands:
            stac_asset = scene.asset(band)['href']
            with COGReader(stac_asset) as cog:
                img, _ = cog.part(bbox)
                
                msk = cloud_mask(scl_url, bbox, height=img.shape[1], width=img.shape[2])
                
                imgData = ImageData(img, msk).as_masked()
                
                # Reshape as RGB for writing. 
                img_reshape = reshape_as_image(imgData)
                save_scenes(scene, band, img_reshape)
        
                
def save_scenes(scene, band, data):
    print('Saving image...')
    path = Path.cwd() /'sentinel-scenes' / str(scene)
    print(path)
    path.mkdir(parents=True, exist_ok=True)
    imageio.imwrite(str(path) + '/' + str(band) + '.tif', data)

    
@click.command(short_help="Pull Sentinel-L2A-COGS for an area of interest")
@click.argument("shape_file", type=str, nargs=1)
@click.option(
    "--bands", "-b", type=str, multiple=True, help="Bands to include for processing.",
    default=['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B8A', 'B11', 'B12', 'SCL']
)
@click.option("--start_time", type=str, default="", help="Start of the date range")
@click.option("--end_time", type=str, default="", help="End of the date range")
def main(shape_file, bands, start_time, end_time):
    f = open(shape_file)
    data = geojson.load(f)
    
    bbox = featurebounds(data)
    scene_assets = search(bbox, start_time, end_time)
    
    process_scenes(scene_assets, bands, bbox)
    
    
if __name__ == '__main__':
    main()

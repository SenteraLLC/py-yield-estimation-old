import numpy as np
import click
from rasterio.features import bounds as featurebounds
from rio_tiler.io import STACReader, COGReader
from rio_tiler.mosaic import mosaic_reader
from rio_tiler.models import ImageData
from datetime import date
from rasterio.plot import reshape_as_image
from pylab import *
from matplotlib import pyplot as plt
import geojson
from satsearch import Search
from pathlib import Path
import imageio

ELEMENT84_URL = "https://earth-search.aws.element84.com/v0/search/"
SENTINEL_L2A_COLLECTION = 'sentinel-s2-l2a-cogs'


def search(geometry: dict, start: str, end: str) -> object:
    kwargs = {
        'bbox': geometry,
        'datetime': f"{start}/{end}",
        'collections': [SENTINEL_L2A_COLLECTION]
    }
    search = Search(url=ELEMENT84_URL, **kwargs)
    print('found: ', len(search.items()))
    return search.items()
   
      
def cloud_mask(asset_url: str, geometry: tuple, height: float, width: float):
    with COGReader(asset_url) as cog:
        scl_band, _ = cog.part(
            geometry,
            resampling_method="nearest",
            height=height, 
            width=width
        )
    # 0 - 4 are shadows, while pixels greater than 6 are cloud probable. 
    cloud_mask = np.ma.where((scl_band < 4) | (scl_band > 6), 0, 1)
    return cloud_mask


def process_scenes(scenes, bands, geometry):
    for scene in scenes:
        scl_url = scene.asset('SCL')['href']
        print('urls: ', scl_url)
        
        for band in bands:
            stac_asset = scene.asset(band)['href']
            with COGReader(stac_asset) as cog:
                img, _ = cog.part(geometry)
                msk = cloud_mask(scl_url, geometry, height=img.shape[1], width=img.shape[2])
                
                scene = ImageData(img, msk).as_masked()
                
                # Reshape as RGB for writing. 
                img_data = reshape_as_image(scene)
                
                return ImageData(img, msk).as_masked()
                
def write_output(scene):
    path = Path.cwd() /'sentinel-images'
    path.mkdir(parents=True, exist_ok=True)

    imageio.imwrite(str(path) + '/' + 'img.tif', scene)
    # plt.imshow(reshape_as_image(scene))
    # plt.show()
    
@click.command(short_help="Pull Sentinel-L2A-COGS for an area of interest")
@click.argument("shape_file", type=str, nargs=1)
@click.option(
    "--bands", "-b", type=str, multiple=True, help="Band index to pull",
    default=['B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'SCL']
)
@click.option("--start_time", type=str, default="", help="Start of the date range")
@click.option("--end_time", type=str, default="", help="End of the date range")
def main(shape_file, bands, start_time, end_time):
    f = open(shape_file)
    data = geojson.load(f)
    bbox = featurebounds(data)
    scene_assets = search(bbox, start_time, end_time)
    scene = process_scenes(scene_assets, bands, bbox)
    
    # TODO: Call in process_images
    write_output(reshape_as_image(scene))


if __name__ == '__main__':
    main()

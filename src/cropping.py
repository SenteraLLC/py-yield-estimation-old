"""Sentera cropping target filed from TIFF script"""

"""Author: Jingtian Shi"""


import pycrs
import rasterio.warp
from rasterio.mask import mask
import geopandas as gpd
import geojson


"""Lib used for print and debugging"""
from rasterio.plot import show


"""parse target coordinates and features of GeoDataFrame into JSON format"""
def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

# Press the green button in the gutter to run the script.
def cropping():

    """# Cropping from a random image at a given coordinate
    #######################################################"""

    """read TIFF file"""
    data = rasterio.open('/home/david/Desktop/testing/sample2/2020-08-02/S2A_14TQN_20200802_0_L2A_SCL.tif')

    """print some basic info of TIFF for debugging"""
    # print(data.bounds)
    # print(data.crs)
    # print(data.height)
    # print(data.width)
    # show((data,1), cmap="terrain")


    """read GeoJSON file"""
    with open('/home/david/Desktop/testing/sample2/real_user_field.geojson') as f:
        user = geojson.load(f)
    # print(user)

    """extract features attributs from TIFF image, and assign to EPSG 4326 CRS.
       signing CRS is required for cropping!!
       change the CRS of input coordinate to given TIFF CRS"""
    gdf = gpd.GeoDataFrame.from_features(user["features"],crs="EPSG:4326")
    gdf = gdf.to_crs(crs=data.crs.data)
    # print(gdf.head())
    # print(gdf.crs)

    """convert the output coordinates to JSON format"""
    out_coords = getFeatures(gdf)
    # print(out_coords)

    """Cropping the TIFF image with targeted coordinates, note there are two return values"""
    out_img, out_transform = mask(dataset=data, shapes=out_coords, crop=True)
    out_meta = data.meta.copy()
    # print(out_meta)

    """create variable to store the CRS for output/clipped image"""
    epsg_code = int(data.crs.data['init'][5:])
    # print(epsg_code)

    """update the coordinates of TIFF image to the targeted coordinates"""
    out_meta.update({"driver": "GTiff",
                     "height": out_img.shape[1],
                     "width": out_img.shape[2],
                     "transform": out_transform,
                     "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})

    """write the output image"""
    with rasterio.open('/home/david/Desktop/testing/sample2/real_user_output.tif', "w", **out_meta) as dest:
        dest.write(out_img)

    """read and print the output filed image for debugging"""
    # clipped = rasterio.open('/home/david/Desktop/testing/sample2/real_user_output.tif')
    # show((clipped, 1), cmap='terrain')
    # print(clipped.bounds)
    # print(clipped.crs)

    """print out the bounding box as needed"""
    # mask = clipped.dataset_mask()
    # for geom, val in rasterio.features.shapes(mask, transform=clipped.transform):
    #     # Transform shapes from the dataset's own coordinate
    #     # reference system to CRS84 (EPSG:4326).
    #     geom = rasterio.warp.transform_geom(clipped.crs, 'EPSG:4326', geom, precision=6)
    #
    #     # Print GeoJSON shapes to stdout.
    #     print(geom)

if __name__ == '__main__':
    cropping()


    """# Cropping a field from a random image at a given coordinate
    ###############################################################"""

    # data = rasterio.open('/home/david/Desktop/try1')
    # # print(data.bounds)
    # # print(data.crs)
    # # print(data.height)
    # # print(data.width)
    # # show((data,1), cmap="terrain")
    #
    # # # WGS84 coordinates
    # minx, miny = -93.493140, 46.04800
    # maxx, maxy = -93.493040, 46.04810
    # bbox = box(minx, miny, maxx, maxy)
    # # # polygon = Polygon([(-95.293049, 45.04626), (-95.270584, 45.058192), (-95.876026, 45.065193), (-95.873833, 45.053505), (-95.293049, 45.04626)])
    #
    # geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0],crs="EPSG:4326")
    # geo = geo.to_crs(crs=data.crs.data)
    #
    # coords = getFeatures(geo)
    # print(coords)
    #
    # out_img, out_transform = mask(dataset=data, shapes=coords, crop=True)
    # out_meta = data.meta.copy()
    # print("cropped image:")
    # print(out_meta)
    #
    # epsg_code = int(data.crs.data['init'][5:])
    # # print(epsg_code)
    #
    # out_meta.update({"driver": "GTiff",
    #                  "height": out_img.shape[1],
    #                  "width": out_img.shape[2],
    #                  "transform": out_transform,
    #                  "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})
    #
    # with rasterio.open('/home/david/Desktop/test_result_good_shape', "w", **out_meta) as dest:
    #     dest.write(out_img)
    #
    # clipped = rasterio.open('/home/david/Desktop/out2')
    # show((clipped, 1), cmap='terrain')
    #
    # print("end")


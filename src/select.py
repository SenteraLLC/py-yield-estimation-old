"""This function selects the optimal date of SCL TIFF file for generating mask"""

"""Author: Jingtian(David) Shi"""


import rasterio
import os


def select():

    """give the path for all the SCL TIFF files"""
    directory = '/home/david/Desktop/testing/sample2'

    """Initialize the best valid pixel ration to 0 and the best TIFF image name to None"""
    best_ratio = 0
    best_tif = None

    """scan thru the folder to read each SCL file"""
    for entry in os.scandir(directory):
        if (entry.path.endswith(".tif")) and entry.is_file():

            data = rasterio.open(entry.path)
            band = data.read(1)

            # print(entry.path)
            # msk = data.read_masks(1)
            # msk.show()

            """count the total valid pixels and then divide by total pixels"""
            valid_pixels = 0
            for row in range(len(band)):
                for col in range(len(band[row])):
                    if band[row][col] == 4 or band[row][col] == 5 or band[row][col] == 6:
                        valid_pixels += 1
                    else:
                        continue

            ratio = valid_pixels / (data.shape[0] * data.shape[1])

            """selecting the best ratio and memorize the name of that TIFF"""
            if ratio > best_ratio:
                best_tif = entry.path
                best_ratio = ratio

    """check the ratio and name of TIFF file"""
    print(best_ratio)
    print(best_tif)

if __name__ == '__main__':
    select()

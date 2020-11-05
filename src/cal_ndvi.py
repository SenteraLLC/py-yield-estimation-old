"""This function calculate the mean NDVI value based on
   masked Red and NIR rasters"""


"""Input: stacked raster of Red and NIR bands"""
"""Output: Mean NDVI value"""

"""Author: Jingtian(David) Shi"""



import rasterio
import rasterio.plot
import numpy
import sys
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show


def cal_mean_ndvi():

    src = rasterio.open('/home/david/Desktop/testing/real_data/result.tif')

    show((src, 1), cmap='terrain')
    show((src, 2), cmap='terrain')
    # im1 = src.read(1)
    # pyplot.imshow(im1, cmap='pink')
    # pyplot.show()
    # im2 = src.read(2)
    # pyplot.imshow(im2, cmap='pink')
    # pyplot.show()

    red = src.read(1)
    nir = src.read(2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    plot.show(red, ax=ax1, cmap='Blues')  # red
    plot.show(nir, ax=ax2, cmap='Blues')  # nir
    fig.tight_layout()

    ndvi=np.where(
        (nir + red) == 0.,
        0,
        (nir-red)/(nir+red)
    )

    numpy.set_printoptions(threshold=sys.maxsize)
    print(ndvi)
    mean_ndvi = numpy.mean(ndvi)
    print(mean_ndvi)

    yeild = 11.359 * (2.7182818284590452353602874713527 ** (3.36 * mean_ndvi))
    # yeild = 11.359 * np.math.exp(3.36 * mean_ndvi)
    print("The mean ndvi : " + str(mean_ndvi))
    print("The yeild prediction: " + str(yeild))



if __name__ == '__main__':
    cal_mean_ndvi()
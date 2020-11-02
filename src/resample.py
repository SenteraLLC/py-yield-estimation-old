""" resample the cropped field to 10 meter resolution"""

"""Author: Jingtian(David) Shi"""


import sys
import numpy
import rasterio
import rasterio.mask
from rasterio import Affine
from rasterio.enums import Resampling

"""used for print image and debug"""
import numpy as np
from rasterio.plot import show

def resample():

    """resample the SCL image to 10 meter resolution"""
    def resample_raster(raster, scale=2):
        t = raster.transform

        # rescale the metadata
        transform = Affine(t.a / scale, t.b, t.c, t.d, t.e / scale, t.f)
        height = raster.height * scale
        width = raster.width * scale

        profile = src.profile
        profile.update(transform=transform, driver='GTiff', height=height, width=width)


        data = raster.read(  # Note changed order of indexes, arrays are band, row, col order not row, col, band
            out_shape=(raster.count, height, width),
            resampling=Resampling.nearest,
        )

        """write down resampled file for later access"""
        with rasterio.open('/home/david/Desktop/testing/sample2/resample.tif', 'w', **profile) as dst:
            dst.write(data)
            del data
            return dst.name

    numpy.set_printoptions(threshold=sys.maxsize)
    src = rasterio.open('/home/david/Desktop/testing/sample2/real_user_output.tif',mode='r+')
    path = resample_raster(src)
    resampled = rasterio.open(path)

    """check on the attributes of source file and resample file"""
    # print(path)
    # im1 = src.read(1)
    # pyplot.imshow(im1, cmap='pink')
    # pyplot.show()
    # print(resampled)
    # print(resampled.shape)
    # print(resampled.dtypes)

    # msk = resampled.read_masks()
    # print("show mask")
    # show(np.dstack(msk))
    # print(msk.type)
    # print(msk[0][3:15,3:15])


if __name__ == '__main__':
    resample()






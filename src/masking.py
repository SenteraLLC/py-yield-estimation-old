"""Apply SCL mask to Red and NIR bands"""

"""Author: Jingtian(David) Shi"""

import rasterio
from matplotlib import pyplot
from pandas import np
from rasterio import features
import rasterio.mask


def masking():

    """SCL mask"""
    msk = rasterio.open('/home/david/Desktop/testing/sample2/resample.tif')
    # print(msk.shape)
    # src_to_crop = rasterio.open('/home/david/Desktop/testing/sample_RN/2020-07-23/S2A_14TQN_20200723_0_L2A_B04.tif')

    """Red and NIR stacked bands"""
    src_to_crop = rasterio.open('/home/david/Desktop/testing/sample_RN/stack.tif')
    # print(src_to_crop.count)

    """Applying SCL mask to Red and NIR stacked bands"""
    msk_affine = msk.meta.get("transform")
    band = msk.read(1)
    band[np.where(band != msk.nodata)] = 1
    geoms = []
    for geometry, raster_value in features.shapes(band, transform=msk_affine):
        # get the shape of the part of the raster
        # not containing "nodata"
        if raster_value == 1:
            geoms.append(geometry)

    out_img, out_transform = rasterio.mask.mask(
        dataset=src_to_crop,
        shapes=geoms,
        crop=True,
    )

    """update the new masked Red and NIR stacked bands and write(optional)"""
    with rasterio.open(
            '/home/david/Desktop/testing/sample2/result.tif',
            'w',
            driver='GTiff',
            height=out_img.shape[1],
            width=out_img.shape[2],
            count=src_to_crop.count,
            dtype=out_img.dtype,
            transform=out_transform,
    ) as dst:
        dst.write(out_img)

    ss = rasterio.open('/home/david/Desktop/testing/sample2/result.tif')

    """print the property and the image of new masked image"""
    # print(ss)
    # print(ss.count)
    # print(ss.shape)
    # im1 = ss.read(2)
    # pyplot.imshow(im1, cmap='pink')
    # pyplot.show()


if __name__ == '__main__':
    masking()
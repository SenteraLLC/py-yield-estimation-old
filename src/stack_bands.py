"""This function is used to stack multiple bands together
   in this script is for stacking Red and NIR bands
   can be changed to stack any other bands as well"""

"""Author: Jingtian(David) Shi"""

import rasterio

"""lib used for print and debugging"""
from matplotlib import pyplot


def stack_bands():

    """The list of all bands wanted to be stacked together"""
    file_list = ['/home/david/Desktop/testing/sample_RN/2020-07-23/S2A_14TQN_20200723_0_L2A_B04.tif',
                 '/home/david/Desktop/testing/sample_RN/2020-07-23/S2A_14TQN_20200723_0_L2A_B08.tif']

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count=len(file_list))
    print(len(file_list))

    # Read each layer and write it to stack
    with rasterio.open('/home/david/Desktop/testing/sample_RN/stack.tif', 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))

    """Open the stack and print for debugging"""
    # src = rasterio.open('/home/david/Desktop/testing/sample_RN/stack.tif')
    # pyplot.imshow(src.read(1), cmap='pink')
    # pyplot.show()


if __name__ == '__main__':
    stack_bands()
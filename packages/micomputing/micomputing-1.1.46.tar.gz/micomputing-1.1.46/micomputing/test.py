
try: from pycamia import info_manager
except ImportError: print("Warning: pycamia not loaded. ")

__info__ = info_manager(
    project = "",
    package = "",
    author = "", 
    create = "",
    fileinfo = "",
    requires = ""
)

import os, sys, re
import batorch as bt
from micomputing.funcs import distance_map_cpp, dilate_cpp, dilate, dilate_python
from pycamia import tokenize, scope

def main():
    image1 = ((bt.image_grid(100, 100, 100) - bt.channel_tensor([50, 50, 50])) ** 2).sum({}) < 400
    image2 = bt.zeros(100, 100, 100)
    image2[20:-20, 20:-20, 20:-20] = 1;
    image2 *= ~image1;
    image = bt.stack(image1, image2, [])
    dismap = distance_map_cpp(image, spacing=(1, 2, 1))
    bt.display(image[1, ..., 50], dismap[1, ..., 50]).show()
    return
    bt.display(image2, dilate_cpp(image2, -1)).show()
    with scope("use cpp"):
        dc = dilate_cpp(image2, 20)
        dc = dilate_cpp(image2, 10)
    with scope("use itk"):
        di = dilate(image2, 20)
        di = dilate(image2, 10)
    # with scope("use python"):
    #     dp = dilate_python(image2, 20)
    #     dp = dilate_python(image2, 10)
    bt.display(dc[..., 50], di[..., 50]).show()

if __name__ == "__main__": main()

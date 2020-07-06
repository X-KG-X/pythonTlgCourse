#!/usr/bin/env python3

from matplotlib.pyplot import imshow
from PIL import Image
import numpy as np
import skimage.color as sc

def main():
    i=np.array(Image.open('img.jpg'))
    imshow(i)


if __name__=="__main__":
    main()
# -*- coding: utf-8 -*-
"""
make gif from select folder
credit to https://github.com/dm20/gif-maker
"""
import imageio
import os
import sys
import re
from os.path import isfile, join
from pathlib import Path
import numpy as np
# from tkinter import filedialog

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from .plotformat import setup


"""
gif_maker many thanks
https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
fp_in = "/path/to/image_*.png"
fp_out = "/path/to/image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)
"""

class animate(object):
    def __init__(self,
                 output):
        self.plot_directory = output
        self.img_name = None
        self.fmt = setup('animation',3)

    def to_gif(self,
               targetpath:str = '.',
               delay:float = 1.33,
               sort:bool = False,
               ext:str = 'png'
               ):
        """
        """
        filelist = [f for f in os.listdir(targetpath)
                    if isfile(join(targetpath, f))
                    and f.endswith(ext)]


        if sort:
            # index = lambda x: re.search('\.\d_',str(x)).group()
            s = lambda x: re.split(r'\d*\.*\d*_',str(x),1)   # t = 1.4_20200505... & 15_2020..
            index = np.array([s(file) for file in filelist],dtype=str)
            if len(index.shape)==1:
                print('err 1D arry')
                return False


            files = np.array([index[...,-1],filelist],dtype=str).T
            files = files[files[...,0].argsort()]
            filelist = list(files[:,1])
            # print(filelist)
        img = lambda f: imageio.imread(targetpath / f)
        images = list(map(img, filelist))

        self.img_name = self.fmt.plot_name(str(targetpath.stem),'gif')
        print('self.img_name',self.img_name)

        dest = self.plot_directory.parent / (str(targetpath.stem)+'.gif')
        print('dest',dest)
        imageio.mimsave(self.img_name, images, duration = delay)


if __name__=='__main__':
    #targetpath = filedialog.askopenfilenames(parent=root, title = 'select files: ')
    targetpath = Path(r'/Users/Michael/Documents/GitHub/MacPersonal/AMATH502/plot_output/ps6')
    to_gif(targetpath,delay,False,'png')

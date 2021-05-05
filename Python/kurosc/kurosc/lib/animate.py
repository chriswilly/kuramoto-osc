# -*- coding: utf-8 -*-
"""
make gif from select folder
credit to https://github.com/dm20/gif-maker
"""
# from tkinter import filedialog
import imageio
import os
import sys
import re
import numpy as np
from os.path import isfile, join

from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1])
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'

from lib.plotformat import setup


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
        self.fmt = setup('animation',4)



    def to_gif(self,
               targetpath:str = None,
               delay:float = 1.33,
               sort:bool = False,
               ext:str = 'png'
               ):
        """
        """
        if not targetpath:
            targetpath = self.plot_directory
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
        # print('self.img_name',self.img_name)
        # dest = self.plot_directory.parent / (str(targetpath.stem)+'.gif')
        # print('dest',dest)
        imageio.mimsave(self.img_name, images, duration = delay)


        try:
            # # print(targetpath.stem)
            # new = self.fmt.plotname(str(targetpath.stem))
            # print(self.plot_directory/new)
            new = self.fmt.plotname(str(targetpath.stem))
            print('',new)
            print(f'did not actually timestamp images, make sure to clean {targetpath.stem} up before running agin :)')

        except:
            print(f'error timestamping images, make sure to clean {targetpath.stem} up before running agin :)')




if __name__=='__main__':
    #targetpath = filedialog.askopenfilenames(parent=root, title = 'select files: ')
    targetpath = Path(r'/Users/Michael/Documents/GitHub/MacPersonal/AMATH502/plot_output/ps6')
    to_gif(targetpath,delay,False,'png')

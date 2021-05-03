# -*- coding: utf-8 -*-
"""
make gif from select folder
credit to https://github.com/dm20/gif-maker
"""
import imageio
import os
import re
from os.path import isfile, join
from pathlib import Path
import numpy as np
# from tkinter import filedialog


# from .plotformat import setup


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

    def to_gif(self,
               targetpath:str = '.',
               delay:float = 1.33,
               sort:bool = False,
               ext:str = 'png'):
        """
        """
        filelist = [f for f in os.listdir(targetpath) if isfile(join(targetpath, f))
                                                            and f.endswith(ext)]


        if sort:
            # index = lambda x: re.search('\.\d_',str(x)).group()
            separate = lambda x: re.split('\.\d_',str(x))   # t = 1.4_20200505...
            index = np.array([separate(file) for file in filelist],dtype=str)

            files = np.array([index[:,1],filelist],dtype=str).T
            files = files[files[:,0].argsort()] # timestamp sort
            filelist = list(files[:,1])
            # print(filelist)

        img = lambda f: imageio.imread(targetpath / f)
        images = list(map(img, filelist))

        # images = list(map(lambda filename: imageio.imread(targetpath / filename), filelist))
        # dest = (targetpath.resolve().parents[0] / (str(targetpath)
        #                   .replace(str(targetpath.parents[0])+'\\','')+'.gif'))

        dest = self.plot_directory.parent / (str(targetpath.stem)+'.gif')


        print(dest)
        imageio.mimsave(dest, images, duration = delay)



if __name__=='__main__':
    #targetpath = filedialog.askopenfilenames(parent=root, title = 'select files: ')
    delay = 1.33 #s
    targetpath = Path(r'/Users/Michael/Documents/GitHub/MacPersonal/AMATH502/plot_output/ps6')
    to_gif(targetpath,'png',delay)

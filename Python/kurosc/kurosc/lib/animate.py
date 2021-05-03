# -*- coding: utf-8 -*-
"""
make gif from select folder
credit to https://github.com/dm20/gif-maker
"""
import imageio
import os
from os.path import isfile, join
from pathlib import Path
# from tkinter import filedialog


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


def to_gif(targetpath:str = '.',
           delay:float = 1.33,
           ext:str = 'png'):
    """
    """
    filelist = [f for f in os.listdir(targetpath) if isfile(join(targetpath, f)) and f.endswith(ext)]
    filelist.sort() # this iteration technique has no built in order, so sort the frames

    images = list(map(lambda filename: imageio.imread(targetpath / filename), filelist))
    dest = (targetpath.resolve().parents[0] / (str(targetpath)
                      .replace(str(targetpath.parents[0])+'\\','')+'.gif'))
    print(dest)
    imageio.mimsave(dest, images, duration = delay)

#targetpath = filedialog.askopenfilenames(parent=root, title = 'select files: ')


if __name__=='__main__':
    delay = 1.33 #s
    targetpath = Path(r'/Users/Michael/Documents/GitHub/MacPersonal/AMATH502/plot_output/ps6')
    to_gif(targetpath,'png',delay)

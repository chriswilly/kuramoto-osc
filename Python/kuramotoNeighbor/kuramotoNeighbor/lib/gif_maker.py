# -*- coding: utf-8 -*-
"""
make gif from select folder
"""
import imageio
import os
from os.path import isfile, join
from pathlib import Path
# from tkinter import filedialog

def CreateGif(targetpath:str = '.',
              ext:str = 'png',
              delay:float = 1.2):
    """
    """
    filelist = [f for f in os.listdir(targetpath) if isfile(join(targetpath, f)) and f.endswith(ext)]
    filelist.sort() # this iteration technique has no built in order, so sort the frames

    images = list(map(lambda filename: imageio.imread(targetpath / filename), filelist))
    dest = targetpath.resolve().parents[0] / (str(targetpath).replace(str(targetpath.parents[0])+'\\','')+'.gif')
    imageio.mimsave(dest, images, duration = delay)

#targetpath = filedialog.askopenfilenames(parent=root, title = 'select files: ')

delay = 1.33 #s
targetpath = Path(r"/Users/Michael/Documents/GitHub/MacPersonal/AMATH502/plot_output/ps6")
CreateGif(targetpath,'png',delay)

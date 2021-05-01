
import os
import matplotlib as mpl
from datetime import datetime
from pathlib import Path

class setup:
    def __init__(self,
                 output:str = 'plot_output'):
        self.title = output
        self.params()
        self.file_path(output.replace(r'\\','').replace(r'$','').strip(),3)  # self.directory


    def plot_name(self,
                  txt:str='placeholder',
                  extension:str = 'png'):
        print(self.directory,self.title)
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S%f")
        file = self.title+'_'+txt.replace('/','-')+'_'+timestamp+f'.{extension}'
        return self.directory / file


    def file_path(self,
                  subdirectory:str = 'plot_output',
                  level:int = 1):
        self.directory = Path(os.path.abspath(__file__)).parents[level] / subdirectory # assume plot dir one level up

        if os.path.exists(self.directory):
            pass
        else:
            try:
                os.mkdir(self.directory)

            except os.error as e:
                print('error:',e)
                self.directory = Path('.')

        print(self.directory)
        # print(os.listdir(self.directory))


    def params(self):
        """matplotlib parameters plot formatting"""
        mpl.rcParams['axes.labelsize'] = 34
        mpl.rcParams['axes.titlesize'] = 34
        mpl.rcParams['xtick.labelsize'] = 24
        mpl.rcParams['ytick.labelsize'] = 24
        mpl.rcParams['axes.xmargin'] = 0
        mpl.rcParams['axes.ymargin'] = 0
        mpl.rcParams['lines.linewidth'] = 2.8
        mpl.rcParams['lines.markersize'] = 18
        mpl.rcParams['lines.markeredgewidth'] = 3
        mpl.rcParams['legend.framealpha'] = 0.93
        mpl.rcParams['legend.fontsize'] = 32

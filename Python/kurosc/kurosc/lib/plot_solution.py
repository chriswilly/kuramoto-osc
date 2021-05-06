"""takes select soscillatorArray: "obj.osc" instance from model.py and constructs plot
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from lib.plotformat import setup

import re
import numpy as np
from scipy.interpolate import RectBivariateSpline


def save_data(data:np.ndarray,
              file_name:str = 'model_data',
              level:int = 3):
    print(file_name)
    fmt = setup(file_name,level)
    np.save(fmt.plot_name(file_name,'npy'),data)


def plot_output(model,obj,
                data:np.ndarray,
                time:np.ndarray,
                file_name:str = 'model_data'):
    print(data.shape)
    for t,image in enumerate(data):
        print('\n\n\n*****************',image)
        # print(kuramoto,kuramoto.osc,'\n\n',image,solution.t[t])
        # input('.')
        model.plot_contour(obj,image,time[t])




def plot_contour(obj,
                 z:np.ndarray,
                 t:float = None,
                 title:str = None,
                 scale:int = None):
    """
    """
    # want to keep this dependence on init setup may also use z.shape[]
    x = np.linspace(0,obj.ic.shape[0],
                      obj.ic.shape[1])
    y = np.linspace(0,obj.ic.shape[1],
                      obj.ic.shape[0])


    # print('*****',x.shape,y.shape,z.shape)
    # input('.')


    if scale:
        s = RectBivariateSpline(x,y,z,kx=3,ky=3)

        x = np.linspace(0,obj.ic.shape[0],
                          obj.ic.shape[1]*scale)
        y = np.linspace(0,obj.ic.shape[1],
                          obj.ic.shape[0]*scale)
        z = s.__call__(x,y).ravel()
    else:
        z = z.ravel()

    x,y = np.meshgrid(x,y,sparse=False)


    # print('%%%%%',x.shape,y.shape,z.shape)
    # input('.')


    phase_array = np.asarray([x.ravel(),y.ravel(),z.ravel()%np.pi]).T
    # print(phase_array.shape)

    if abs(obj.domain[0]) % np.pi == 0 and not obj.domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(obj.domain[0])

    if abs(obj.domain[1]) % np.pi == 0 and not obj.domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(obj.domain[1])

    if not title:
        title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
        # title_trans = ''

        if t or not (t==None):
            if t>10:
                title+=f' at t = {t:.0f}'
            else:
                title+=f' at t = {t:2.1f}'

    plot_phase(obj,
               phase_array,
               title,
               'Location y',
               'Location x'
               )



def plot_phase(obj,
               X: np.ndarray,
               plot_title:str = None,
               y_axis:str = 'y',
               x_axis:str = 'x',
               resolution:int = 24
               ):
    """
    """
    fldr = plot_title.replace('at t = ','')
    fldr = re.sub('[*\d\.\d*]','',fldr).strip()
    # print(fldr)
    fmt = setup(fldr,obj.level)
    obj.plot_directory = fmt.directory

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)


    colorscale = np.linspace(np.min(obj.domain),
                             np.max(obj.domain),
                             resolution,
                             endpoint=True)

    # print(X[...,0].shape,X[...,1].shape,X[...,2].shape)
    print('\n\nx:0',X[0:6,0],'\n\ny:1',X[0:6,1],'\n\nz:2',X[0:6,2])
    # input('.')


    plt.tricontourf(X[...,0],X[...,1],X[...,2],
                    colorscale,
                    cmap=plt.cm.nipy_spectral,
                    )

    plt.gca().invert_yaxis()
    plt.grid(b=True, which='major', axis='both')

    plt.clim(colorscale[0],colorscale[-1])
    obj.domain[1]

    plt.colorbar(ticks=colorscale[::-1][::5],format='%1.2f')

    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    # ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%g $\pi$'))
    # ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=1))

    plt.title(plot_title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    plt.grid(b=None, which='major', axis='both')
    # plt.show()
    fig.savefig(fmt.plot_name(plot_title,'png'))
    plt.close('all')

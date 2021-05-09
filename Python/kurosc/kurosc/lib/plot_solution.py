"""takes select soscillatorArray: "obj.osc" instance from model.py and constructs plot
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from lib.plotformat import setup

import re
import numpy as np
np.set_printoptions(precision=3, suppress=True)
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
                samples:int=4,
                seconds:int=4,
                scale:bool = False,
                file_name:str = 'model_data'):

    # print(data.shape)
    for k in np.arange(data.shape[2]):
        model.plot_contour(obj,data[...,k],time[k],)

        if samples and np.round(10*time[k])%10==0 and not time[k]==time[-1]:
            print(np.round(time[k]))
            idx=np.where(time>=time[k])[0]  # larger set of two
            idy=np.where(time<time[k]+seconds)[0]
            idz = idx[np.in1d(idx, idy)]  # intersection of sets

            # print(idz,'\n',time[idz])
            # input('.')
            model.plot_timeseries(obj,
                                  data[...,idz],
                                  time[idz],
                                  samples,
                                  seconds)


    #TODO call timeseries fn for z,t to select random clusters nearby for 8 periods at each t%1s=0

################################################################################


def plot_timeseries(obj,
                    z:np.ndarray,
                    t:np.ndarray,
                    samples:int=3,
                    seconds:int = 2,
                    title:str = None,
                    y_axis:str = '$\cos(\omega*t)$',
                    x_axis:str = 'time, s',
                   ):
    """plot the solution timeseries for a random cluster of neighbor nodes
    """
    if not title:
        title = f'Solution Timeseries for {samples} Random Neighbors'

        if t[0]:
            if t[0]>10:
                title+=f' at t = {t[0]:.0f} to {t[-1]:.0f}'
            else:
                title+=f' at t = {t[0]:2.1f} to {t[-1]:2.1f}'


    fmt = setup(title,obj.level)  # plotting format obj
    fig = plt.figure(figsize=(16,8))
    ax = fig.add_subplot(111)

    rng = np.random.default_rng()

    rnd_node = rng.choice(np.arange(z.shape[0]),
                          size=2,
                          replace=False,
                          )

    # TODO generalize this to larger square m*n
    neighbors = np.array([[1,1,-1,-1,0,0,1,-1],
                          [1,-1,1,-1,1,-1,0,0]]).T

    idx = np.broadcast_to(rnd_node,neighbors.shape) + neighbors

    ##validate in range, since these are 2d but coupled pairs and where returns 1d just use unique
    # idlimit = np.where(idx<=z.shape[0:2])[0]
    # idzero = np.where(idx>=0)[0]

    # indx within limit
    idlimit0 = np.where(idx[:,0]<z.shape[0])[0]
    idlimit1 = np.where(idx[:,1]<z.shape[1])[0]
    # indx >0, actually if ~-1, -2 that is permissable but it won't be as local
    idzero0 = np.where(idx[:,0]>=0)[0]
    idzero1 = np.where(idx[:,1]>=0)[0]
    # down select x's, y's indiv
    idu = np.intersect1d(idlimit0,idzero0)
    idv = np.intersect1d(idlimit1,idzero1)
    # intersection of permissable sets
    idw = np.intersect1d(idu,idv)

    rnd_near = rng.choice(idx[idw,:],
                         size=samples,
                         replace=False,
                         )
    # rnd_near = np.squeeze(rnd_near)
    ax.plot(t,np.cos(z[rnd_node[0],rnd_node[1],:]),
            '-k',label=f'oscillator at {rnd_node[0]},{rnd_node[1]}')
    for nearby in rnd_near:
        ax.plot(t,np.cos(z[nearby[0],nearby[1],:]),
                '--r',label=f'oscillator at {nearby[0]},{nearby[1]}')
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.grid(b=True, which='major', axis='both')
    ax.legend(loc=0)

    # plt.show()
    fig.savefig(fmt.plot_name(title,'png'))
    plt.close('all')




################################################################################







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



    if scale:
        s = RectBivariateSpline(x,y,z,
                                kx=obj.ic.shape[0],
                                ky=obj.ic.shape[1])

        x = np.linspace(0,obj.ic.shape[0],
                          obj.ic.shape[1]*scale)
        y = np.linspace(0,obj.ic.shape[1],
                          obj.ic.shape[0]*scale)
        z = s.__call__(x,y).ravel()
    else:
        z = z.ravel()

    x,y = np.meshgrid(x,y,sparse=False)



    #### this z%pi is to show phase locking and not precisely the phase state in time
    #### see figures in paper for demo
    #### may do %2pi but would look more chaotic
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
               'Vertical Node Location',
               'Horizontal Node Location'
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



    plt.tricontourf(X[...,0],X[...,1],X[...,2],
                    colorscale,
                    cmap=plt.cm.nipy_spectral,
                    )

    plt.gca().invert_yaxis()
    plt.grid(b=True, which='major', axis='both')

    plt.clim(colorscale[0],colorscale[-1])


    # tick_marks = np.append(colorscale[::-1][::5],0).sort()

    plt.colorbar(ticks=colorscale[::-1][::5],format='%1.2f')

    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=obj.ic.shape[0]/4))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(base=obj.ic.shape[1]/4))


    plt.title(plot_title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    plt.grid(b=None, which='major', axis='both')
    # plt.show()
    fig.savefig(fmt.plot_name(plot_title,'png'))
    plt.close('all')

################################################################################

import re
import numpy as np

def title():

    ti = 2
    tf = 7

    plot_title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
    plot_title +='at t = 99.999'
    fldr = plot_title.replace('at t = ','').replace('\d\.\d*','')
    test = re.sub('\d*\.\d*','',fldr)
    print(test)
    print(fldr)



def plot_fix():
    d = {"/":'-',
         "\\":'',
         '$':'',
         '[':'',
         ']':'',
         '(':'',
         ')':'',
         ',':'_'
         }

    """ '[()[\]{}] | [,\\$]'   ''   ''  """
    for (key,value) in d.items():
        txt = txt.replace(key,value)

    # if not txt:
    #     txt = self.title

    ## TODO
    txt = re.sub('[()[\]{}] | [\\$]','',txt)
    txt = re.sub('/','-',txt)
    txt = re.sub(',','_',txt)




def filename2():
    import numpy as np
    import re


    kernel_params:dict = {'a': 10000/3*2,
                       'b': 0,
                       'c': 10, # breadth of wavelet
                       'order': 4},

    interaction_params:dict = {'beta': 0.75,'r': 0.25},
    title=None
    domain = [0,np.pi]
    kn=11.1

    if abs(domain[0]) % np.pi == 0 and not domain[0] == 0:
        ti = r'\pi'
        ti = '-'+ti
    else:
        ti = str(domain[0])

    if abs(domain[1]) % np.pi == 0 and not domain[1] == 0:
        tf = r'\pi'
    else:
        tf = str(domain[1])

    if not title:
        print(interaction_params,
                kernel_params,
                            )

        title = 'R={r:.2f} $\\beta$={beta:.2f} K/N={kn:.0f} & c={c:.0f} for $\\theta_t$$\in$[${ti}$,${tf}$)'.format(
                                                                                       **interaction_params[0],
                                                                                       **kernel_params[0],
                                                                                       kn=np.round(9),
                                                                                       ti=ti, tf=tf)
    t=2.0
    if t or not (t==None):
        if t>10:
            title+=f' at t = {t:.0f}'
        else:
            title+=f' at t = {t:2.1f}'

    print('\n\n',title)

    title = re.sub(r'(( at t = \d*\.\d*)|( at t = \d+))', '', title)
    # fldr = title.replace('at t = [*\d\.\d*]','')
    # fldr = re.sub('[*\d\.\d*]','',fldr).strip()

    print('\n\n',title, title[-1])


def filename():

    """
    index = lambda x: re.search('\.\d_*',str(x))  # t = 0.0_876896789
    truncate = lambda x: re.sub('\.\d_*','',str(x))
    filelist = [truncate(index(file)) for file in filelist]
    """


    filelist = [
            'Oscillator Phase in 0pi at t = 11_210503_211652626384.png' ,
            'Oscillator Phase in 0pi at t = 4.5_210503_211549726809.png' ,
            'Oscillator Phase in 0pi at t = 0.0_210503_211049550263.png' ,
            ]
    # print('\n',filelist[0])
    term = r' at t = \d*\.*\d*_'  # | ^[\d*_]
    date = lambda x: re.split(term,str(x),1)   # t = 1.4_20200505...
    truncate = lambda x: re.sub(term,'',x,1)

    index = np.array([date(file) for file in filelist],dtype=str)
    print('\nlamda\n',index.shape,'\n',index,'\n')

    test = index[...,-1]
    # test = np.array([truncate(file.strip()) for file in index[...,1]],dtype=str)
    print(index,'\n',test[np.newaxis].T)
    #
    # print('\nlamda\n',index.shape,'\n',index,'\n')

    # if index.shape==1:
    #     print('err 1D arry')
    #     return False

if __name__=='__main__':
    filename()

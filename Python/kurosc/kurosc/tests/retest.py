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
    term = r'\d*\.*\d*_'  # | ^[\d*_]
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

import re


def title():

    ti = 2
    tf = 7

    plot_title = 'Oscillator Phase $\in$ [${0}$,${1}$)'.format(ti,tf)
    plot_title +='at t = 99.999'
    fldr = plot_title.replace('at t = ','').replace('\d\.\d*','')
    test = re.sub('\d*\.\d*','',fldr)
    print(test)
    print(fldr)



def filename():

    """
    index = lambda x: re.search('\.\d_*',str(x))  # t = 0.0_876896789
    truncate = lambda x: re.sub('\.\d_*','',str(x))
    filelist = [truncate(index(file)) for file in filelist]
    """
    
    name = 'Oscillator Phase in 0_pi at t = 0.0_210503_143047936013.png'
    test = re


if __name__=='__main__':
    filename()

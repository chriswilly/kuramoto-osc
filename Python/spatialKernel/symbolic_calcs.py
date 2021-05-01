"""
symbolic derivation of gaussian function
to construct wavelet for distance decay
spatial kernel
"""

from sympy import (symbols,
                   diff,
                   solve,
                   expand,
                   sqrt,
                   exp)



def gaussian(x,a,b,c):
    return a*exp(-(x-b)**2/2/c**2)


def derivative(fn,n,var):
    i=0
    while i<n:
        fn = diff(fn,var)
        i+=1
    return fn



def main(n: int = 4):
    x,a,b,c = symbols('x,a,b,c')

    fn = derivative(gaussian(x,a,b,c),n,x)
    # print('Gaussian',n,'th derivative\n',fn)
    return fn

if __name__ == '__main__':
    main()

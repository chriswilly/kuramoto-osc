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
    return fn, i



def main():
    x,a,b,c = symbols('x,a,b,c')

    test, i = derivative(gaussian(x,a,b,c),0,x)
    print(test, i)


if __name__ == '__main__':
    main()

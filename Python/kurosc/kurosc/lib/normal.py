import numpy as np


def custom_dist(kernel, size=None, limits=(0.0, 120.0), oversample=10):
    """Regular normal distribution, but with hard cut-offs at the specified limits"""
    options = np.linspace(limits[0], limits[1], num=oversample * size)
    weights = kernel(options)
    probs = weights / sum(weights)
    return np.random.choice(options, size=size, replace=True, p=probs)


def normal_dist(obj, kernel,
                distance:float = 3/2,
                resolution:int = 1e6, #1mln samples
                params:dict = {'a': 1/7,
                               'b': 0,
                               'c': 1/2,
                               },     # by eye fig 2?
                )->np.ndarray:

    """construct a normal dist frequency lookup
    # can be packaged to lib but need some onject passing
    """
    x = np.linspace(0,distance,int(resolution)) # Half curve


    g = kernel.wavelet(kernel.gaussian,
                            x,*params.values(),True)

    rng = np.random.default_rng()

    p = rng.choice(g,
                   size=np.prod(obj.ic.shape),
                   replace=True
                   )
    # print('***********',p.shape,g.shape)

    #init a bool indx
    indx = np.zeros((*g.shape,*p.shape),dtype=bool)
    # print(indx.shape[1])


    indy = np.arange(*g.shape)

    for k,q in enumerate(p):
        indx[indy[g==q],k] = 1
        #return a mxn big list of frequencies matches
    # print(x[indx.any(axis=1)].shape)

    y = x[indx.any(axis=1)]  # flatten
    # create random sign by x^(0 | -1; p(0)=0.5)
    y *= (-np.ones(*y.shape))**rng.choice((0,1),size=y.shape[0])
    return y

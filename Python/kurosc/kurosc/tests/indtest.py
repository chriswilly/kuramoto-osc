

import numpy as np
np.set_printoptions(precision=3)

def ind_compare():
    x,y = np.meshgrid(np.arange(3),
                      np.arange(3),
                      sparse=False, indexing='ij')
    print('ij\nx:\n',x,'\n\ny:\n',y)

    x,y = np.meshgrid(np.arange(3),
                      np.arange(3),
                      sparse=False, indexing='xy')

    print('\nxy\nx:\n',x,'\n\ny:\n',y)


def torus(x, y, size_x, size_y):
    """
    https://stackoverflow.com/questions/62522809/\
    how-to-generate-a-numpy-manhattan-distance-array-with-torus-geometry-fast
    >>> f(x=2, y=3, size_x=8, size_y=8)
    array([[5, 4, 3, 2, 3, 4, 5, 6],
           [4, 3, 2, 1, 2, 3, 4, 5],
           [3, 2, 1, 0, 1, 2, 3, 4],
           [4, 3, 2, 1, 2, 3, 4, 5],
           [5, 4, 3, 2, 3, 4, 5, 6],
           [6, 5, 4, 3, 4, 5, 6, 7],
           [7, 6, 5, 4, 5, 6, 7, 8],
           [6, 5, 4, 3, 4, 5, 6, 7]])
    >>> f(x=1, y=1, size_x=3, size_y=3)
    array([[2, 1, 2],
           [1, 0, 1],
           [2, 1, 2]])
    """
    a, b = divmod(size_x, 2)
    # print('a,b',a,b)
    # input('...')

    x_template = np.r_[:a+b, a:0:-1] # [0 1 2 1] for size_x == 4 and [0 1 2 2 1] for size_x == 5
    x_template = np.roll(x_template, x) # for x == 2, size_x == 8: [2 1 0 1 2 3 4 3]
    print('x',x_template)
    input('...')

    a, b = divmod(size_y, 2)
    y_template = np.r_[:a+b, a:0:-1]
    y_template = np.roll(y_template, y)

    print('y',y_template)
    input('...')

    d =  np.sqrt(np.add.outer(x_template**2, y_template**2))
    return d

    # return np.sqrt(np.add.outer(x_template**2, y_template**2))
    # return np.add.outer(x_template, y_template)


if __name__ == '__main__':
    # ind_compare()
    print(torus(3,3,6,6))

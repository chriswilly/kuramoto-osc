

import numpy as np

x,y = np.meshgrid(np.arange(3),
                  np.arange(3),
                  sparse=False, indexing='ij')
print('ij\nx:\n',x,'\n\ny:\n',y)

x,y = np.meshgrid(np.arange(3),
                  np.arange(3),
                  sparse=False, indexing='xy')

print('xy\nx:\n',x,'\n\ny:\n',y)

"""
test fns
"""
import numpy as np
import pandas as pd

a = np.array([[4,8],[0,7],[9,7]])
# print(a[0].index)
p = pd.DataFrame(a)
i = p.index.to_numpy()
print(type(i),i)

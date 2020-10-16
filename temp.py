import numpy as np

a = np.array([[4,7,1,3,2], [3,2,4,2,1]])
print(a)
b = a.copy()

b.sort()

print(a)
print(b)
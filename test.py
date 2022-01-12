import numpy as np

testing = [[[0 for i in range(0, 3)] for j in range(0, 480)]
           for k in range(0, 640)]

testing = np.array(testing)
print(testing)

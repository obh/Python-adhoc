import numpy as np

out = np.random.beta( [60, 40], [40, 60])
x1 = 0
x2 = 0
for i in range(0, 10000):
    if out[0] > out[1]:
        x1+=1
    else:
        x2+=1

print(x1)
print(x2)


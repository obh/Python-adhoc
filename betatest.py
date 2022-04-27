import numpy as np

x1 = 0
x2 = 0
x3 = 0

s1 = 55
f1 = 100 - s1

s2 = 65
f2 = 100 - s2

s3 = 1
f3 = 100 - s3
for i in range(0, 10000):
    out = np.random.beta( [s1, s2, s3], [f1, f2, f3])
    if out[0] > out[1] and out[0] > out[2]:
        x1+=1
    elif out[1] > out[0] and out[1] > out[2]:
        x2+=1
    elif out[2] > out[0] and out[2] > out[1]:
        x3 += 1

print(x1)
print(x2)
print(x3)


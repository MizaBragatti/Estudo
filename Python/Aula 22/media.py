import numpy
from scipy import stats
import matplotlib.pyplot as plt

velocidades = [80, 85, 82, 87, 94, 99, 87, 88, 93, 90, 91]

# x = numpy.mean(velocidades)
# y = numpy.median(velocidades)
# z = stats.mode(velocidades)

# print(f'{x:.2f}')
# print(y)
# print(z)

speed = [86,87,88,86,87,85,86]
speed = [32,111,138,28,59,77,97]

dp = numpy.std(speed)
md  = numpy.median(speed)
var = numpy.var(speed)


print(f'{dp:.2f}',  f'{md:.2f}', f'{var:.2f}')

ages = [5,31,43,48,50,41,7,11,15,39,80,82,32,2,8,6,25,36,27,61,31]
percentil = numpy.percentile(ages, 90)

print(f'{percentil:.2f}')

# aleatorios = numpy.random.uniform(0.0, 5.0, 100000)
# plt.hist(aleatorios, 100)
# plt.show()

distNormal = numpy.random.normal(5.0, 1.0, 100000)
plt.hist(distNormal, 100)
plt.show()
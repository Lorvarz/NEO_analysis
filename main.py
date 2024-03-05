from modules import *
import matplotlib.pyplot as plt
import numpy as np

opGain = 1e10
capacitance = 1e-9
resistance = 1e9

p1 = 0.5
f1 = 2
mag1 = 2

p2 = 0.3
f2 = 3
mag2 = 1.5

s1 = signal.fromPolar(mag1, f1, p1)
s2 = signal.fromPolar(mag2, f2, p2)
original = s1 + s2

differ = Differentiator(opGain, capacitance, resistance)
subber = Subtractor(opGain)
multer = Multiplier()

firstDer = differ(s1)
secondDer = differ(firstDer)

firstSquared = multer(s1, s1)

zeroWithSecond = multer(s1, secondDer)

final = subber(firstSquared, zeroWithSecond)
print(final)

x = np.linspace(0, 2*pi, 1000)



fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(x, [original(t) for t in x], color='blue', label="input")
ax1.set_ylabel('Original')

ax2.plot(x, [final(t) for t in x], color='red', label="output")
ax2.set_ylabel('Final')
ax2.set_xlabel('x')

plt.show()














# subtracted = lambda t: mag1 * cos(f1*t + p1) - mag2 * cos(f2*t + p2)
# derivatated = lambda t: -mag1 * f1 * sin(f1*t + p1) 
# multiplied = lambda t: mag1 * mag2 * cos(f1*t + p1) * cos(f2*t + p2)

# differ = Differentiator(opGain, capacitance, resistance)
# subber = Subtractor(opGain)


# s1 = signal.fromPolar(mag1, f1, p1)
# s2 = signal.fromPolar(mag2, f2, p2)
# subbed = subber(s1, s2)
# diffed = differ(s1)
# multed = s1 * s2

# x = np.linspace(0, 2*pi, 1000)

# # plt.plot(x, [subtracted(t) for t in x], color='blue', label = "input")
# # plt.plot(x, [subbed(t) for t in x], color='red', label="output")

# # plt.plot(x, [derivatated(t) for t in x], color='blue', label = "input")
# # plt.plot(x, [diffed(t) for t in x], color='red', label="output")

# plt.plot(x, [multiplied(t) for t in x], color='blue', label = "input")
# plt.plot(x, [multed(t) for t in x], color='red', label="output")


plt.legend()
plt.show()
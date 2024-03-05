import cmath
from dataclasses import dataclass
from typing import Any
from math import pi, cos, sin
from copy import deepcopy


class signal():

    def __init__(self, real, imaginary, frequency) -> None:
        self.val = complex(real, imaginary)
        self.frequency = frequency
    
    @staticmethod
    def fromComplex(val, frequency):
        return signal(val.real, val.imag, frequency)
    
    @staticmethod
    def fromPolar(magnitude, frequency, phase = 0):
        return signal(magnitude * cos(phase), magnitude * sin(phase), frequency)

    @property
    def mag(self):
        return abs(self.val)

    @property
    def phase(self):
        return cmath.phase(self.val)

    def __add__(self, other):
        if isinstance(other, signal):
            if self.frequency == other.frequency:
                return signal.fromComplex(self.val + other.val, self.frequency)
            else:
                return composedSignal([self, other])
        else:
            return signal.fromComplex(self.val + other, self.frequency)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, signal):
            return self.mag * other.mag * 0.5 * composedSignal([signal.fromPolar(1, self.frequency + other.frequency, self.phase + other.phase), \
                                                                signal.fromPolar(1, self.frequency - other.frequency, self.phase - other.phase)])
        else:
            return signal.fromComplex(self.val * other, self.frequency)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self * (1/other)
    
    def __neg__(self):
        return signal.fromComplex(-self.val, self.frequency)

    def __repr__(self) -> str:
        return f"{self.val}|{self.frequency:.2f}Rad/s"

    def __call__(self, t : float) -> Any:
        return abs(self.val) * cos(self.frequency*t + cmath.phase(self.val))

class composedSignal():

    def __init__(self, signals) -> None:
        self.signals = signals
    
    def __add__(self, other):
        copy = composedSignal(deepcopy(self.signals))

        if isinstance(other, int) or isinstance(other, float):
            other = signal(other, 0, 0)

        if isinstance(other, signal):
            for i in range(len(copy.signals)):
                if copy.signals[i].frequency == other.frequency:
                    copy.signals[i] += other
                    return copy
            copy.signals.append(other)
            return copy
        
        if isinstance(other, composedSignal):
            for s in other.signals:
                copy += s
            return copy
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self.__add__(other)

    def __mul__(self, other):
        assert (isinstance(other, int) or isinstance(other, float)), f"multiplication with {type(other)} not supported for {type(self)}"
        return composedSignal([s * other for s in self.signals])

    def __truediv__(self, other):
        assert (isinstance(other, int) or isinstance(other, float)), f"division with {type(other)} not supported for {type(self)}"
        return composedSignal([s / other for s in self.signals])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return composedSignal([-s for s in self.signals])

    def __call__(self, t : float) -> Any:
        return sum([s(t) for s in self.signals])

    def __repr__(self) -> str:
        final = ""
        for s in self.signals:
            final += f"{s}\n"
        return final
    
class Differentiator():

    def __init__(self, opGain, capacitance, resistance) -> None:
        self.opGain = opGain
        self.capacitance = capacitance
        self.resistance = resistance
    
    def __call__(self, input):
        if isinstance(input, signal):
            return input * complex((input.frequency**2 * self.capacitance**2 * self.opGain * self.resistance**2) \
                                / (self.resistance**2 * input.frequency**2 * self.capacitance**2 + self.opGain**2), \
                                -(input.frequency * self.capacitance * self.opGain**2 * self.resistance) \
                                / (self.resistance**2 * input.frequency**2 * self.capacitance**2 + self.opGain**2))
        if isinstance(input, composedSignal):
            return composedSignal([self.__call__(s) for s in input.signals])

class Subtractor():

    def __init__(self, opGain, Vss = 0) -> None:
        self.opGain = opGain
        self.Vss = Vss
    
    def __call__(self, posInput, negInput):
        return (posInput - negInput + self.Vss) / (1 + 2/self.opGain)
    
class Multiplier():

    def __init__(self) -> None:
        pass

    def __call__(self, input1, input2):
        return input1 * input2
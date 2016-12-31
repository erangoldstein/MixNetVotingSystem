import tinyec.ec as ec
import tinyec.registry as reg
from group import *
from copy import deepcopy
import pdb


class EllipticCurveGroup(MultiplicativeGroup):

    def __init__(self, g, q):
        self._g = g
        self._q = q

    # returns (p,q,g) such as p,q large primes p = 2q+1
    def generate(self):
        raise NotImplementedError()


class EllipticCurvePoint(MultiplicativeGroupItem):

    def __init__(self, **kwargs):
        if kwargs.has_key('point') and (type(kwargs['point']) is ec.Point or type(kwargs['point']) is ec.Inf):
            self._ec_point = deepcopy(kwargs['point'])
        elif kwargs.has_key('curve_name') and kwargs.has_key('x_coord') and kwargs.has_key('y_coord'):
            self._ec_point = ec.Point(reg.get_curve(kwargs['curve_name']), kwargs['x_coord'], kwargs['y_coord'])
        else:
            raise NotImplementedError("Unexpected input at point initialization")

    # Returns the multiplication of (self * other) mod q
    def plus(self, other):
        assert type(other) is EllipticCurvePoint, "parameter given is not an Elliptic Curve Point!"
        assert self._ec_point.curve.name == other._ec_point.curve.name, "Points are not on the same curve"

        return EllipticCurvePoint(point=self._ec_point + other._ec_point)

    def scalar_multiply(self, s):
        return EllipticCurvePoint(point=self._ec_point * s)

    def inverse(self):
        return EllipticCurvePoint(point=self._ec_point * -1)

    def __eq__(self, other):
        return self._ec_point == other._ec_point

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self._ec_point.__str__()

    def __repr__(self):
        return self._ec_point.__repr__()
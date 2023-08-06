from numpy import linspace, arange
from numpy.random import normal
import uuid


def np_linspace(args):
    return list(linspace(*args))


def np_arange(args):
    return list(arange(*args))


def np_normal(args):
    return list(normal(*args))

def int_(arg):
    return int(arg)

def round_(arg):
    return round(arg)


def uid(*args):
    return uuid.uuid1()

from enum import Enum


class D_Value(Enum):
    """
    The D_Value class represents the D value of a gate {0,1,D,D',x}.
    """

    ZERO = [0, 0]
    ONE = [1, 1]
    D = [1, 0]
    D_PRIME = [0, 1]
    X = ["X", "X"]

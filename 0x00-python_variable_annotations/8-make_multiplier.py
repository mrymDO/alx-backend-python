#!/usr/bin/env python3
"""Create a multiplier function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """multiplier function"""
    def multiplier_function(x: float) -> float:
        """function that multiplies a float by a multiplier"""
        return x * multiplier

    return multiplier_function

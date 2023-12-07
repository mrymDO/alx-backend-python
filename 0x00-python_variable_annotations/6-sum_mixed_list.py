#!/usr/bin/env python3
"""sum of a mixed lit of float and integer"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sum of a mixed lit of float and integer"""
    return sum(mxd_lst)

#!/usr/bin/env python3
"""duck type"""
from typing import Iterable, Tuple, List, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Calculate the length of each element in the input list"""
    return [(i, len(i)) for i in lst]

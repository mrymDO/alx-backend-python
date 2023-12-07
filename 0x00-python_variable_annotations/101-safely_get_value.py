#!/usr/bin/env python3
"""type annotations"""
from typing import TypeVar, Mapping, Any, Union, Optional

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Optional[T] = None) -> Union[Any, T]:
    """retrieve a value from a dictionary"""
    if key in dct:
        return dct[key]
    else:
        return default

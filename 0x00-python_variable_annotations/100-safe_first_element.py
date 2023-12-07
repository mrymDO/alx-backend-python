#!/usr/bin/env python3
"""Duck typing"""
from typing import Sequence, Optional, Any


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """retrieve the first element of a sequence"""
    if lst:
        return lst[0]
    else:
        return None

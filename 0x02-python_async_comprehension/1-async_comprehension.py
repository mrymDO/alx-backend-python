#!/usr/bin/env python3
"""Async Comprehension"""

import asyncio
from typing import Generator, List


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """async comprenhension"""
    result = [value async for value in async_generator()]
    return result

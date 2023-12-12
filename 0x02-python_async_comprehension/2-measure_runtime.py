#!/usr/bin/env python3
"""run time for parallel comprehension"""

import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure runtime"""
    start_time = asyncio.get_event_loop().time()

    await asyncio.gather(
            async_comprehension(),
            async_comprehension(),
            async_comprehension(),
            async_comprehension()
    )
    end_time = asyncio.get_event_loop().time()

    return end_time - start_time

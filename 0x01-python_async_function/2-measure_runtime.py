#!/usr/bin/env python3
"""measure time"""
import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time_async(n: int, max_delay: int = 10) -> float:
    """measure time"""
    start_time = time.time()

    await wait_n(n, max_delay)

    end_time = time.time()

    total_time = end_time - start_time

    return total_time / n


def measure_time(n: int, max_delay: int = 10) -> float:
    """run the asynchronous function"""
    return asyncio.run(measure_time_async(n, max_delay))

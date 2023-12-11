#!/usr/bin/env python3
"""execute multiple coroutines"""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> list:
    """execute multiple coroutines at the same time"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = []

    for coroutine in asyncio.as_completed(tasks):
        delay = await coroutine
        delays.append(delay)
    return delays

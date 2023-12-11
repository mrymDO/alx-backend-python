#!/usr/bin/env python3
"""Execuute multiple coroutines"""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """Execuute multiple coroutines"""
    asks = [wait_random(max_delay) for _ in range(n)]
    delays = []

    for coroutine in asyncio.as_completed(tasks):
        delay = await coroutine
        delays.append(delay)

    return delays

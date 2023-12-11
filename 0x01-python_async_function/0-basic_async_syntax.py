#!/usr/bin/env python3
"""basic async syntax"""
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """Asynchronous coroutine that waits for a random delay"""
    random_delay = random.uniform(0, max_delay)
    await asyncio.sleep(random_delay)
    return random_delay

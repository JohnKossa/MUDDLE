import asyncio
import inspect


def async_to_sync(func, loop=None, *args, **kwargs):
    if not inspect.iscoroutine(func):
        print("Attempted to sync an already sync function")
        return func(*args, **kwargs)
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_until_complete(func(*args, **kwargs))


async def sync_to_async(func, loop=None, *args, **kwargs):
    if inspect.iscoroutine(func):
        print("Attempted to async an already async function")
        return await func(*args, **kwargs)
    if loop is None:
        loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)

import asyncio
import logging
from typing import (
    Awaitable
)

from config import (
    log_verbose, logger
)


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    try:
        # 挂起当前协程,直到异步函数完成操作
        await fn
    except Exception as e:
        logging.exception(e)
        msg = f"Caught exception: {e}"
        logger.error(f"{e.__class__.__name__}: {msg}",
                     exc_info=e if log_verbose else False)
    finally:
        # 通知其他等待的协程
        event.set()

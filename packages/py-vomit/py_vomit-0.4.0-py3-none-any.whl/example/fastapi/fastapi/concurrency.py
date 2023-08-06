from contextlib import AsyncExitStack as AsyncExitStack
from contextlib import asynccontextmanager as asynccontextmanager
from typing import AsyncGenerator, ContextManager, TypeVar
import anyio
from anyio import CapacityLimiter
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool
from starlette.concurrency import run_in_threadpool as run_in_threadpool
from starlette.concurrency import run_until_first_complete as run_until_first_complete
_T = TypeVar('_T')

@asynccontextmanager
async def contextmanager_in_threadpool(cm: ContextManager[_T]) -> AsyncGenerator[_T, None]:
    exit_limiter = CapacityLimiter(1)
    try:
        yield (await run_in_threadpool(cm.__enter__))
    except Exception as e:
        ok = bool(await anyio.to_thread.run_sync(cm.__exit__, type(e), e, None, limiter=exit_limiter))
        if not ok:
            raise e
    else:
        await anyio.to_thread.run_sync(cm.__exit__, None, None, None, limiter=exit_limiter)
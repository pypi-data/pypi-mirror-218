import os
from contextvars import ContextVar
from typing import Optional, TYPE_CHECKING

from codebox.config import settings
from codebox.utils import set_api_key
from codebox.codebox import CodeBox

if TYPE_CHECKING:
    from aiohttp import ClientSession


aiosession: ContextVar[Optional["ClientSession"]] = ContextVar(
    "aiohttp-session", default=None
)


__all__ = [
    "CodeBox", 
    "set_api_key", 
    "settings",
    "aiosession"
]
import importlib.metadata

from .fields import Field
from .routing import APIRouter

__version__ = importlib.metadata.version("universi")
__all__ = ["Field", "APIRouter"]

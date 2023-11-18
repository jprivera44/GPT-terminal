"""Data classes."""

from dataclasses import dataclass
from typing import Optional



@dataclass
class BackendResponse:
    """Response data returned from a model."""

    completion: str
    completion_time_sec: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int



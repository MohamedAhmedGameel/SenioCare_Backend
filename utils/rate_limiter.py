import time
import asyncio
from fastapi import Request, HTTPException, status

class RateLimiter:
    def __init__(self, rate_limit: int = 30, time_window: int = 1):
        """
        Simple in-memory token bucket rate limiter.
        :param rate_limit: Number of requests allowed per time_window.
        :param time_window: Time window in seconds.
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.tokens = rate_limit
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()

    async def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        
        # Calculate tokens to add
        tokens_to_add = elapsed * (self.rate_limit / self.time_window)
        
        if tokens_to_add >= 1:
            self.tokens = min(self.rate_limit, self.tokens + tokens_to_add)
            self.last_refill = now

    async def check(self):
        async with self.lock:
            await self._refill()
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False

# Global instance for 30 ops/second (less than 33)
global_rate_limiter = RateLimiter(rate_limit=30, time_window=1)

async def rate_limit_dependency(request: Request):
    """
    Dependency to be used in routes or globally.
    """
    allowed = await global_rate_limiter.check()
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

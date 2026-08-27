"""Simple in-memory rate limiter middleware (per-IP token bucket).

Architecture point: swap for Redis-backed limiter in multi-instance production.
"""
import time
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max = max_requests
        self.window = window_seconds
        self._hits: dict = defaultdict(deque)

    async def dispatch(self, request, call_next):
        # exempt health/docs
        path = request.url.path
        if path.startswith(("/api/health", "/docs", "/openapi.json", "/redoc")):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        bucket = self._hits[client_ip]
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()
        if len(bucket) >= self.max:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please slow down."},
                headers={"Retry-After": str(self.window)},
            )
        bucket.append(now)
        return await call_next(request)

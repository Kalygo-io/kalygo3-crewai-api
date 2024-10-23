from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from .routers import (
  hierarchicalHaitianNewsCrew,
  healthcheck
)

import debugpy

load_dotenv()

# debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

app = FastAPI(docs_url=None, redoc_url=None)

origins = [
    "http://127.0.0.1:3000",
    "https://kalygo.io"
]

# origins = [ "*" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Limiter instance
limiter = Limiter(key_func=get_remote_address)

# Add SlowAPI middleware to FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(healthcheck.router, prefix="")

app.include_router(
    hierarchicalHaitianNewsCrew.router,
    prefix="/api/hierarchical-haitian-news-crew",
    tags=['hierarchical-haitian-news-crew'],
)

# Handle preflight requests explicitly
@app.options("/")
async def options_handler():
    return {"status": "OK"}

import asyncio
import logging
from contextlib import asynccontextmanager

import httpx
import requests
import uvicorn
from fastapi import FastAPI

from config.config import Config
from routers import DataService, BlockchainService
from utility.RequestHandler import GET, POST

app = FastAPI()
app.include_router(DataService.router)
app.include_router(BlockchainService.router)

@app.get("/")
async def root():
    return {"message": "NODE API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_config="log_conf.yaml")
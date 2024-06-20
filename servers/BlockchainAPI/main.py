import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import ContractService

app = FastAPI()

app.include_router(ContractService.router)




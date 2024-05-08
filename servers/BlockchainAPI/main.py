import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import ContractService
from utility.Contract import listen

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen())

app.include_router(ContractService.router)




import uvicorn
from fastapi import FastAPI
from routers import DataService, BlockchainService

app = FastAPI()
app.include_router(DataService.router)
app.include_router(BlockchainService.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_config="log_conf.yaml")
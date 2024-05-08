from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from utility.RequestHandler import GET, POST
from config.config import Config
import json
import logging
import psycopg2

router = APIRouter(
    prefix="",
    tags=["Blockchain-Service"],
    responses={404: {"description": "Not found"}}
)

logger = logging.getLogger(__name__)
event_buffer = {}

@router.post('/start-contract', tags=['contract'])
async def start_contract(request: Request):
    try:
        if request.method == 'POST':
            body = await request.json()
            print(body)

            response = POST(Config.BLOCKCHAIN_API + "/start-contract", body)
            print(response)

            if response["status"] == "revert":
                logging.error(response["URL"])
                return JSONResponse(
                    status_code=406,
                    content={
                        "message": (f"{response['message']}")
                    },
                )
            else:
                return JSONResponse(
                    status_code=202,
                    content={
                        "status": (f"{response['status']}")
                    },
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/contract-fulfilment/{id}', tags=['contract'])
async def get_contract_fulfilment(id):
    try:
        response = GET(Config.BLOCKCHAIN_API + f"/contract-fulfilment/{id}")
        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/contract-trail/{id}', tags=['contract'])
def get_contract_trail(id):
    try:
        response = GET(Config.BLOCKCHAIN_API + f"/contract-trail/{id}")
        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/contract-data/{id}', tags=['contract'])
async def get_contract_data(id: int):
    try:
        response = GET(Config.BLOCKCHAIN_API + f"/contract-data/{id}")
        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post('/deliver/{id}', tags=['contract'])
async def next_destination(request: Request, id):
    if request.method == 'POST':
        try:
            body = await request.json()

            response = POST(Config.BLOCKCHAIN_API + f"/handover/{id}", body)

            if response["status"] == "revert":
                logging.error(response["URL"])
                return JSONResponse(
                    status_code=406,
                    content={
                        "message": f"{response['message']}"
                    },
                )
            else:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": f"{response['status']}"
                    },
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@router.post('/receive/{id}', tags=['contract'])
async def receive_product(request: Request, id: int):
    if request.method == 'POST':
        try:
            body = await request.json()
            response = POST(Config.BLOCKCHAIN_API + f"/receive/{id}", body)

            if response["status"] == "revert":
                logging.error(response["URL"])
                return JSONResponse(
                    status_code=406,
                    content={
                        "message": f"{response['message']}"
                    },
                )
            else:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": f"{response['status']}"
                    },
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@router.post('/end-contract/{id}', tags=['contract'])
async def end_agreement(request: Request, id):
    if request.method == 'POST':
        try:
            body = await request.json()
            response = POST(Config.BLOCKCHAIN_API + f"/end-contract/{id}", body)

            if response["status"] == "revert":
                logging.error(response["URL"])
                return JSONResponse(
                    status_code=406,
                    content={
                        "message": f"{response['message']}"
                    },
                )
            else:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": f"{response['status']}"
                    },
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@router.post('/events', tags=['contract'])
async def events(request: Request):
    if request.method == 'POST':
        try:
            body = await request.json()
            event_buffer[body["new_holder"]] = body["agreement_id"]
            logger.info(f"Transfer events: {event_buffer}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@router.get('/events', tags=['contract'])
async def events(request: Request):
    if request.method == 'GET':
        try:
            return JSONResponse(
                status_code=200,
                content=event_buffer
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)

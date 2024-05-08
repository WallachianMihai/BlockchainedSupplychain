from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config.config import Config
from utility.Contract import web3, contract, process_receipt
from web3.exceptions import ContractLogicError, ContractCustomError, ContractPanicError
from utility.ContractPDF import PDFHandler
import logging
import psycopg2

router = APIRouter(
    prefix="",
    tags=["contract"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

@router.post('/start-contract', tags=['contract'])
async def start_contract(request: Request):
    try:
        if request.method == 'POST':
            body = await request.json()
            account_seller: str = body["account_seller"]
            account_client: str = body["account_client"]
            seller = body["seller"]
            client = body["client"]
            product_id = body["product_id"]
            product = body["product"]
            quantity = body["quantity"]
            logger.debug(f"seller: {seller}, client: {client}, account_seller: {account_seller}, account_client: {account_client}, product: {product}, quantity: {quantity}")

            conn = psycopg2.connect(Config.CONNECTION_STRING)
            cur = conn.cursor()

            sql_for_count = f"SELECT \"supply_chain\".get_contract_count();"
            cur.execute(sql_for_count)
            count = cur.fetchone()[0]
            cur.close()
            conn.close()

            logger.debug(f"contract count: {count}")

            PDF_URI, hash = PDFHandler.generate_contract_pdf(product, product_id, seller, client, quantity, count)

            conn = psycopg2.connect(Config.CONNECTION_STRING)
            cur = conn.cursor()

            sql = f"SELECT \"supply_chain\".insert_contract_and_return_id({product_id}, '{account_client}', {quantity}, '{PDF_URI}', '{account_seller}');"

            cur.execute(sql)
            id = cur.fetchone()[0]

            tx_hash = contract.functions.startAgreement(id, account_client, product, quantity, str(hash)).transact({'from': account_seller})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            logger.info(f"Transaction receipt: {receipt}")

            process_receipt(tx_receipt=receipt)

            if receipt.status == 1:
                conn.commit()
            cur.close()
            conn.close()

            return JSONResponse(
                status_code=200,
                content={
                    "status": ("OK")
                },
            )
    except Exception as e:
        if isinstance(e, ContractLogicError):
            revert = e.message.split(',')[0]
            message = revert[revert.rfind(":"):]
            message = message[2:]
            return JSONResponse(
                status_code=406,
                content={
                    "URL": (f"Failed method {request.method} at URL {request.url}."),
                    "message": (f"{message}"),
                    "status": ("revert")
                },
            )
        elif isinstance(e, ContractPanicError):
            revert = e.message.split(',')[0]
            message = revert[revert.rfind(":"):]
            message = message[2:]
            return JSONResponse(
                status_code=406,
                content={
                    "URL": (f"Failed method {request.method} at URL {request.url}."),
                    "message": (f"{message}"),
                    "status": ("revert")
                },
            )
        elif isinstance(e, ContractCustomError):
            revert = e.message.split(',')[0]
            message = revert[revert.rfind(":"):]
            message = message[2:]
            return JSONResponse(
                status_code=406,
                content={
                    "URL": (f"Failed method {request.method} at URL {request.url}."),
                    "message": (f"{message}"),
                    "status": ("revert")

                },
            )
        else:
            raise HTTPException(status_code=500, detail=e)


@router.get('/contract-fulfilment/{id}', tags=['contract'])
async def get_contract_fulfilment(id: int):
    try:
        result = contract.functions.getContractFulfilment(id).call()
        fulfilment = {"client": result[0], "seller": result[1]}
        logger.info(f"Fulfilment on contract {id}: {fulfilment}")

        return fulfilment

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/contract-trail/{id}', tags=['contract'])
async def get_contract_trail(id: int):
    try:
        result = contract.functions.getTrailHistory(id).call()

        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = f"SELECT account, name from \"supply_chain\".\"Customer\""

        cur.execute(sql)
        data = cur.fetchall()

        idx = -1
        trail = [{idx + 1: row[1]} for row in data if row[0] in result]

        cur.close()
        conn.close()

        logger.info(f"Trail of contract {id}: {trail}")

        return JSONResponse(content=trail)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/contract-data/{id}', tags=['contract'])
async def get_contract_data(id: int):
    try:
        result = contract.functions.getAgreementData(id).call()
        data = {
            "seller": result[0],
            "holder": result[1],
            "next_holder": result[2],
            "client": result[3],
            "product": result[4],
            "quantity": result[5]
        }

        logger.info(f"Contract data {id}: {data}")
        return JSONResponse(content=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.post('/handover/{id}', tags=['contract'])
async def next_destination(id: int, request: Request):
    if request.method == 'POST':
        try:
            body = await request.json()
            from_address: str = body["from"]
            to_address: str = body["to"]
            logger.info(f"from: {from_address}; to: {to_address}")

            tx_hash = contract.functions.nextDestination(id, to_address).transact({'from': from_address})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            process_receipt(tx_receipt=receipt)

            return JSONResponse(
                status_code=200,
                content={
                    "status": ("OK")
                },
            )
        except Exception as e:
            if isinstance(e, ContractLogicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractPanicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractCustomError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            else:
                raise HTTPException(status_code=500, detail=e)


@router.post('/receive/{id}', tags=['contract'])
async def receive_product(id: int, request: Request):
    if request.method == 'POST':
        try:
            body = await request.json()
            new_holder: str = body["from"]
            logger.info(f"from: {new_holder}")

            tx_hash = contract.functions.receiveProduct(id).transact({'from': new_holder})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            process_receipt(tx_receipt=receipt)

            return JSONResponse(
                status_code=200,
                content={
                    "status": ("OK")
                },
            )
        except Exception as e:
            if isinstance(e, ContractLogicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractPanicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractCustomError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            else:
                raise HTTPException(status_code=500, detail=e)



@router.post('/end-contract/{id}', tags=["contract"])
async def end_agreement(id: int, request: Request):
    if request.method == 'POST':
        try:
            body = await request.json()
            account = body["account"]

            tx_hash = contract.functions.endAgreement(id).transact(
                {'from': account, 'value': web3.to_wei(1, 'ether')})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            process_receipt(tx_receipt=receipt)

            logger.info(f"Agreement with id: {id} has ended.")
            return JSONResponse(
                status_code=200,
                content={
                    "status": ("OK")
                },
            )
        except Exception as e:
            if isinstance(e, ContractLogicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractPanicError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            elif isinstance(e, ContractCustomError):
                revert = e.message.split(',')[0]
                message = revert[revert.rfind(":"):]
                message = message[2:]
                return JSONResponse(
                    status_code=406,
                    content={
                        "URL": (f"Failed method {request.method} at URL {request.url}."),
                        "message": (f"{message}"),
                        "status": ("revert")
                    },
                )
            else:
                raise HTTPException(status_code=500, detail=e)

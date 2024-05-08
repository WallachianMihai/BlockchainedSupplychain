import asyncio, requests, json
from web3 import Web3
from config.config import Config
import logging
from fastapi import HTTPException

web3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
contract = web3.eth.contract(address=Config.PUBLIC_KEY, abi=Config.ABI)

logger = logging.getLogger(__name__)


def handle_event(event):
    event_json = web3.to_json(event)
    logger.info(f"Event: {event_json}")
    data = json.loads(event_json)

    body = {
            "holder": data["args"]["holder"],
            "new_holder": data["args"]["new_holder"],
            "agreement_id": data["args"]["agreement_id"]
    }
    response = requests.post(url=Config.CLIENT + "/events", json=body).json()


async def listen():
    while True:
        event_filter = contract.events.transferProduct.create_filter(fromBlock='latest')
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(5)


def process_receipt(tx_receipt):
    if tx_receipt.status == 0:
        logs = contract.events.Revert().processReceipt(tx_receipt)

        revert_messages = ""
        for log in logs:
            revert_messages += log['args']['message'] + "; "

        logger.info(revert_messages)
        raise HTTPException(status_code=406, detail=revert_messages)
    else:
        logger.info(f"Transaction successful: {tx_receipt.transactionHash}")
        logger.info(f"Transaction info: block number: {tx_receipt.blockNumber}; "
                    f"Gas used: {tx_receipt.gasUsed};")

        logger.info(f"transaction logs: {tx_receipt.logs}")

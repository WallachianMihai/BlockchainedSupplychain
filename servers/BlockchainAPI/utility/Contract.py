import json
import httpx
from web3 import Web3
from config.config import Config
import logging
from fastapi import HTTPException

web3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
contract = web3.eth.contract(address=Config.PUBLIC_KEY, abi=Config.ABI)

logger = logging.getLogger(__name__)


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

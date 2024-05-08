import asyncio
import psycopg2
from web3 import Web3
import os
import json

# anvil_url = "http://127.0.0.1:8545"
# web3 = Web3(Web3.HTTPProvider(anvil_url))
#
# contract_abi = [{"type":"function","name":"endAgreement","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"payable"},{"type":"function","name":"getAgreementData","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"address","internalType":"address"},{"name":"","type":"address","internalType":"address"},{"name":"","type":"address","internalType":"address"},{"name":"","type":"address","internalType":"address"},{"name":"","type":"string","internalType":"string"},{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"getContractFulfilment","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"},{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"function","name":"getTrailHistory","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"address[]","internalType":"address[]"}],"stateMutability":"view"},{"type":"function","name":"nextDestination","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"},{"name":"account","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"receiveProduct","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"startAgreement","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"},{"name":"account","type":"address","internalType":"address"},{"name":"product","type":"string","internalType":"string"},{"name":"quantity","type":"uint256","internalType":"uint256"},{"name":"contract_hash","type":"string","internalType":"string"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"verifyContract","inputs":[{"name":"agreement_id","type":"uint256","internalType":"uint256"},{"name":"hash","type":"string","internalType":"string"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"event","name":"transferProduct","inputs":[{"name":"holder","type":"address","indexed":True,"internalType":"address"},{"name":"new_holder","type":"address","indexed":True,"internalType":"address"}],"anonymous":False}]
#
# contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
#
# contract = web3.eth.contract(address=contract_address, abi=contract_abi)
#
# def handle_event(event):
#     print(Web3.to_json(event))
#
# async def log_loop(event_filter, poll_interval):
#     while True:
#         for PairCreated in event_filter.get_new_entries():
#             handle_event(PairCreated)
#         await asyncio.sleep(poll_interval)
#
# def start_listening():
#     event_filter = contract.events.transferProduct.create_filter(fromBlock='latest')
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(
#             asyncio.gather(
#                 log_loop(event_filter, 2)))
#     finally:
#         # close loop to free up system resources
#         loop.close()
#
# start_listening()

# Call a function
# result = contract.functions.getContractFulfilment(5).call()
# print(result)

# Send a transaction to a function (requires an unlocked account)
# try:
#     tx_hash = contract.functions.nextDestination(6, "0x70997970C51812dc3A010C7d01b50e0d17dc79C8").transact({'from': "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"})
# except Exception as e:
#     print(type(e))
#     print(e)
#
# # Wait for the transaction to be mined
# receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
# print(receipt)


event = '{"args": {"holder": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8", "new_holder": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC", "agreement_id": 16}, "event": "transferProduct", "logIndex": 0, "transactionIndex": 0, "transactionHash": "0xa5bae5961728133d0f07d291ff9255e14510733305f7f98de239292fbdfb99ef", "address": "0x5FbDB2315678afecb367f032d93F642f64180aa3", "blockHash": "0x37e86f80cdcde67c91637e7c82a2954b6992ae1c48b2d36567bc78db4cc3e6ce", "blockNumber": 3}'
data = json.loads(event)
print(data["args"]["holder"])
print( data["args"]["new_holder"])
print(data["args"]["agreement_id"])


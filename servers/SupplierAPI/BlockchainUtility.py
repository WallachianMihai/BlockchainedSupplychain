import web3
from web3 import Web3
from config import Config

web3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
contract = web3.eth.contract(address=Config.PUBLIC_KEY, abi=Config.ABI)


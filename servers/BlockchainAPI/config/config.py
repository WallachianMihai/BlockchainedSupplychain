import json
import os
import logging

logger = logging.getLogger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, "anvil_config.json"), 'r') as j:
    data = json.loads(j.read())
    conn_string = f"dbname={data['name']} user={data['user']} password={data['password']} host={data['host']} port={data['port']}"
    print(conn_string)
    url = data['rpc-url']
    client = data['client']
    contract_abi = data['ABI']

with open(os.path.join(basedir, ".secret")) as p:
    public_key = p.readline()[:-1]
    private_key = p.readline()[:-1]

class Config:
    NAME = "BlockchainAPI"
    BASE_DIR = basedir
    PRIVATE_KEY = private_key
    PUBLIC_KEY = public_key
    CONNECTION_STRING = conn_string
    RPC_URL = url
    CLIENT = client
    ABI = contract_abi

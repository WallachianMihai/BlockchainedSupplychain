import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, "static/anvil_config.json"), 'r') as j:
    data = json.loads(j.read())
    conn_string = f"dbname={data['name']} user={data['user']} password={data['password']} host={data['host']} port={data['port']}"
    url = data['rpc-url']
    contract_abi = data['ABI']

with open(os.path.join(basedir, "static/.secret"), 'r') as p:
    public_key = p.readline()
    private_key = p.readline()

class Config:
    NAME = "ServiceAPI"
    BASE_DIR = basedir
    PRIVATE_KEY = private_key
    PUBLIC_KEY = public_key
    CONNECTION_STRING = conn_string
    RPC_URL = url
    ABI = contract_abi

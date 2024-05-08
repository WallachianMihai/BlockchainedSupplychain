import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, "config.json"), 'r') as j:
    data = json.loads(j.read())
    conn_string = f"dbname={data['name']} user={data['user']} password={data['password']} host={data['host']} port={data['port']}"
    blockchain_api = data['blockchain-service']

with open(os.path.join(basedir, ".secret")) as p:
    public_key = p.readline()

class Config:
    NAME = "Node"
    BASE_DIR = basedir
    CONNECTION_STRING = conn_string
    BLOCKCHAIN_API = blockchain_api
    ACCOUNT = public_key

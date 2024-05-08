import os.path
import json
from flask import Flask, jsonify

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, "static/config.json"), 'r') as j:
    data = json.loads(j.read())
    conn_string = f"dbname={data['name']} user={data['user']} password={data['password']} host={data['host']} port={data['port']}"

@app.route('/start-contract', methods = ['POST'])
def startContract(request):
    if request.method == 'POST':
        id = request.form.get("contract_id")
        account = request.form
    else:
        return 405

@app.route('/')
def default():  # put application's code here
    return 'Blockchained supply chain'


if __name__ == '__main__':
    app.run()
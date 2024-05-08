from flask import Flask, jsonify
from fpdf import FPDF
from datetime import date
from Crypto.Hash import keccak
import psycopg2
from config import Config
from BlockchainUtility import web3, contract

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def test_page():
        return '<h1>Supply chain services</h1>'

    return app

app = create_app()

@app.route("/products", methods=["GET"])
def get_products():
    try:
        # Connect to the database
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        # Define your product query
        sql = "SELECT id, name, description, price FROM \"supply_chain\".\"Product\""
        cur.execute(sql)

        # Fetch data as list of dictionaries
        data = cur.fetchall()
        print(data)
        products = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3]
            }
            for row in data
        ]

        # Close connection
        cur.close()
        conn.close()

        # Return data as JSON
        return jsonify(products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers", methods=["GET"])
def get_customers():
    try:
        # Connect to the database
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        # Define your customer query
        sql = "SELECT id, name, location FROM \"supply_chain\".\"Customer\""
        cur.execute(sql)

        # Fetch data as list of dictionaries
        data = cur.fetchall()
        customers = [
            {
                "id": row[0],
                "name": row[1],
                "location": row[2],
            }
            for row in data
        ]

        # Close connection
        cur.close()
        conn.close()

        # Return data as JSON
        return jsonify(customers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/inventory", methods=["GET"])
def get_inventory():
    try:
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = """
        SELECT id, product_id, quantity from \"supply_chain\".\"Inventory\";
        """

        cur.execute(sql)

        data = cur.fetchall()
        inventory = [
            {
                "id": row[0],
                "product_id": row[1],
                "quantity": row[2],
            }
            for row in data
        ]

        cur.close()
        conn.close()

        return jsonify(inventory)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/contracts", methods=["GET"])
def get_contracts():
    try:
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = "SELECT id, product_id, customer_id, quantity, contract_path FROM \"supply_chain\".\"Contract\";"

        cur.execute(sql)

        data = cur.fetchall()
        contracts = [
            {
                "id": row[0],
                "product_id": row[1],
                "customer_id": row[2],
                "quantity": row[3],
                "contract_path": row[4],
            }
            for row in data
        ]

        # Close connection
        cur.close()
        conn.close()

        # Return data as JSON
        return jsonify(contracts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_contract_pdf(account, product_name, customer_name, quantity) -> tuple[str, str]:
    conn = psycopg2.connect(Config.CONNECTION_STRING)
    cur = conn.cursor()

    sql_for_count = f"SELECT \"supply_chain\".get_contract_count();"
    cur.execute(sql_for_count)
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    filename = f"{Config.NAME}-{customer_name}-{product_name}-{quantity}{count}.pdf"
    save_location = f"{Config.BASE_DIR}/../../documents"

    pdf = FPDF()

    pdf.add_page()

    content = (f"This is a purchasing agreement between {Config.NAME} "
               f"and {customer_name} for {quantity} of {product_name}.\n\n{date.today()}")

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=content, align='C')

    PDF_URI = save_location + filename;
    pdf.output(PDF_URI)

    k = keccak.new(digest_bits=256)
    k.update(content)

    return PDF_URI, k.hexdigest()


@app.route('/start-contract/', methods=['POST'])
def start_contract(request):
    try:
        if request.method == 'POST':
            account = request.form.get("account")
            product_id = request.form.get("product")
            quantity = request.form.get("quantity")

            conn = psycopg2.connect(Config.CONNECTION_STRING)
            cur = conn.cursor()

            sql_for_info = f"SELECT \"supply_chain\".get_contract_data({product_id}, {account});"
            cur.execute(sql_for_info)
            row = cur.fetchone()

            product_name = row[0]
            customer_name = row[1]

            PDF_URI, hash = generate_contract_pdf(account, product_name, customer_name, quantity)

            conn = psycopg2.connect(Config.CONNECTION_STRING)
            cur = conn.cursor()

            sql = f"SELECT \"supply_chain\".insert_contract_and_return_id({product_id}, {account}, {quantity}, {PDF_URI});"

            cur.execute(sql)
            id = cur.fetchone()[0]

            tx_hash = contract.functions.startAgreement(id, account, product_name, quantity, hash).transact({'from': Config.PUBLIC_KEY})
            web3.eth.wait_for_transaction_receipt(tx_hash)

            conn.commit()
            cur.close()
            conn.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/contract-fulfilment/<id>', methods=['GET'])
def get_contract_fulfilment(id):
    try:
        result = contract.functions.getContractFulfilment(id).call()
        fulfilment = {"client": result[0], "seller": result[1]}

        return jsonify(fulfilment)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/contract-trail/<id>', methods=['GET'])
def get_contract_trail(id):
    try:
        result = contract.functions.getTrailHistory(id).call()

        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = f"SELECT account, name from \"supply_chain\".\"Customer\""

        cur.execute(sql)
        data = cur.fetchall()

        trail = [row[1] for row in data if row[0] in result]

        cur.close()
        conn.close()

        return jsonify(trail)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/contract-data/<id>', methods=['GET'])
def get_contract_data(id):
    try:
        result = contract.functions.getAgreementData(id).call()
        data = {
            "seller": result[0],
            "holder": result[1],
            "client": result[2],
            "product": result[3],
            "quantity": result[4]
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deliver/<id>', methods=['POST'])
def next_destination(request, id):
    if request.method == 'POST':
        try:
            account = request.form.get('account')

            tx_hash = contract.functions.startAgreement(id, account).transact( {'from': Config.PUBLIC_KEY})
            web3.eth.wait_for_transaction_receipt(tx_hash)

            print(tx_hash)

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/end-agreement/<id>', methods=['POST'])
def end_agreement(request, id):
    if request.method == 'POST':
        try:
            account = request.form.get('account')

            tx_hash = contract.functions.endAgreement(id).transact( {'from': Config.PUBLIC_KEY, 'value': web3.toWei(1, 'ether')})
            web3.eth.wait_for_transaction_receipt(tx_hash)

            print(tx_hash)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

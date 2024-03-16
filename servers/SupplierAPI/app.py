from flask import Flask, jsonify, request
import psycopg2

# Database connection details
DB_NAME = "SupplyChain"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = 5432

# Define connection string
conn_string = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Flask server is running!"

@app.route("/products", methods=["GET"])
def get_products():
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        # Define your product query
        sql = "SELECT id, name, description, price FROM \"Supplier\".\"Product\""
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
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        # Define your customer query
        sql = "SELECT id, name, location FROM \"Supplier\".\"Customer\""
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
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        sql = """
        SELECT id, product_id, quantity from \"Supplier\".\"Inventory\";
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
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        # Define your contract query (assuming foreign key relationships)
        sql = "SELECT id, product_id, customer_id, quantity, contract_path FROM \"Supplier\".\"Contract\";";

        cur.execute(sql)

        # Fetch data as list of dictionaries
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

if __name__ == "__main__":
    app.run(debug=True)

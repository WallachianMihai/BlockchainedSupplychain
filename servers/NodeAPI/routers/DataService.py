from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from config.config import Config
import logging
import psycopg2

router = APIRouter(
    prefix="",
    tags=["Node-Service"],
    responses={404: {"description": "Not found"}}
)


@router.get("/products", tags=['node'])
async def get_products():
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
        return JSONResponse(content=products)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/customers", tags=['node'])
async def get_customers():
    try:
        # Connect to the database
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        # Define your customer query
        sql = "SELECT account, name, location, role FROM \"supply_chain\".\"Customer\""
        cur.execute(sql)

        # Fetch data as list of dictionaries
        data = cur.fetchall()
        print(data)
        customers = [
            {
                "account": row[0],
                "name": row[1],
                "location": row[2],
                "role": row[3]
            }
            for row in data
        ]

        # Close connection
        cur.close()
        conn.close()

        # Return data as JSON
        return JSONResponse(content=customers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/inventory", tags=["inventory"])
async def get_inventory():
    try:
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = """
        SELECT i.id, p.name, i.quantity from \"supply_chain\".\"Inventory\" as i
        join \"supply_chain\".\"Product\" as p on product_id = p.id;
        """

        cur.execute(sql)

        data = cur.fetchall()
        print(data)
        inventory = [
            {
                "id": row[0],
                "product_name": row[1],
                "quantity": row[2],
            }
            for row in data
        ]

        cur.close()
        conn.close()

        return JSONResponse(content=inventory)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/contracts", tags=["contract"])
async def get_contracts():
    try:
        conn = psycopg2.connect(Config.CONNECTION_STRING)
        cur = conn.cursor()

        sql = "SELECT id, product_id, customer_account, quantity, contract_path FROM \"supply_chain\".\"Contract\";"

        cur.execute(sql)

        data = cur.fetchall()
        print(data)
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
        print(contracts)
        return JSONResponse(content=contracts)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

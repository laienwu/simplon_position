from pathlib import Path
import sqlite3
import requests

# set request link env
SALES_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
PRODUCT_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
STORE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
schema_path = Path("./db_schema.sql")
SQLITE_URI = "/db/database.sqlite"


def create_tables(schema: sqlite3, conn: sqlite3.Connection) -> None:
    try:
        cursor = conn.cursor()
        cursor.executescript(schema)
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


def populate_vente(conn: sqlite3.Connection, rows: list, table_name: str = 'Vente') -> None:
    try:
        cursor = conn.cursor()
        cursor.executemany(f"INSERT or IGNORE INTO {table_name} VALUES (?,?,?,?)", rows)
        print("Rows inserted successfully in Ventes table.")
    except sqlite3.Error as e:
        print(f"Error inserting rows: {e}")


def populate_magasin(conn: sqlite3.Connection, rows: list, table_name: str = 'Magasins') -> None:
    try:
        cursor = conn.cursor()
        cursor.executemany(f"INSERT or IGNORE INTO {table_name} VALUES (?,?,?)", rows)
        print("Rows inserted successfully in Magasins table.")
    except sqlite3.Error as e:
        print(f"Error inserting rows: {e}")


def populate_produits(conn: sqlite3.Connection, rows: list, table_name: str = 'Produits') -> None:
    try:
        cursor = conn.cursor()
        cursor.executemany(f"INSERT or IGNORE INTO {table_name} VALUES (?,?,?,?)", rows)
        print("Rows inserted successfully in Produits table.")
    except sqlite3.Error as e:
        print(f"Error inserting rows: {e}")


if '__main__' == __name__:
    sales = requests.get(SALES_URL).content.decode('utf-8')
    products = requests.get(PRODUCT_URL).content.decode('utf-8')
    stores = requests.get(STORE_URL).content.decode('utf-8')
    sales_data = [tuple(elem.split(',')) for elem in sales.split('\r\n')[1:]]
    products_data = [tuple(elem.split(',')) for elem in products.split('\r\n')[1:]]
    stores_data = [tuple(elem.split(',')) for elem in stores.split('\r\n')[1:]]

    # conn = sqlite3.connect('database.sqlite')
    try:
        conn = sqlite3.connect(SQLITE_URI, uri=True)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise Exception(f"Error connecting to database: {SQLITE_URI}")

    with open(schema_path, "r", encoding='utf-8') as file:
        schema_sql = file.read()
        with conn:
            create_tables(schema_sql, conn)
    with conn:
        populate_vente(conn, table_name="Ventes", rows=sales_data)
        populate_magasin(conn, table_name="Magasins", rows=stores_data)
        populate_produits(conn, table_name="Produits", rows=products_data)

    print('test de select')
    res = conn.execute("SELECT * FROM Ventes").fetchall()
    print(res)


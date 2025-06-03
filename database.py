import sqlite3

DATABASE = 'shop.db'
import os
'''print("DB will be created at:", os.path.abspath(DATABASE))'''

def get_connection():
    return sqlite3.connect(DATABASE)

def tables():
    connection = get_connection()
    cursor = connection.cursor()

    print("Running create_tables()...")
    print("Database path:", os.path.abspath(DATABASE))

    cursor.execute( """
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(30) NOT NULL,
        password VARCHAR(30) NOT NULL,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15) NOT NULL,
        address VARCHAR(30),
        admin INT DEFAULT 0
        );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(15) NOT NULL,
        category VARCHAR(15) NOT NULL,
        price INT NOT NULL,
        stock INT default 0
            );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL,
        order_price INT,
        FOREIGN KEY(customer_id) REFERENCES user(id)
        );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_item(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        price INT NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES product(id)
        );
    """)

    connection.commit()
    connection.close()
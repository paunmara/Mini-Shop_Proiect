from .database import get_connection

class User:
    def __init__(self, username, email, password, first_name, last_name, address = None, user_id = None, admin = False):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.admin = admin

    def pass_check(self,password_attempt):
        return self.password == password_attempt

    def save_user(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO user (username, email, password, first_name, last_name, address, admin) VALUES (?,?,?,?,?,?,?)""",
                       (self.username, self.email, self.password, self.first_name, self.last_name, self.address, int(self.admin))
        )

        self.id = cursor.lastrowid

        connection.commit()
        connection.close()

    @classmethod
    def get_user(cls,username):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return cls(user_id = row[0], username = row[1], email = row[2], password = row[3], first_name = row[4], last_name = row[5], address = row[6], admin = bool(row[7]))
        else:
            return None

    def delete_user(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM users WHERE id = ?
        """, self.id)
        connection.commit()
        connection.close()

class Product:
    def __init__(self, name, category, price, stock, product_id = None):
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def save_product(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO product (name,category,price,stock) VALUES(?,?,?,?)""",
                       (self.name,self.category,self.price,self.stock))

        self.id = cursor.lastrowid

        connection.commit()
        connection.close()

    @classmethod
    def get_products(cls):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM product ORDER BY category DESC")
        rows = cursor.fetchall()
        connection.close()

        products = []
        for row in rows:
            product = cls(product_id = row[0], name = row[1], category = row[2], price = row[3], stock = row[4])
            products.append(product)

        return products
    @staticmethod
    def get_price(name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT price FROM product WHERE id = ?", (name,))
        price = cursor.fetchone()
        connection.close()
        return price[0]
    @classmethod
    def get_single_product(cls, product_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        connection.close()

        return cls(product_id = row[0], name = row [1], category = row[2], price = row[3], stock = row[4])

    def delete_product(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM product WHERE name = ?", self.name)
        connection.commit()
        connection.close()

class Order:
    def __init__(self, user_id, items, order_price = None, order_id = None):
        self.userid = user_id
        self.items = items
        self.price = order_price
        self.orderid = order_id

    def save_order(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO orders(customer_id) VALUES(?)
        """, (self.userid,))

        self.orderid = cursor.lastrowid

        for item in self.items:
            cursor.execute("""
                INSERT INTO order_item(order_id, product_id, quantity, price) VALUES (?,?,?,?)
            """, (self.orderid, item['product_id'], item['quantity'], item['price']))

            # Reduce stock for the product
            cursor.execute("""
                UPDATE product SET stock = stock - ? WHERE id = ?
            """, (item['quantity'], item['product_id']))

        connection.commit()
        connection.close()

    @classmethod
    def get_user_order(cls, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT o.id, p.name, oi.quantity, oi.price 
            FROM orders o
            JOIN order_item oi ON o.id = oi.order_id
            JOIN product p ON oi.product_id = p.id 
            WHERE o.customer_id = ?
        """,(user_id,))
        rows = cursor.fetchall()
        connection.close()

        for row in rows:
            print(f"Order ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Price: {row[3]}")
    @classmethod
    def delete_order(cls, order_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM order_item WHERE order_id = ?",(order_id,))
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        connection.commit()
        connection.close()
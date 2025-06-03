import unittest
import sqlite3
from myapp import database
from myapp.models import User, Product, Order

def get_test_connection():
    conn = sqlite3.connect(":memory:")
    database.get_connection = lambda: conn
    database.tables()
    return conn

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.conn = get_test_connection()

    def test_create_user(self):
        user = User(
            username="testuser",
            email="test@example.com",
            password="1234",
            first_name="Test",
            last_name="User",
            address="Test Street"
        )
        user.save_user()
        self.assertIsNotNone(user.id)

    def test_get_user_returns_none_if_missing(self):
        result = User.get_user("doesnotexist")
        self.assertIsNone(result)

class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.conn = get_test_connection()

    def test_add_and_get_products(self):
        product = Product("Laptop", "Electronics", 1200, 5)
        product.save_product()

        products = Product.get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Laptop")

class TestOrderModel(unittest.TestCase):
    def setUp(self):
        self.conn = get_test_connection()
        # Create user and product
        self.user = User("alex", "a@.com", "pass", "alex", "vasile")
        self.user.save_user()

        self.product = Product("Phone", "Electronics", 800, 10)
        self.product.save_product()

    def test_save_order(self):
        items = [
            {"product.id": self.product.id, "quantity": 2, "price": 1600}
        ]
        order = Order(user_id=self.user.id, items=items)
        order.save_order()

        self.assertIsNotNone(order.orderid)

        self.conn = get_test_connection()
class TestLoginFunctionality(unittest.TestCase):
    def setUp(self):
        self.admin_user = User(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            admin=True
            )
        self.admin_user.save_user()

        self.normal_user = User(
            username="user",
            email="user@example.com",
            password="userpass",
            first_name="Normal",
            last_name="User"
        )
        self.normal_user.save_user()

    def test_admin_login(self):
        user = User.get_user("admin")
        self.assertTrue(user.admin)
        self.assertEqual(user.username, "admin")

    def test_normal_user_login(self):
        user = User.get_user("user")
        self.assertFalse(user.admin)
        self.assertEqual(user.username, "user")
if __name__ == '__main__':
    unittest.main()

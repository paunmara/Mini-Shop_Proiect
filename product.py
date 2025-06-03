from .models import Product, Order

def add_product():
    print("=== Add a product ===")
    name = input("Enter product name: ")
    category = input("Enter product category: ")
    price = int(input("Enter product price: "))
    stock = int(input("Enter product stock: "))

    new_product = Product(name = name, category = category, price = price, stock = stock)
    new_product.save_product()

    print("You added a new product!")

def delete_product():
    print("=== Delete a product ===\n")
    list_products()
    print("\n")
    name = input("Choose a product to delete: ")
    deleted_product = Product(name = name, category = "", price = "", stock = "")
    deleted_product.delete_product()
    print("You deleted a product!")

def list_products():
    print("=== Product list ===")
    products = Product.get_products()
    for product in products:
        print(f'{product.id}. {product.name} -> {product.price}')

def add_product_to_order(current_user):
    print("=== Place an order ===")
    print("--- when you are done with the order type 'done' ---")
    list_products()
    items = []

    while True:
        product_id = input("Enter the product's ID to add to your order (or 'done'): ")
        if product_id.lower() == 'done':
            order = Order(current_user.id, items)
            order.save_order()
            print("Your order was registered!")
            break
        if not product_id.isdigit():
            print("Invalid Product!")
            continue
        else:
            product = Product.get_single_product(int(product_id))
            quantity = int(input("Select quantity: "))
            if product.stock == 0 or quantity > product.stock:
                print("No stock!")
                continue
            else:
                product_price = Product.get_price(product.id)
                items.append({
                    'product_id': product.id,
                    'name': product,
                    'quantity': quantity,
                    'price': product_price
                })
    fin_order(current_user)

def fin_order(current_user):
    while True:
        choice = input("Would you like to view or delete your order?(Type 'view', 'delete' or 'done'): ")
        if choice == 'done':
            print("Returning to the main menu...")
            return
        elif choice == 'view':
            print("Here are your orders:\n")
            Order.get_user_order(current_user.id)
        elif choice == 'delete':
            print("Your order was deleted!")
            Order.delete_order(current_user.id)
        else:
            print("Invalid option!")
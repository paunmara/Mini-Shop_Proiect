from myapp.registration import login_user, sign_up_user
from myapp.database import tables
from myapp.product import list_products, delete_product, add_product, add_product_to_order
tables()

def login_menu():
    current_user = None
    while not current_user:
        print("==WELCOME==")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

        choice = int(input("Choose an option: "))

        if choice == 1:
            current_user = login_user()
            if not current_user:
                print("Login failed!")
        elif choice == 2:
            current_user = sign_up_user()
            if not current_user:
                print("Sign up failed!")
        elif choice == 3:
            exit()
        else:
            print("Invalid option")
    main_menu(current_user)

def main_menu(current_user):
    print(f'=== Welcome {current_user.first_name}!')

    if current_user.admin == True:
        print("1. Add a new Product")
        print("2. Delete a product")
        print("3. List all products")
        print("4. Place an order")
        print("5. Exit")

        admin_choice = int(input("Choose an option: "))
        if admin_choice == 1:
            add_product()
        elif admin_choice == 2:
            delete_product()
        elif admin_choice == 3:
            list_products()
        elif admin_choice == 4:
            add_product_to_order(current_user)
        else:
            exit()
    else:
        print("1. List all products")
        print("2. Place an order")
        print("3. Exit")

        user_choice = int(input("Choose an option: "))

        if user_choice == 1:
            list_products()
        elif user_choice == 2:
            add_product_to_order(current_user)
        else:
            exit()

login_menu()
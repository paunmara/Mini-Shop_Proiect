from .models import User

def login_user():
    print("=== Login User ===")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    user = User.get_user(username)
    if user.password == password:
        print("Login successful!")
        return user
    else:
        print("Login Failed!")
        return None

def sign_up_user():
    print("=== Sign Up New User ===\n")

    username = input("Enter an username: ")
    email = input("Enter an email: ")
    password = input("Enter a password: ")
    last_name = input("Enter your last name: ")
    first_name = input("Enter your first name: ")
    address = input("Enter your address: ")
    admin_check = input("Is this user an admin? (yes/no): ")

    if admin_check == "yes":
        admin = True
    else:
        admin = False

    if User.get_user(username):
        print("Username already exists!")
        return None
    new_user = User(username = username, email = email, password = password, first_name = first_name, last_name = last_name, address = address, admin = admin)
    new_user.save_user()
    print("Sign up successful!")
    return new_user
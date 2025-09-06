import os
import sys
import time
import re
import random
import datetime

#Main Menu Function do not delete or modify this function
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Administrator Login")
        print("2. Staff Login")
        print("3. Member Login")
        print("4. Guest Access")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            admin_login()  
        elif choice == '2':
            staff_login()
        elif choice == '3':
            member_login()
        elif choice == '4':
            guest_access() 
        elif choice == '5':
            print("Exiting the program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

#Miscellaneous Functions:

#Password Making Function:
def password_making(password):
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r'[A-Z]', password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not re.search(r'[a-z]', password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not re.search(r'[0-9]', password):
        print("Password must contain at least one digit.")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        print("Password must contain at least one special character.")
        return False
    return True

#Admin Class:
class Admin:
    def __init__(self, admin_id, name, password, contact):
        self.admin_id = admin_id
        self.name = name
        self.password = password
        self.contact = contact

    def __str__(self):
        return f"Admin ID: {self.admin_id}, Name: {self.name}, Contact: {self.contact}"

    @staticmethod
    def get_valid_name():
        while True:
            name = input("Enter admin name: ")
            if any(char.isdigit() for char in name) or not name.replace(" ", "").isalpha():
                print("Invalid username. It must not contain numbers or special characters.")
                continue
            return name

    @staticmethod
    def get_valid_password():
        while True:
            password = input("Enter new password: ")
            if not password_making(password):
                continue
            return password

    @staticmethod
    def get_valid_contact():
        while True:
            contact = input("Enter contact number: ")
            if not re.match(r'^\d{10}$', contact):
                print("Invalid contact number. Please enter a 10-digit number.")
                continue
            return contact

#Administrator Section:

#Admin Login and Registration Function:
#Admin ID Generator Function:
def adminID_Generator():
    if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
        with open("Admin Cred.txt", "r") as file:
            num_users = len(file.readlines())
        new_admin_id = str(num_users + 1).zfill(5)
    else:
        new_admin_id = "00001"
    print(f"Generated Admin ID: {new_admin_id}")
    return new_admin_id

#Admin Registration Function:
def admin_registration():
    print("Admin Registration")
    name = Admin.get_valid_name()
    password = Admin.get_valid_password()
    contact = Admin.get_valid_contact()
    admin_id = adminID_Generator()
    with open("Admin Cred.txt", "a") as file:
        file.write(f"{admin_id},{name},{password},{contact}\n")
    print(f"Admin registered successfully with ID: {admin_id}")
    return f"Admin registered successfully with ID: {admin_id}"

#Admin Login Function:
def admin_login():
    while True:
        print("Admin Login")
        admin_id = input("Enter Admin ID: ")
        password = input("Enter Password: ")
        with open("Admin Cred.txt", "r") as file:
            for line in file:
                stored_id, stored_name, stored_password, stored_contact = line.strip().split(',')
                if admin_id == stored_id and password == stored_password:
                    print(f"Welcome, {stored_name}!")
                    admin = Admin(stored_id, stored_name, stored_password, stored_contact)
                    return admin_menu(admin)
        print("Invalid credentials. Please try again.")

#Admin Menu Function:
def admin_menu(admin):
    while True:
        print("Admin Menu:")
        print("1. Manage staff")
        print("2. Manage Members")
        print("3. Manage Repository")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            manage_staff()
        elif choice == '2':
            manage_members()
        elif choice == '3':
            manage_repository()
        elif choice == '4':
            print("Logging out.")
            break

#Manage Staff Function:
def manage_staff():
    print("Manage Staff")
    print("1. Staff Manaagement")
    print("2. Admin Management")
    print("3. Back to Admin Menu")
    choice = input("Enter your choice (1-3): ")
    if choice == '1':
        print("Staff Management Selected")
        return Staff_Manager()
    elif choice == '2':
        print("Admin Management Selected")
        return Admin_Manager()
    elif choice == '3':
        return admin_menu()
    else:
        print("Invalid choice. Please try again.")









































#Staff Section:
#Staff Login Function:








#Member Section:
#Member Login Function:





#Guest Section:
#Guest Access Function:







# DO NOT DELETE THE BELOW LINE OR ENTER ANYTHING BELOW THIS LINE UNLESS YOU ARE DELBERT #
def main():
    while True:
       main_menu()

if __name__ == "__main__":
    main()
import os
import sys
import time
import re
import random
import datetime
import pandas as pd

#@Main Menu Function do not delete or modify this function //ANCHOR : Main Menu Function:
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

#@Miscellaneous Functions://ANCHOR : Miscellaneous Functions:
#lockout Function:
def lockout(locked_out):
    while True:
        current_time = datetime.datetime.now()
        remaining_time = int((locked_out - current_time).total_seconds())
        if remaining_time <= 0:
            break
        print(f"Too many incorrect attempts. Please wait {remaining_time} seconds.", end='\r')
        time.sleep(1)
        
#@Password Making Function:
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
    if not re.search(r'[!#@$%^&*(),.?":{}|<>]', password):
        print("Password must contain at least one special character.")
        return False
    return True

#@Admin Class: //ANCHOR : Admin Class:
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
            input_contact = input("Enter contact number: ")
            if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
                with open("Admin Cred.txt", "r") as file:
                    for line in file:
                        _, _, _, stored_contact = line.strip().split(',')
                        if input_contact == stored_contact:
                            print("Contact number already exists. Please enter a different number.")
                            break
                    else:
                        if not re.match(r'^\d{10}$', input_contact):
                            print("Invalid contact number. Please enter a 10-digit number.")
                            continue
                        return input_contact
        
    def verify_password(self):
        attempts = 3
        while attempts > 0:
            password = input("Re-enter password for verification: ")
            if password == self.password:
                return True
            else:
                attempts -= 1
                print(f"Incorrect password. You have {attempts} attempts left.")
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return admin_menu(admin=self)
    
    @staticmethod
    def credential_verification(input_id, input_password):
        print("Verifying credentials...")
        if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
            with open("Admin Cred.txt", "r") as file:
                for line in file:
                    stored_id, _, stored_password, _ = line.strip().split(',')
                    if input_id == stored_id and Admin.verify_password(input_password, stored_password):
                        return True
        print("Invalid Admin ID or Password.")
        return False
    
    
    

#@Administrator Section: //ANCHOR : Administrator Section:

#@Admin Login and Registration Function:
#@Admin ID Generator Function:
def adminID_Generator():
    if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
        with open("Admin Cred.txt", "r") as file:
            next(file)
            num_users = len(file.readlines())
        new_admin_id = str(num_users + 1).zfill(5)
    else:
        new_admin_id = "00001"
    print(f"Generated Admin ID: {new_admin_id}")
    return new_admin_id

#@Admin Registration Function: //ANCHOR - Admin Registration Function:
def admin_registration(admin):
    print("Admin Registration")
    name = Admin.get_valid_name()
    password = Admin.get_valid_password()
    contact = Admin.get_valid_contact()
    admin_id = adminID_Generator()
    with open("Admin Cred.txt", "a",newline="\n") as file:
        file.write(f"\n{admin_id},{name},{password},{contact}")
    print(f"Admin registered successfully with ID: {admin_id}")
    while True:
        continue_choice = input("Do you want to register another admin? (y/n): ").lower()
        if continue_choice == 'y':
            return admin_registration(admin)
        elif continue_choice == 'n':
            return manage_admin(admin)

#@Admin Login Function: //ANCHOR - Admin Login Function:
def admin_login():
    attempts = 3
    locked_out = None  
    while attempts > 0:
        print("Admin Login")
        input_id = input("Enter Admin ID: ")
        input_password = input("Enter Password: ")
        if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
            with open("Admin Cred.txt", "r") as file:
                for line in file:
                    stored_id, name, stored_password, contact = line.strip().split(',')
                    if input_id == stored_id and input_password == stored_password:
                        print(f"Welcome, {name}!")
                        admin = Admin(stored_id, name, stored_password, contact)
                        return admin_menu(admin)
            print(f"Invalid Admin ID or Password. You have {attempts-1} attempts left.")
            attempts -= 1
        if attempts == 0:
            locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
            lockout(locked_out)
            attempts = 3
            return main_menu()

        
#@Admin Menu Function: //ANCHOR - Main Admin Menu Function:
def admin_menu(admin):
    while True:
        print("Admin Menu:")
        print("1. Admin Management")
        print("2. Staff Management")
        print("3. Member Management")
        print("4. Repository Management")
        print("5. Logout")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            if admin.verify_password():
                return manage_admin(admin)
        elif choice == '2':
            if admin.verify_password():
                return manage_staff(admin)
        elif choice == '3':
            if admin.verify_password():
                return manage_members(admin)
        elif choice == '4':
            if admin.verify_password():
                return manage_repository(admin)
        elif choice == '5':
            print("Logging out.")
            return admin_menu(admin)
        else:
            print("Invalid choice. Please try again.")

#@Admin Section://ANCHOR : Admin Menu Function:
#@Admin Manager Menu Function:
def manage_admin(admin):
    while True:
        print("Administrator Management")
        print("1. Add Admin")
        print("2. View Admin")
        print("3. Remove Admin")
        print("4. Previous Menu")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            print("Add Admin")
            return admin_registration(admin)
        elif choice == '2':
            print("View Admin")
            return view_members()
        elif choice == '3':
            print("Remove Admin")
            return remove_member()
        elif choice == '4':
            return Admin_manager(admin)
        else:
            print("Invalid choice. Please try again.")

#@Staff Section://ANCHOR - (Admin) Staff Management Section:
#@Add Staff Menu Function:
def manage_staff(admin):
    while True:
        print("Staff Management")
        print("1. Add Staff")
        print("2. View Staff")
        print("3. Remove Staff")
        print("4. Previous Menu")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            print("Add Staff")
            return add_staff()
        elif choice == '2':
            print("View Staff")
            return view_staff()
        elif choice == '3':
            print("Remove Staff")
            return remove_staff()
        elif choice == '4':
            return admin_menu(admin)
        else:
            print("Invalid choice. Please try again.")


#@Member Section: //ANCHOR - (Admin) Member Management Section:
#@Manage Members Menu Function:
def manage_members(admin):
    while True:
        print("Member Management")
        print("1. Add Member")
        print("2. View Members")
        print("3. Remove Member")
        print("4. Previous Menu")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            print("Add Member")
            return add_member()
        elif choice == '2':
            print("View Members")
            return view_members()
        elif choice == '3':
            print("Remove Member")
            return remove_member()
        elif choice == '4':
            return admin_menu(admin)
        else:
            print("Invalid choice. Please try again.")
        

#@Manage Repository Function: //ANCHOR - (Admin) Repository Management Section:
def manage_repository():
    while True:
        print("Repository Management")
        print("1. Add Book")
        print("2. View Repository")
        print("3. Remove Book")
        print("4. View Issued Books")
        print("5. View Returned Books")
        print("6. Previous Menu")
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            return add_book()
        elif choice == '2':
            print("View Members")
            return view_repo()
        elif choice == '3':
            print("Remove Member")
            return remove_book()
        elif choice == '4':
            return view_issued_books()
        elif choice == '5':
            return view_returned_books()
        elif choice == '6':
            return admin_menu(admin)
        else:
            print("Invalid choice. Please try again.")
























#Staff Section:
#Staff Login Function:








#Member Section:
#Member Login Function:





#Guest Section:
#Guest Access Function:







# DO NOT DELETE THE BELOW LINE OR ENTER ANYTHING BELOW THIS LINE UNLESS YOU ARE DELBERT #@
def main():
    while True:
       main_menu()

if __name__ == "__main__":
    main()
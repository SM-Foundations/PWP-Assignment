import os
import sys
import time
import re
import datetime


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
    if not re.search(r'[!#@$%^&*(),.?":{}|<>-]', password):
        print("Password must contain at least one special character.")
        return False
    return True

#@Admin Class: //ANCHOR : Admin Class:
class Admin:
    def __init__(self, admin_id, password, sec_phrase, name=None, contact=None):
        self.admin_id = admin_id
        self.password = password
        self.Sec_Phrase = sec_phrase
        self.name = name
        self.contact = contact

    def verify_password(stored_password, input_password):
        try:
            if os.path.exists("Admin Password.txt") and os.path.getsize("Admin Password.txt") > 0:
                with open("Admin Password.txt", "r",encoding="utf-8") as file:
                    next(file)
                    for line in file:
                        stored_id, stored_password = line.strip().split(',')
            return stored_id, stored_password == input_password
        except FileNotFoundError:
            print("file not found")
            return main_menu()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return main_menu()

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
                with open("Admin Cred.txt", "r", encoding="utf-8") as file:
                    next(file)
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                            _, _, stored_contact = parts
                            if input_contact == stored_contact:
                                print("Contact number already exists. Please enter a different number.")
                                break
                    else:
                        if not re.match(r'^\d{10}$', input_contact):
                            print("Invalid contact number. Please enter a 10-digit number.")
                            continue
                        return input_contact
    
    def verify_password(self):
        try:
            attempts = 3
            while attempts > 0:
                password = input("Re-enter password for verification: ")
                input_phrase = input("Re-enter your security phrase: ")
                if password == self.password and input_phrase == self.Sec_Phrase:
                    return True
                else:
                    attempts -= 1
                    print(f"Incorrect password or security phrase. You have {attempts} attempts left.")
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return admin_menu(admin=self)
        except FileNotFoundError:
            print("file not found")
            return main_menu()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return main_menu
            
    @staticmethod
    def credential_verification(input_id, input_password, sec_phrase):
        if os.path.exists("Admin Password.txt") and os.path.getsize("Admin Password.txt") > 0:
            with open("Admin Password.txt", "r", encoding='utf-8') as file:
                next(file)
                for line in file:
                    stored_id, stored_password, stored_phrase = line.strip().split(',')
                    if input_id == stored_id and input_password == stored_password and sec_phrase == stored_phrase:
                        print("Credentials verified successfully.")
                        return True
        print("Invalid Admin ID or Password.")
        return False
    
    @staticmethod
    def admin_table(admin_data):
        try:
            with open("Admin Cred.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                admin_data = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ]
                if not admin_data:
                    print("No data to be displayed")
            print(f"|{headers[0]:10} | {headers[1]:<15} | {headers[2]:<20}|")
            print("-" * 60)
            for row in admin_data:
                print(f"|{row[0]:<10} | {row[1]:<15} | {row[2]:<20}|")
        except FileNotFoundError:
            print("Error: 'routes admin.txt' file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

#@Administrator Section: //ANCHOR : Administrator Section:

#@Admin Login and Registration Function:
#@Admin ID Generator Function:
def adminID_Generator():
    if os.path.exists("Admin Cred.txt") and os.path.getsize("Admin Cred.txt") > 0:
        with open("Admin Cred.txt", "r",encoding="utf-8") as file:
            next(file)
            num_users = len(file.readlines())
        new_admin_id = str(num_users + 1).zfill(5)
    else:
        new_admin_id = "00001"
    print(f"Generated Admin ID: {new_admin_id}")
    return new_admin_id

#@Admin Registration Function: //ANCHOR - Admin Registration Function:
def admin_registration(admin):
    try:
        print("Admin Registration")
        name = Admin.get_valid_name()
        password = Admin.get_valid_password()
        contact = Admin.get_valid_contact()
        security_phrase = input("Enter a security phrase: ")
        admin_id = adminID_Generator()
        if not os.path.exists("Admin Cred.txt") or os.path.getsize("Admin Cred.txt") == 0:
            with open("Admin Cred.txt", "a", newline="\n", encoding="utf-8") as file:
                file.write("AdminID,Name,Contact\n")
        with open("Admin Cred.txt", "a", newline="\n", encoding="utf-8") as file:
            file.write(f"\n{admin_id},{name},{contact}\n")
        if not os.path.exists("Admin Password.txt") or os.path.getsize("Admin Password.txt") == 0:
            with open("Admin Password.txt", "a", newline="\n", encoding="utf-8") as file:
                file.write("AdminID,Password,Security_Question\n")
        with open("Admin Password.txt", "a", newline="\n", encoding="utf-8") as file:
            file.write(f"\n{admin_id},{password},{security_phrase}\n")
        Admin.admin_table(admin)
        print(f"Admin account set successfully for Admin ID: {admin_id}")
        while True:
            continue_choice = input("Do you want to register another admin? (y/n): ").lower()
            if continue_choice == 'y':
                return admin_registration(admin)
            elif continue_choice == 'n':
                return manage_admin(admin)
    except FileNotFoundError:
        print("file not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#@Admin Login Function: //ANCHOR - Admin Login Function:
def admin_login():
    try:
        attempts = 3
        locked_out = None 
        while attempts > 0:
            print("Admin Login")
            input_id = input("Enter Admin ID: ")
            input_password = input("Enter Password: ")
            sec_phrase = input("Enter Security Phrase: ")
            if Admin.credential_verification(input_id, input_password, sec_phrase):
                admin = Admin(input_id,input_password,sec_phrase)
                return admin_menu(admin)
            print(f"Invalid Admin ID or Password. You have {attempts-1} attempts left.")
            attempts -= 1
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return main_menu()
    except FileNotFoundError:
        print("file not found")
        return manage_admin(admin)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return manage_admin(admin)

        
#@Admin Menu Function: //ANCHOR - Main Admin Menu Function:
def admin_menu(admin):
    while True:
        print("Admin Menu:")
        print("1. Admin Management")
        print("2. Staff Management")
        print("3. Member Management")
        print("4. Repository Management")
        print("5. Reset Password")
        print("6. Logout")
        choice = input("Enter your choice (1-6): ")
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
            if admin.verify_password():
                return reset_password_self(admin)
        elif choice == '6':
            print("Logging out.")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

#@Admin Section://ANCHOR : Admin Menu Function:
#@Admin Manager Menu Function:
def manage_admin(admin):
    while True:
        print("Administrator Management")
        print("1. View Admin")
        print("2. Add Admin")
        print("3. Remove Admin")
        print("4. Reset Password")
        print("5. Previous Menu")
        print('6. Logout')
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            return view_admin(admin)
        elif choice == '2':
            return add_admin(admin)
        elif choice == '3':
            return remove_admin(admin)
        elif choice == '4':
            return password_reset_admin(admin)
        elif choice == '5':
            return admin_menu(admin)
        elif choice == '6':
            print("Logging Out")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

#@ View Admin Functions:
def view_admin(admin):
    while True:
        Admin.admin_table(admin)
        os.system('pause')
        return manage_admin(admin)
    
#@ Add Admin Function:
def add_admin(admin):
    while True:
        return admin_registration(admin)
        
#@ Remove Admin Function:
def remove_admin(admin):
    try:
        Admin.admin_table(admin)
        with open("Admin Password.txt", 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_sec = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        with open("Admin Cred.txt", 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_cred = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        selected_admin = input("\nEnter Admin ID to remove: ").strip()

        admin_index = -1
        for index, line in enumerate(admin_sec):
            if line[0] == selected_admin:
                admin_index = index
        for index, line in enumerate(admin_cred):
            if line[0] == selected_admin:
                admin_index = index
                break

        if admin_index == -1:
            print("No matching ID found.")
            return manage_admin(admin)
        
        selected_admin = admin_cred[admin_index]
        confirm = input(f"Are you sure you want to delete this admin: {', '.join(selected_admin)}? (y/n): ").lower()
        if confirm != 'y':
            print("Deletion canceled.")
            return manage_admin(admin)
        admin_cred.pop(admin_index)
        admin_sec.pop(admin_index)

        with open("Admin Cred.txt", 'w', encoding='utf-8') as file:
            file.write(','.join(headers) + '\n')
            for row in admin_cred:
                file.write(','.join(row) + '\n')
        
        with open("Admin Password.txt", 'w', encoding='utf-8') as file:
            file.write(','.join(headers) + '\n')
            for row in admin_sec:
                file.write(','.join(row) + '\n')
        while True:
            continue_choice = input("Do you want to register another admin? (y/n): ").lower()
            if continue_choice == 'y':
                return admin_registration(admin)
            elif continue_choice == 'n':
                return manage_admin(admin)
    except FileNotFoundError:
        print("file not found")
        return manage_admin(admin)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return manage_admin(admin)
    
#@ Password Reset Function:
def password_reset_admin(admin):
    try:
        Admin.admin_table(admin)
        with open("Admin Password.txt", 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_sec = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        with open("Admin Cred.txt", 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_cred = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        selected_admin = input("\nEnter Admin ID to reset password: ").strip()

        admin_index = -1
        for index, line in enumerate(admin_sec):
            if line[0] == selected_admin:
                admin_index = index

        if admin_index == -1:
            print("No matching ID found.")
            return manage_admin(admin)
        
        selected_admin = admin_cred[admin_index]
        confirm = input(f"Are you sure you want to reset password for this admin: {', '.join(selected_admin)}? (y/n): ").lower()
        if confirm != 'y':
            print("Password Reset Cancelled.")
            return manage_admin(admin)
        new_password = Admin.get_valid_password()
        new_security_phrase = input("Enter a new security phrase: ")
        admin_sec[admin_index][1] = new_password
        admin_sec[admin_index][2] = new_security_phrase
        with open("Admin Password.txt", 'w', encoding='utf-8') as file:
            file.write(','.join(headers) + '\n')
            for row in admin_sec:
                file.write(','.join(row) + '\n')
        print("Password reset successfully.")
        while True:
            continue_choice = input("Do you want to reset another password? (y/n): ").lower()
            if continue_choice == 'y':
                return password_reset_admin(admin)
            elif continue_choice == 'n':
                return manage_admin(admin)
            else:
                print("Invalid choice. Please try again.")
    except FileNotFoundError:
        print("file not found")
        return manage_admin(admin)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return manage_admin(admin)


#//ANCHOR - Staff Management Section:










#@Staff Section:
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
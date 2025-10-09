import os
import time
import datetime

#@ File Handling:
admin_file_C = "Admin Cred.txt"
staff_file_C = "Staff Cred.txt"
member_file_C = "Member Cred.txt"
admin_file_P = "Admin Password.txt"
staff_file_P = "Staff Password.txt"
member_file_P = "Member Password.txt"

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
            break
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
    special_characters = ["!","#","$","%","^","&","*","(",")",",",".","?","\"",":","{","}","|","<",">","-"]
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not any(char.islower() for char in password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not any(char.isdigit() for char in password):
        print("Password must contain at least one digit.")
        return False
    if not any(char in special_characters for char in password):
        print("Password must contain at least one special character.")
        return False
    return True

#@General Utility Functions:
def get_valid_password():
    while True:
        password = input("Enter new password: ")
        if not password_making(password):
            continue
        return password

def get_valid_contact(cred_files=None):
    if cred_files is None:
        cred_files = [admin_file_C, staff_file_C, member_file_C]
    while True:
        input_contact = input("Enter contact number: ")
        exists = False
        for cred_file in cred_files:
            if os.path.exists(cred_file) and os.path.getsize(cred_file) > 0:
                with open(cred_file, "r", encoding="utf-8") as file:
                    next(file)
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                            _, _, stored_contact = parts
                        if input_contact == stored_contact:
                            exists = True
                            break
            if exists:
                break
        if exists:
            print("Contact number already exists. Please enter a different number.")
            continue
        if len(input_contact) != 10 or not input_contact.isdigit():
            print("Invalid contact number. Please enter a 10-digit number.")
            continue
        return input_contact

#@Get Valid Name Function:
def get_valid_name():
        while True:
            name = input("Enter name: ")
            if any(char.isdigit() for char in name) or not name.replace(" ", "").isalpha():
                print("Invalid username. It must not contain numbers or special characters.")
                continue
            return name

#@Admin Class: //ANCHOR : Admin Class:
class Admin:
    def __init__(self, admin_id, password, sec_phrase, name=None, contact=None):
        self.admin_id = admin_id
        self.password = password
        self.Sec_Phrase = sec_phrase
        self.name = name
        self.contact = contact

    def verify_password(stored_id, input_password):
        try:
            if os.path.exists(admin_file_P) and os.path.getsize(admin_file_P) > 0:
                with open(admin_file_P, "r", encoding="utf-8") as file:
                    next(file)
                    for line in file:
                        stored_id, stored_password, *_ = line.strip().split(',')
                        if stored_id == stored_id and stored_password == input_password:
                            return True
            return False
        except FileNotFoundError:
            print("Admin password file not found.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

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
        except Exception as e:
            print(f"An unexpected error occurred during password verification: {e}")
            return False
        
    @staticmethod
    def admin_id_generator():
        """Generate a new Admin ID."""
        if os.path.exists(admin_file_C) and os.path.getsize(admin_file_C) > 0:
            with open(admin_file_C, "r", encoding="utf-8") as file:
                next(file)
                num_users = len(file.readlines())
            new_admin_id = str(num_users + 1).zfill(5)
        else:
            new_admin_id = "00001"
        print(f"Generated Admin ID: {new_admin_id}")
        return new_admin_id
            
    @staticmethod
    def credential_verification(input_id, input_password, sec_phrase):
        input_id = input_id
        input_password = input_password
        sec_phrase = sec_phrase
        if os.path.exists(admin_file_P) and os.path.getsize(admin_file_P) > 0:
            with open(admin_file_P, "r", encoding='utf-8') as file:
                next(file)
                for line in file:
                    stored_id, stored_password, stored_phrase = line.strip().split(',')
                    if input_id == stored_id and input_password == stored_password and sec_phrase == stored_phrase:
                        print("Credentials verified successfully.")
                        return True
            print("Invalid Admin ID or Password.")
        return False
    
    @staticmethod
    def admin_table():
        try:
            with open(admin_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                admin_data = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ]
                if not admin_data:
                    print("No data to be displayed")
            headers = (f"|{headers[0]:10} | {headers[1]:<15} | {headers[2]:<20}|")
            print(headers)
            print(len(headers)*"-")
            for row in admin_data:
                print(f"|{row[0]:<10} | {row[1]:<15} | {row[2]:<20}|")
            print(len(headers)*"-")
        except FileNotFoundError:
            print(f"Error: '{admin_file_C}' file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    #ANCHOR - Staff Management Section:

    def StaffID_Generator():
        if os.path.exists(staff_file_C) and os.path.getsize(staff_file_C) > 0:
            with open(staff_file_C, "r",encoding="utf-8") as file:
                next(file)
                num_users = len(file.readlines())
            new_staff_id = str(num_users + 1).zfill(5)
        else:
            new_staff_id = "00001"
        print(f"Generated Staff ID: {new_staff_id}")
        return new_staff_id
    #!SECTION - Staff Table Function:

    @staticmethod
    def staff_table():
        try:
            with open(staff_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                staff_data = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ]
                if not staff_data:
                    print("No data to be displayed")
            headers = (f"|{headers[0]:10} | {headers[1]:<15} | {headers[2]:<20}|")
            print(headers)
            print(len(headers)*"-")
            for row in staff_data:
                print(f"|{row[0]:<10} | {row[1]:<15} | {row[2]:<20}|")
            print(len(headers)*"-")
        except FileNotFoundError:
            print(f"Error: '{staff_file_C}' file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

#@Member Class://ANCHOR : Member Class:
class member:
#@View Members Function:
    def member_table():
        try:
            with open(member_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                member_data = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ]
            if not member_data:
                print("No data to be displayed")
            headers = (f"|{headers[0]:10} | {headers[1]:<15} | {headers[2]:<20}|")
            print(headers)
            print(len(headers)*"-")
            for row in member_data:
                print(f"|{row[0]:<10} | {row[1]:<15} | {row[2]:<20}|")
        except FileNotFoundError:
            print(f"Error: '{member_file_C}' file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

#@Add Member Function:
    def add_member():
        try:
            print("Member Registration")
            name = get_valid_name()
            password = get_valid_password()
            contact = get_valid_contact()
            security_phrase = input("Enter a security phrase: ")
            member_id = member.member_id_generator()
            if not os.path.exists(member_file_C) or os.path.getsize(member_file_C) == 0:
                with open(member_file_C, "a", newline="\n", encoding="utf-8") as file:
                    file.write("MemberID,Name,Contact\n")
            with open(member_file_C, "a", newline="\n", encoding="utf-8") as file:
                    file.write(f"{member_id},{name},{contact}\n")
            if not os.path.exists(member_file_P) or os.path.getsize(member_file_P) == 0:
                with open(member_file_P, "a", newline="\n", encoding="utf-8") as file:
                    file.write("MemberID,Password,Security_Question\n")
            with open(member_file_P, "a", newline="\n", encoding="utf-8") as file:
                file.write(f"{member_id},{password},{security_phrase}\n")
            member.view_members()
            print(f"Member account set successfully for Member ID: {member_id}")
            while True:
                continue_choice = input("Do you want to register another member? (y/n): ").lower()
                if continue_choice == 'y':
                    return member.add_member()
                elif continue_choice == 'n':
                    return manage_members()
        except FileNotFoundError:
            print("Error: Member credential file not found. Please contact system administrator.")
        except Exception as e:
            print(f"An unexpected error occurred during member registration: {e}")

#@Remove Member Function:
    def remove_member():
        while True:
            member.view_members()
            with open(member_file_P, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                member_sec = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
            with open(member_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                member_cred = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
            selected_member = input("\nEnter Member ID to reset password (or type 'cancel' to abort): ").strip()
            member_index = -1
            member_index_cred = -1
            for index, line in enumerate(member_sec):
                if line[0] == selected_member:
                    member_index_sec = index
            for index, line in enumerate(member_cred):
                if line[0] == selected_member:
                    member_index_cred = index
                    break
            for index, line in enumerate(member_sec):
                if line[0] == selected_member:
                    member_index = index
            if selected_member.lower().strip() == 'cancel':
                print("Reset canceled.")
                return manage_members()
            if member_index == -1:
                print("No matching ID found.")
            else:
                selected_member_row = member_cred[member_index_cred]
                confirm = input(f"Are you sure you want to delete this member: {', '.join(selected_member_row)}? (y/n): ").lower()
                if confirm != 'y':
                    print("Deletion canceled.")
                    return manage_members()
                member_cred.pop(member_index_cred)
                member_sec.pop(member_index_sec)

                with open(member_file_C, 'w', encoding='utf-8') as file:
                    file.write(','.join(headers) + '\n')
                    for row in member_cred:
                        file.write(','.join(row) + '\n')

                with open(member_file_P, 'w', encoding='utf-8') as file:
                    file.write(','.join(headers) + '\n')
                    for row in member_sec:
                        file.write(','.join(row) + '\n')
                print("Member removed successfully.")
                while True:
                    continue_choice = input("Do you want to register delete member? (y/n): ").lower()
                    if continue_choice == 'y':
                        return member.remove_member()
                    elif continue_choice == 'n':
                        return manage_members()

#@Password Reset Member Function:
    def password_reset_member():
        while True:
            member.view_members()
            with open(member_file_P, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                member_sec = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
            with open(member_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                member_cred = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
                selected_member = input("\nEnter Member ID to reset password (or type 'cancel' to abort): ").strip()
                member_index = -1
                for index, line in enumerate(member_sec):
                    if line[0] == selected_member:
                        member_index = index
                if selected_member == 'cancel':
                    print("Reset canceled.")
                    return manage_members()
                if member_index == -1:
                    print("No matching ID found.")
                else:
                    selected_member = member_cred[member_index]
                    confirm = input(f"Are you sure you want to reset password for this member: {', '.join(selected_member)}? (y/n): ").lower()
                    if confirm != 'y':
                        print("Password Reset Cancelled.")
                        return manage_members()
                    new_password = get_valid_password()
                    new_security_phrase = input("Enter a new security phrase: ")
                    member_sec[member_index][1] = new_password
                    member_sec[member_index][2] = new_security_phrase
                    with open(member_file_P, 'w', encoding='utf-8') as file:
                        file.write(','.join(headers) + '\n')
                        for row in member_sec:
                            file.write(','.join(row) + '\n')
                    print("Password reset successfully.")
                    while True:
                        continue_choice = input("Do you want to reset another password? (y/n): ").lower()
                        if continue_choice == 'y':
                            return member.password_reset_member()
                        elif continue_choice == 'n':
                            return manage_members()
                        else:
                            print("Invalid choice. Please try again.")

    def view_members(admin):
        while True:
            member.member_table()
            input("Press Enter to continue...")
            return manage_members(admin)
        
#@Member ID Generator Function:
    @staticmethod
    def member_id_generator():
        if os.path.exists(member_file_C) and os.path.getsize(member_file_C) > 0:
            with open(member_file_C, "r",encoding="utf-8") as file:
                next(file)
                num_users = len(file.readlines())
            new_member_id = str(num_users + 1).zfill(5)
        else:
            new_member_id = "00001"
        print(f"Generated Member ID: {new_member_id}")
        return new_member_id


#@Administrator Section: //ANCHOR : Administrator Section:

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
        print("Error: Admin credential file not found. Please contact system administrator.")
        return main_menu()
    except Exception as e:
        print(f"An unexpected error occurred during admin login: {e}")
        return main_menu()

        
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
        Admin.admin_table()
        input("Press Enter to continue...")
        return manage_admin(admin)

#@ Add Admin Function:
def add_admin(admin):
    while True:
        try:
            print("Admin Registration")
            name = get_valid_name()
            password = get_valid_password()
            contact = get_valid_contact()
            security_phrase = input("Enter a security phrase: ")
            admin_id = Admin.admin_id_generator()
            if not os.path.exists(admin_file_C) or os.path.getsize(admin_file_C) == 0:
                with open(admin_file_C, "a", newline="\n", encoding="utf-8") as file:
                    file.write("AdminID,Name,Contact\n")
            with open(admin_file_C, "a", newline="\n", encoding="utf-8") as file:
                file.write(f"{admin_id},{name},{contact}\n")
            if not os.path.exists(admin_file_P) or os.path.getsize(admin_file_P) == 0:
                with open(admin_file_P, "a", newline="\n", encoding="utf-8") as file:
                    file.write("AdminID,Password,Security_Question\n")
            with open(admin_file_P, "a", newline="\n", encoding="utf-8") as file:
                file.write(f"{admin_id},{password},{security_phrase}\n")
            Admin.admin_table()
            print(f"Admin account set successfully for Admin ID: {admin_id}")
            while True:
                continue_choice = input("Do you want to register another admin? (y/n): ").lower()
                if continue_choice == 'y':
                    return add_admin(admin)
                elif continue_choice == 'n':
                    return manage_admin(admin)
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
#@ Remove Admin Function:
def remove_admin(admin):
    while True:
        Admin.admin_table()
        with open(admin_file_P, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_sec = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        with open(admin_file_C, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_cred = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        selected_admin = input("\nEnter Admin ID to reset password (or type 'cancel' to abort): ").strip()
        admin_index = -1
        admin_index_cred = -1
        for index, line in enumerate(admin_sec):
            if line[0] == selected_admin:
                admin_index_sec = index
        for index, line in enumerate(admin_cred):
            if line[0] == selected_admin:
                admin_index_cred = index
                break
        for index, line in enumerate(admin_sec):
            if line[0] == selected_admin:
                admin_index = index
        if selected_admin.lower().strip() == 'cancel':
            print("Reset canceled.")
            return manage_admin(admin)
        if admin_index == -1:
            print("No matching ID found.")
        else:
            selected_admin_row = admin_cred[admin_index_cred]
            confirm = input(f"Are you sure you want to delete this admin: {', '.join(selected_admin_row)}? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return manage_admin(admin)
            admin_cred.pop(admin_index_cred)
            admin_sec.pop(admin_index_sec)

            with open(admin_file_C, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in admin_cred:
                    file.write(','.join(row) + '\n')
            
            with open(admin_file_P, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in admin_sec:
                    file.write(','.join(row) + '\n')
            print("Admin removed successfully.")
            while True:
                continue_choice = input("Do you want to register delete admin? (y/n): ").lower()
                if continue_choice == 'y':
                    return remove_admin(admin)
                elif continue_choice == 'n':
                    return manage_admin(admin)
    
#@ Password Reset Function:
def password_reset_admin(admin):
    while True:
        Admin.admin_table()
        with open(admin_file_P, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_sec = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        with open(admin_file_C, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_cred = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
            selected_admin = input("\nEnter Admin ID to reset password (or type 'cancel' to abort): ").strip()
            admin_index = -1
            for index, line in enumerate(admin_sec):
                if line[0] == selected_admin:
                    admin_index = index
            if selected_admin == 'cancel':
                print("Reset canceled.")
                return manage_admin(admin)
            if admin_index == -1:
                print("No matching ID found.")
            else:
                selected_admin = admin_cred[admin_index]
                confirm = input(f"Are you sure you want to reset password for this admin: {', '.join(selected_admin)}? (y/n): ").lower()
                if confirm != 'y':
                    print("Password Reset Cancelled.")
                    return manage_admin(admin)
                new_password = Admin.get_valid_password()
                new_security_phrase = input("Enter a new security phrase: ")
                admin_sec[admin_index][1] = new_password
                admin_sec[admin_index][2] = new_security_phrase
                with open(admin_file_P, 'w', encoding='utf-8') as file:
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

#ANCHOR - Staff Management Section:

def manage_staff(admin):
    while True:
        print("Staff Management")
        print("1. View Staff")
        print("2. Add Staff")
        print("3. Remove Staff")
        print("4. Reset Password")
        print("5. Previous Menu")
        print('6. Logout')
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            return view_staff(admin)
        elif choice == '2':
            return add_staff(admin)
        elif choice == '3':
            return remove_staff(admin)
        elif choice == '4':
            return password_reset_staff(admin)
        elif choice == '5':
            return admin_menu(admin)
        elif choice == '6':
            print("Logging Out")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

def view_staff(admin):
    while True:
        print("View Staff - Functionality to be implemented")
        Admin.staff_table()
        input("Press Enter to continue...")
        return manage_staff(admin)
    
def add_staff(admin):
    while True:
        try:
            print("Staff Registration")
            name = Admin.get_valid_name()
            password = Admin.get_valid_password()
            contact = Admin.get_valid_contact()
            security_phrase = input("Enter a security phrase: ")
            staff_id = Admin.StaffID_Generator()
            if not os.path.exists(staff_file_C) or os.path.getsize(staff_file_C) == 0:
                with open(staff_file_C, "a", newline="\n", encoding="utf-8") as file:
                    file.write("StaffID,Name,Contact\n")
            with open(staff_file_C, "a", newline="\n", encoding="utf-8") as file:
                    file.write(f"{staff_id},{name},{contact}\n")
            if not os.path.exists(staff_file_P) or os.path.getsize(staff_file_P) == 0:
                with open(staff_file_P, "a", newline="\n", encoding="utf-8") as file:
                    file.write("StaffID,Password,Security_Question\n")
            with open(staff_file_P, "a", newline="\n", encoding="utf-8") as file:
                file.write(f"{staff_id},{password},{security_phrase}\n")
            Admin.staff_table()
            print(f"Staff account set successfully for Staff ID: {staff_id}")
            while True:
                continue_choice = input("Do you want to register another staff member? (y/n): ").lower()
                if continue_choice == 'y':
                    return add_staff(admin)
                elif continue_choice == 'n':
                    return manage_staff(admin)
        except FileNotFoundError:
            print("Error: Staff credential file not found. Please contact system administrator.")
        except Exception as e:
            print(f"An unexpected error occurred during staff registration: {e}")

def remove_staff(admin):
    while True:
        Admin.staff_table()
        with open(staff_file_P, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                staff_sec = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
        with open(staff_file_C, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                staff_cred = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
        selected_staff = input("\nEnter Staff ID to reset password (or type 'cancel' to abort): ").strip()
        staff_index = -1
        staff_index_cred = -1
        for index, line in enumerate(staff_sec):
            if line[0] == selected_staff:
                staff_index_sec = index
        for index, line in enumerate(staff_cred):
            if line[0] == selected_staff:
                staff_index_cred = index
                break
        for index, line in enumerate(staff_sec):
            if line[0] == selected_staff:
                staff_index = index
        if selected_staff.lower().strip() == 'cancel':
            print("Reset canceled.")
            return manage_staff(admin)
        if staff_index == -1:
            print("No matching ID found.")
        else:
            selected_staff_row = staff_cred[staff_index_cred]
            confirm = input(f"Are you sure you want to delete this staff: {', '.join(selected_staff_row)}? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return manage_staff(admin)
            staff_cred.pop(staff_index_cred)
            staff_sec.pop(staff_index_sec)

            with open(staff_file_C, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in staff_cred:
                    file.write(','.join(row) + '\n')

            with open(staff_file_P, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in staff_sec:
                    file.write(','.join(row) + '\n')
            print("Staff removed successfully.")
            while True:
                continue_choice = input("Do you want to register delete staff? (y/n): ").lower()
                if continue_choice == 'y':
                    return remove_staff(admin)
                elif continue_choice == 'n':
                    return manage_staff(admin)

def password_reset_staff(admin):
    while True:
        Admin.staff_table()
        with open(staff_file_P, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            staff_sec = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
            ]
        with open(staff_file_C, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            staff_cred = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
            ]
        selected_staff = input("\nEnter Staff ID to reset password (or type 'cancel' to abort): ").strip()
        staff_index = -1
        for index, line in enumerate(staff_sec):
            if line[0] == selected_staff:
                staff_index = index
        if selected_staff == 'cancel':
            print("Reset canceled.")
            return manage_staff(admin)
        if staff_index == -1:
            print("No matching ID found.")
        else:
            selected_staff = staff_cred[staff_index]
            confirm = input(f"Are you sure you want to reset password for this staff: {', '.join(selected_staff)}? (y/n): ").lower()
            if confirm != 'y':
                print("Password Reset Cancelled.")
                return manage_staff(admin)
            new_password = Admin.get_valid_password()
            new_security_phrase = input("Enter a new security phrase: ")
            staff_sec[staff_index][1] = new_password
            staff_sec[staff_index][2] = new_security_phrase
            with open(staff_file_P, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in staff_sec:
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

#ANCHOR - Member Management Section:
def manage_members(admin):
    while True:
        print("Member Management")
        print("1. View Members")
        print("2. View Members logs")
        print("3. Add Member")
        print("4. Remove Member")
        print("5. Reset Password")
        print("6. Previous Menu")
        print('7. Logout')
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            return member.view_members(admin)
        elif choice == '2':
            return member.view_member_logs(admin)
        elif choice == '3':
            return member.add_member(admin)
        elif choice == '4':
            return member.remove_member(admin)
        elif choice == '5':
            return member.password_reset_member(admin)
        elif choice == '6':
            return admin_menu(admin)
        elif choice == '7':
            print("Logging Out")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")






































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
    main_menu()
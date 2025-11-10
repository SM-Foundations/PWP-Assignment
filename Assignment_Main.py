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
repository = "Book_Collection.txt"
BookLog = "Book_Logs.txt"

##NOTE##
#@ Master Credentials for all users are as follows: 1,1,1 @#

#@Main Menu Function do not delete or modify this function
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
            staff_login() #Incomplete function
        elif choice == '3':
            member_login()
        elif choice == '4':
            guest_access() #Incomplete function
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

##################################################################################################
#@ Extra Functions: @#
##################################################################################################
#lockout Function:
def lockout(locked_out):
    while True:
        current_time = datetime.datetime.now()
        remaining_time = int((locked_out - current_time).total_seconds())
        if remaining_time <= 0:
            break
        print(f"Too many incorrect attempts. Please wait {remaining_time} seconds.", end='\r')
        time.sleep(1)
        return main_menu()
        
##################################################################################################
#@General Utility Functions:
##################################################################################################
#@ Password Making Function:
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

#@ Get Valid Password Function:
def get_valid_password():
    while True:
        password = input("Enter new password: ")
        if not password_making(password):
            continue
        return password

#@ Get Valid Contact Function:
def get_valid_contact():
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
                            continue
        if exists:
            print("Contact number already exists. Please enter a different number.")
            continue
        if len(input_contact) != 10 or not input_contact.isdigit():
            print("Invalid contact number. Please enter a 10-digit number.")
            continue
        return input_contact

#@ Get Valid Name Function:
def get_valid_name():
        while True:
            name = input("Enter name: ")
            if any(char.isdigit() for char in name) or not name.replace(" ", "").isalpha():
                print("Invalid username. It must not contain numbers or special characters.")
                continue
            return name
        
###################################################################################################
#@ ADMIN : Admin Management Section: @# --Master ID, password and security phrase: 1, 1, 1
###################################################################################################
#@Admin Menu Function:
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
            if reverify_password(admin):
                return manage_admin(admin)
        elif choice == '2':
            if reverify_password(admin):
                return manage_staff(admin)
        elif choice == '3':
            if reverify_password(admin):
                return manage_members(admin)
        elif choice == '4':
            if reverify_password(admin):
                return manage_repository(admin)
        elif choice == '5':
            print("Logging out.")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

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
    admin_table()
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
            admin_id = admin_id_generator()
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
            admin_table()
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
        admin_table()
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
        if selected_admin.strip() == 'cancel':
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
        admin_table()
        with open(admin_file_P, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            admin_sec = [
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
                selected_admin = admin_sec[admin_index]
                confirm = input(f"Are you sure you want to reset password for this admin: {selected_admin[0]}? (y/n): ").lower()
                if confirm != 'y':
                    print("Password Reset Cancelled.")
                    return manage_admin(admin)
                new_password = get_valid_password()
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

#@Reverify Admin Password Function:
def reverify_password(admin):
    try:
        attempts = 3
        if os.path.exists(admin_file_P) and os.path.getsize(admin_file_P) > 0:
            with open(admin_file_P, "r", encoding="utf-8") as file:
                next(file)
                for line in file:
                    _, stored_password, Sec_Phrase = line.strip().split(',')
                    while attempts > 0:
                        input_password = input("Re-enter password for verification: ")
                        input_phrase = input("Re-enter your security phrase: ")
                        if input_password == stored_password and input_phrase == Sec_Phrase:
                            return True
                        else:
                            attempts -= 1
                            print(f"Incorrect password or security phrase. You have {attempts} attempts left.")
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return admin_menu(admin)
    except Exception as e:
        print(f"An unexpected error occurred during password verification: {e}")
        return False

#@Admin ID Generator Function:
def admin_id_generator(): #Generate a new Admin ID.
    if os.path.exists(admin_file_C) and os.path.getsize(admin_file_C) > 0: 
        with open(admin_file_C, "r", encoding="utf-8") as file:
            next(file)
            num_users = len(file.readlines())
        new_admin_id = str(num_users + 1).zfill(5)
    else:
        new_admin_id = "00001"
    print(f"Generated Admin ID: {new_admin_id}")
    return new_admin_id
        
#@Credential Verification Function:
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

#@View Admin Functions:
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
        max_len = [max(len(row[i]) for row in admin_data + [headers]) for i in range(len(headers))]
        headers = (f"|{headers[0]:^10} | {headers[1]:^{max_len[1]}} | {headers[2]:^20}|")
        print(len(headers)*"-")
        print(headers)
        print(len(headers)*"-")
        for row in admin_data:
            print(f"|{row[0]:^10} | {row[1]:^{max_len[1]}} | {row[2]:^20}|")
        print(len(headers)*"-")
    except FileNotFoundError:
        print(f"Error: '{admin_file_C}' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#@ Admin Login Function:
def admin_login():
    try:
        attempts = 3
        locked_out = None 
        while attempts > 0:
            print("Admin Login")
            input_id = input("Enter Admin ID: ")
            input_password = input("Enter Password: ")
            sec_phrase = input("Enter Security Phrase: ")
            if credential_verification(input_id, input_password, sec_phrase):
                admin = (input_id,input_password,sec_phrase)
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

##############################################################################################
#@ ADMIN: Staff Management Section: @# 
##############################################################################################
#@Staff Management Menu Function:
def manage_staff(admin):
    while True:
        print("Staff Management")
        print("1. View Staff")
        print("2. Add Staff")
        print("3. Remove Staff")
        print("4. Reset Password")
        print("5. Previous Menu")
        print('6. Logout')
        choice = input("Enter your choice (1-6): ")
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

#@Staff ID Generator Function:
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

#@Staff Table Function:
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
        max_len = [max(len(row[i]) for row in staff_data + [headers]) for i in range(len(headers))]
        headers = (f"|{headers[0]:^10} | {headers[1]:^{max_len[1]}} | {headers[2]:^20}|")
        print(len(headers)*"-")
        print(headers)
        print(len(headers)*"-")
        for row in staff_data:
            print(f"|{row[0]:^10} | {row[1]:^{max_len[1]}} | {row[2]:^20}|")
        print(len(headers)*"-")
    except FileNotFoundError:
        print(f"Error: '{staff_file_C}' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#@ View Staff Functions:
def view_staff(admin):
    print("View Staff")
    staff_table()
    input("Press Enter to continue...")
    return manage_staff(admin)

#@ Add Staff Function: 
def add_staff(admin):
    while True:
        try:
            print("Staff Registration")
            name = get_valid_name()
            password = get_valid_password()
            contact = get_valid_contact()
            security_phrase = input("Enter a security phrase: ")
            staff_id = StaffID_Generator()
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
            staff_table()
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

#@ Remove Staff Function:
def remove_staff(admin):
    while True:
        staff_table()
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

#@ Password Reset Staff Function:
def password_reset_staff(admin):
    while True:
        staff_table()
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
            new_password = get_valid_password()
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

##################################################################################################
#@ ADMIN: Member Member Section: @#
##################################################################################################
#@ Member Manager Menu Function:
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
            view_members(admin)
        elif choice == '2':
            view_member_logs(admin)
        elif choice == '3':
            add_member(admin)
        elif choice == '4':
            remove_member(admin)
        elif choice == '5':
            password_reset_member(admin)
        elif choice == '6':
            admin_menu(admin)
        elif choice == '7':
            print("Logging Out")
            main_menu()
        else:
            print("Invalid choice. Please try again.")
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
        max_len = [max(len(row[i]) for row in member_data + [headers]) for i in range(len(headers))]
        headers = (f"|{headers[0]:^10} | {headers[1]:^{max_len[1]}} | {headers[2]:^20}|")
        print(len(headers)*"-")
        print(headers)
        print(len(headers)*"-")
        for row in member_data:
            print(f"|{row[0]:^10} | {row[1]:^{max_len[1]}} | {row[2]:^20}|")
        print(len(headers)*"-")
    except FileNotFoundError:
        print(f"Error: '{member_file_C}' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#@Add Member Function:
def add_member(admin):
    try:
        print("Member Registration")
        name = get_valid_name()
        password = get_valid_password()
        contact = get_valid_contact()
        security_phrase = input("Enter a security phrase: ")
        member_id = member_id_generator()
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
        member_table()
        print(f"Member account set successfully for Member ID: {member_id}")
        while True:
            continue_choice = input("Do you want to register another member? (y/n): ").lower()
            if continue_choice == 'y':
                return add_member(admin)
            elif continue_choice == 'n':
                return manage_members(admin)
    except FileNotFoundError:
        print("Error: Member credential file not found. Please contact system administrator.")
    except Exception as e:
        print(f"An unexpected error occurred during member registration: {e}")

#@Remove Member Function:
def remove_member(admin):
    while True:
        member_table()
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
            return manage_members(admin)
        if member_index == -1:
            print("No matching ID found.")
        else:
            selected_member_row = member_cred[member_index_cred]
            confirm = input(f"Are you sure you want to delete this member: {', '.join(selected_member_row)}? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return manage_members(admin)
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
                    return remove_member(admin)
                elif continue_choice == 'n':
                    return manage_members(admin)

#@Password Reset Member Function:
def password_reset_member(admin):
    while True:
        member_table()
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
                return manage_members(admin)
            if member_index == -1:
                print("No matching ID found.")
            else:
                selected_member = member_cred[member_index]
                confirm = input(f"Are you sure you want to reset password for this member: {', '.join(selected_member)}? (y/n): ").lower()
                if confirm != 'y':
                    print("Password Reset Cancelled.")
                    return manage_members(admin)
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
                        return password_reset_member(admin)
                    elif continue_choice == 'n':
                        return manage_members(admin)
                    else:
                        print("Invalid choice. Please try again.")

def view_members(admin):
    member_table()
    input("Press Enter to continue...")
    return manage_members(admin)
    
#@Member ID Generator Function:
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

#@View Member Logs Function:
def view_member_logs(admin):
    try:
        print(f"Member Book History:")
        member_table()
        selected_member_id = input("Enter Member ID to view book history: ").strip()
        with open(BookLog, "r", encoding="utf-8") as log_file:
            lines = log_file.readlines()
            filtered_log_lines = []
            headers = lines[0].strip().split(',')
            BookLog_Data = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
                ]
            if not BookLog_Data:
                print("No data to be displayed")
            for row in BookLog_Data:
                if row[0] == selected_member_id:
                    filtered_log_lines.append(row)
            max_length = [max(len(row[i]) for row in filtered_log_lines + [headers]) for i in range(len(headers))]
            headers = (f"|{headers[0]:^10}|{headers[1]:^10}|{headers[2]:^{max_length[2]+1}}|{headers[3]:^15}|{headers[4]:^15}|{headers[5]:^15}|")
            print(len(headers)*"-")
            print(headers)
            print(len(headers)*"-")
            for row in filtered_log_lines:
                print(f"|{row[0]:^10}|{row[1]:^10}|{row[2]:^{max_length[2]+1}}|{row[3]:^15}|{row[4]:^15}|{row[5]:^15}|")
            print(len(headers)*"-")
        input("Press Enter to continue...")
        return manage_members(admin)
    except FileNotFoundError:  
        print("Error: Book Logs file not found.")
        return manage_members(admin)
    except Exception as e:
        print(f"An unexpected error occurred while viewing book history: {e}")
        return manage_members(admin)

##################################################################################################
#@ Repository Management Function:
##################################################################################################
#@ Repository Management Menu Function:
def manage_repository(admin):
    while True:
        print("Repository Management")
        print("1. View Repository")
        print("2. Add to Repository")
        print("3. Remove from Repository")
        print("4. Book Logs")
        print("5. Previous Menu")
        print('6. Logout')
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            return view_repository(admin)
        elif choice == '2':
            return add_repository(admin)
        elif choice == '3':
            return remove_book(admin)
        elif choice == '4':
            return view_book_logs(admin)
        elif choice == '5':
            return admin_menu(admin)
        elif choice == '6':
            print("Logging Out")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

#@ Repository Table Function:
def repository_table():
    try:
        with open(repository, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            repository_data = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
            ]
            if not repository_data:
                print("No data to be displayed")
        max_length = [max(len(row[i]) for row in repository_data + [headers]) for i in range(len(headers))]
        headers = (f"|{headers[0]:^10} | {headers[1]:^15} | {headers[2]:^{max_length[2]+1}}| {headers[3]:^20}| {headers[4]:^20}|")
        print(len(headers)*"-")
        print(headers)  
        print(len(headers)*"-")
        for row in repository_data:
            print(f"|{row[0]:^10} | {row[1]:^15} | {row[2]:<{max_length[2]+1}}| {row[3]:^20}| {row[4]:^20}|")
        print(len(headers)*"-")
    except FileNotFoundError:
        print(f"Error: '{staff_file_C}' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#@ ISBN Checker Function:
def isbn_checker(isbn):
    while not (isbn.isdigit() and len(isbn) == 13):
        print("Invalid ISBN. Please enter a 13-digit numeric ISBN.")
        isbn = input("Enter ISBN (13 digits): ")
    return isbn

#@Book ID Generator Function:
def book_id_generator():
    if os.path.exists(repository) and os.path.getsize(repository) > 0:
        with open(repository, "r",encoding="utf-8") as file:
            next(file)
            num_books = len(file.readlines())
        new_book_id = "B" + str(num_books + 1).zfill(4)
    else:
        new_book_id = ("B"+ "0001")
    print(f"Generated Book ID: {new_book_id}")
    return new_book_id

#@ View Repository Function:
def view_repository(admin): 
    repository_table()
    input("Press Enter to continue...")
    return manage_repository(admin)

#@ Add Repository Function:
def add_repository(admin):
    try:
        while True:
            print("Add to Repository")
            print("Type 'cancel' at any prompt to cancel the operation.")
            bookID = book_id_generator()
            isbn = isbn_checker(input("Enter ISBN (13 digits): "))
            name = input("Enter Book Name: ")
            category = input("Enter Book Category: ")
            Availability = 'Available'
            new_book = f"{bookID},{isbn},{name},{category},{Availability}\n"
            if not os.path.exists(repository) or os.path.getsize(repository) == 0:
                with open(repository, "a", newline="\n", encoding="utf-8") as file:
                    file.write("BookID,ISBN,Name,Category,Availability\n")
            with open(repository, "a", newline="\n", encoding="utf-8") as file:
                file.write(new_book)
            print("Book added to repository successfully.")
            while True:
                continue_choice = input("Do you want to add another book? (y/n): ").lower()
                if continue_choice == 'y':
                    return add_repository(admin)
                elif continue_choice == 'n':
                    return manage_repository(admin)
                else:
                    print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred while adding to the repository: {e}")
        return manage_repository(admin)

#@ Remove Repository Function:
def remove_book(admin):
    while True:
        repository_table()
        with open(repository, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            book_data = [
                    line.strip().split(',')
                    for line in lines[1:]
                    if len(line.strip().split(',')) == len(headers)
                ] 
        selected_book = input("\nEnter Book ID to remove (or type 'cancel' to abort): ").strip()
        book_index = -1
        for index, line in enumerate(book_data):
            if line[0] == selected_book:
                book_index = index
        if selected_book.lower().strip() == 'cancel':
            print("Removal canceled.")
            return manage_repository()
        if book_index == -1:
            print("No matching Book ID found.")
        else:
            selected_book_row = book_data[book_index]
            confirm = input(f"Are you sure you want to delete this book: {', '.join(selected_book_row)}? (y/n): ").lower()
            if confirm != 'y':
                print("Deletion canceled.")
                return manage_repository()
            book_data.pop(book_index)

            with open(repository, 'w', encoding='utf-8') as file:
                file.write(','.join(headers) + '\n')
                for row in book_data:
                    file.write(','.join(row) + '\n')
            print("Book removed successfully.")
            while True:
                continue_choice = input("Do you want to remove another book? (y/n): ").lower()
                if continue_choice == 'y':
                    return remove_book(admin)
                elif continue_choice == 'n':
                    return manage_repository(admin)

#@ Book Logs Function:
def view_book_logs(admin):
    try:
        with open(BookLog, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            BookLog_Data = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
            ]
            if not BookLog_Data:
                print("No data to be displayed")
        max_length = [max(len(row[i]) for row in BookLog_Data + [headers]) for i in range(len(headers))]
        headers = (f"|{headers[0]:^10}|{headers[1]:^10}|{headers[2]:^{max_length[2]+1}}|{headers[3]:^15}|{headers[4]:^15}|{headers[5]:^15}|")
        print(len(headers)*"-")
        print(headers)
        print(len(headers)*"-")
        for row in BookLog_Data:
            print(f"|{row[0]:^10}|{row[1]:^10}|{row[2]:<{max_length[2]+1}}|{row[3]:^15}|{row[4]:^15}|{row[5]:^15}|")
        print(len(headers)*"-")
        input("Press Enter to continue...")
        return manage_repository(admin)
    except FileNotFoundError:
        print(f"Error: '{staff_file_C}' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


##################################################################################################
#@Library Staff Section:
##################################################################################################
#Staff Login Function:
BookList = [
    {
        "BookID": "B001",
        "Title": "math textbook",
        "Author": "Chew Lee Kuen",
        "ISBN": "1234567890123",
        "Status": "Available",
        "Borrower": None,
        "IssueDate": None,
        "DueDate": None
    },
    {
        "BookID": "B002",
        "Title": "English textbook",
        "Author": "James Matthew Barrie",
        "ISBN": "0987654321123",
        "Status": "Issued",
        "Borrower": "M002",
        "IssueDate": "2025-10-20",
        "DueDate": "2025-11-03"
    }
]


def IssueBook(MemberID, BookID, IssueDate, DueDate):
    for book in BookList:
        if book["BookID"] == BookID:
            if book["Status"] == "Available":
                book["Status"] = "Issued"
                book["Borrower"] = MemberID
                book["IssueDate"] = IssueDate
                book["DueDate"] = DueDate
                print("Book issued successfully.")
            else:
                print("Book is not available.")
            return
    print("Book ID not found.")


def ReturnBook(BookID):
    for book in BookList:
        if book["BookID"] == BookID:
            if book["Status"] == "Issued":
                book["Status"] = "Available"
                book["Borrower"] = None
                book["IssueDate"] = None
                book["DueDate"] = None
                print("Book returned successfully.")
            else:
                print("Book is not currently issued.")
            return
    print("Book ID not found.")


def SearchBook(SearchType, SearchValue):
    found = False
    for book in BookList:
        if (SearchType.lower() == "title" and book["Title"].lower() == SearchValue.lower()) or \
           (SearchType.lower() == "author" and book["Author"].lower() == SearchValue.lower()) or \
           (SearchType.lower() == "isbn" and book["ISBN"] == SearchValue):
            print("\nBook Found:")
            print("Book ID:", book["BookID"])
            print("Title:", book["Title"])
            print("Author:", book["Author"])
            print("ISBN:", book["ISBN"])
            print("Status:", book["Status"])
            found = True
    if not found:
        print("No book found.")


def ReportIssuedBooks():
    print("\nList of Currently Issued Books:")
    found = False
    for book in BookList:
        if book["Status"] == "Issued":
            print("----------------------------")
            print("Book ID:", book["BookID"])
            print("Title:", book["Title"])
            print("Borrower ID:", book["Borrower"])
            print("Due Date:", book["DueDate"])
            found = True
    if not found:
        print("No books are currently issued.")


def PaymentSystem(BookID, ReturnDate):
    from datetime import datetime

    for book in BookList:
        if book["BookID"] == BookID and book["Status"] == "Issued":
            due_date = datetime.strptime(book["DueDate"], "%Y-%m-%d")
            return_date = datetime.strptime(ReturnDate, "%Y-%m-%d")
            days_late = (return_date - due_date).days

            if days_late > 0:
                fine = days_late * 1.00  # RM1 per day late
                print(f"Book is overdue by {days_late} days.")
                print(f"Total fine = RM {fine:.2f}")
            else:
                print("No fine. Returned on time.")
            return
    print("Book not found or not issued.")


def StockCheckingSystem():
    available_count = 0
    issued_count = 0

    for book in BookList:
        if book["Status"] == "Available":
            available_count += 1
        elif book["Status"] == "Issued":
            issued_count += 1

    print("\nStock Summary:")
    print("Available Books:", available_count)
    print("Issued Books:", issued_count)


def Staff_Menu():
    while True:
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Search Book")
        print("4. Report Issued Books")
        print("5. Payment System")
        print("6. Stock Checking System")
        print("7. Exit")
        print("==============================================")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            member = input("Enter Member ID: ")
            book_id = input("Enter Book ID: ")
            issue_date = input("Enter Issue Date (YYYY-MM-DD): ")
            due_date = input("Enter Due Date (YYYY-MM-DD): ")
            IssueBook(member, book_id, issue_date, due_date)

        elif choice == "2":
            book_id = input("Enter Book ID: ")
            ReturnBook(book_id)

        elif choice == "3":
            s_type = input("Search by (Title/Author/ISBN): ")
            s_value = input("Enter search value: ")
            SearchBook(s_type, s_value)

        elif choice == "4":
            ReportIssuedBooks()

        elif choice == "5":
            book_id = input("Enter Book ID: ")
            return_date = input("Enter Return Date (YYYY-MM-DD): ")
            PaymentSystem(book_id, return_date)

        elif choice == "6":
            StockCheckingSystem()

        elif choice == "7":
            print("Exiting Library System...")
            print("thanks you please come agian !")
            break

        else:
            print("Invalid choice. Please try again.")

##################################################################################################
#@ Member Section: @# @ SAEED
##################################################################################################
#@ Member Credential Verification Function:
def member_credential_verification(input_id, input_password, sec_phrase):
    input_id = input_id
    input_password = input_password
    sec_phrase = sec_phrase
    if os.path.exists(member_file_P) and os.path.getsize(member_file_P) > 0:
        with open(member_file_P, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                stored_id, stored_password, stored_phrase = line.strip().split(",")
                if (
                    input_id == stored_id
                    and input_password == stored_password
                    and sec_phrase == stored_phrase
                ):
                    print("Credentials verified successfully.")
                    return True
        print("Invalid Member ID or Password.")
    return False

#@ Member Login Function:
def member_login():
    try:
        attempts = 3
        locked_out = None
        while attempts > 0:
            print("Member Login")
            input_id = input("Enter Member ID: ")
            input_password = input("Enter Password: ")
            sec_phrase = input("Enter Security Phrase: ")
            if member_credential_verification(input_id, input_password, sec_phrase):
                member = (input_id, input_password, sec_phrase)
                print("Login successful, Welcome Member " + input_id)
                return member_menu(member)
            print(
                f"Invalid Member ID or Password. You have {attempts - 1} attempts left."
            )
            attempts -= 1
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return main_menu()
    except FileNotFoundError:
        print(
            "Error: Member credential file not found. Please contact system administrator."
        )
        return main_menu()
    except Exception as e:
        print(f"An unexpected error occurred during member login: {e}")
        return main_menu()

#@ Member Menu Function:
def member_menu(member):
    while True:
        print("Member Menu:")
        print("1. Borrow a Book")
        print("2. View Book History")
        print("3. Logout")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            return borrow_book(member)
        elif choice == "2":
            return view_member_book_history(member)
        elif choice == "3":
            print("Logging out.")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")

def borrow_book(member):
    try:
        while True:
            repository_table()
            with open(repository, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(',')
                book_data = [
                        line.strip().split(',')
                        for line in lines[1:]
                        if len(line.strip().split(',')) == len(headers)
                    ] 
            selected_book = input("\nEnter Book ID to borrow (or type 'cancel' to abort): ").strip()
            book_index = -1
            for index, line in enumerate(book_data):
                if line[0] == selected_book:
                    book_index = index
            if selected_book.lower().strip() == 'cancel':
                print("Borrowing canceled.")
                return member_menu(member)
            if book_index == -1:
                print("No matching Book ID found.")
            else:
                selected_book_row = book_data[book_index]
                confirm = input(f"Are you sure you want to borrow this book: {', '.join(selected_book_row)}? (y/n): ").lower()
                if confirm != 'y':
                    print("Borrowing canceled.")
                    return member_menu(member)
                borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")
                book_data[book_index][4] = 'Borrowed'
                book_data[book_index].append(borrow_date)
                BookLog_entry = f"{member[0]},{selected_book_row[0]},{selected_book_row[2]},{selected_book_row[3]},{borrow_date}\n"
                if not os.path.exists(BookLog) or os.path.getsize(BookLog) == 0:
                    with open(BookLog, "a", newline="\n", encoding="utf-8") as file:
                        file.write("MemberID,BookID,BookName,Category,BorrowDate\n")
                with open(BookLog, "a", newline="\n", encoding="utf-8") as file:
                    file.write(BookLog_entry)
                with open(repository, 'w', encoding='utf-8') as file:
                    file.write(','.join(headers) + '\n')
                    for row in book_data:
                        file.write(','.join(row) + '\n')
                print("Book borrowed successfully.")
                while True:
                    continue_choice = input("Do you want to borrow another book? (y/n): ").lower()
                    if continue_choice == 'y':
                        return borrow_book(member)
                    elif continue_choice == 'n':
                        return member_menu(member)
    except Exception as e:
        print(f"An error occurred while borrowing the book: {e}")
        return member_menu(member)
             
def view_member_book_history(member):
    try:
        print(f"Member {member[0]} Book History:")
        with open(BookLog, "r", encoding="utf-8") as log_file:
            lines = log_file.readlines()
            filtered_log_lines = []
            headers = lines[0].strip().split(',')
            BookLog_Data = [
                line.strip().split(',')
                for line in lines[1:]
                if len(line.strip().split(',')) == len(headers)
                ]
            if not BookLog_Data:
                print("No data to be displayed")
            for row in BookLog_Data:
                if row[0] == member[0]:
                    filtered_log_lines.append(row)
            max_length = [max(len(row[i]) for row in filtered_log_lines + [headers]) for i in range(len(headers))]
            headers = (f"|{headers[0]:^10}|{headers[1]:^10}|{headers[2]:^{max_length[2]+1}}|{headers[3]:^15}|{headers[4]:^15}|{headers[5]:^15}|")
            print(len(headers)*"-")
            print(headers)
            print(len(headers)*"-")
            for row in filtered_log_lines:
                print(f"|{row[0]:^10}|{row[1]:^10}|{row[2]:^{max_length[2]+1}}|{row[3]:^15}|{row[4]:^15}|{row[5]:^15}|")
            print(len(headers)*"-")
        input("Press Enter to continue...")
        return member_menu(member)
    except FileNotFoundError:  
        print("Error: Book Logs file not found.")
        return member_menu(member)
    except Exception as e:
        print(f"An unexpected error occurred while viewing book history: {e}")
        return member_menu(member)

#@ Member Reverify Password Function:
def member_reverify_password(member):
    try:
        attempts = 3
        if os.path.exists(member_file_P) and os.path.getsize(member_file_P) > 0:
            with open(member_file_P, "r", encoding="utf-8") as file:
                next(file)
                for line in file:
                    _, stored_password, Sec_Phrase = line.strip().split(",")
                    while attempts > 0:
                        input_password = input("Re-enter password for verification: ")
                        input_phrase = input("Re-enter your security phrase: ")
                        if (
                            input_password == stored_password
                            and input_phrase == Sec_Phrase
                        ):
                            return True
                        else:
                            attempts -= 1
                            print(
                                f"Incorrect password or security phrase. You have {attempts} attempts left."
                            )
            if attempts == 0:
                locked_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
                lockout(locked_out)
                attempts = 3
                return member_menu(member)
    except Exception as e:
        print(f"An unexpected error occurred during password verification: {e}")
        return False

##################################################################################################
#@ Guest Section:
##################################################################################################
#@ Guest Access Function:





#@ DO NOT DELETE #@
def main():
    while True:
       main_menu()
if __name__ == "__main__":
    main()
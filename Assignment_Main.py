import os
import sys
import time
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
        return "Exited Main Menu" 
#Administrator Login And Registration
"""def admin_login():
    while True
        print("Admin Login")
        username = input("Enter admin username: ") weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        password = input("Enter admin password: ")
"""








# DO NOT DELETE THE BELOW LINE OR ENTER ANYTHING BELOW THIS LINE
if __name__ == "__main__":
    main_menu()
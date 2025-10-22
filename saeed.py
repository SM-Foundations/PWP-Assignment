def login(user,password):
    with open("Admin Cred.txt") as login_file:
        first_line = login_file.readline().strip()
        header = first_line.split(",") 
        # print(header)
        name_index = header.index("Name")
        password_index = header.index("Password")   
        for line in login_file:
            user_cred = line.strip().split(",")
            if user_cred[name_index] == user and user_cred[password_index] == password:
                return header, user_cred

def borrow(name):
    pass



if __name__ == "__main__":
    name = input("Enter name: ")
    password = input("Enter Password: ")
    if logged_in := login(name, password):
        print(logged_in)
    else:
        print("Invalid credentials")



    
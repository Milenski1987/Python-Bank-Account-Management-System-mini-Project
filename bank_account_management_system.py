import json
import re
import tkinter as tk
from tkinter import ttk
import numpy as np


class ChosenNumberOutOfRange(Exception):
    pass

class InvalidUsername(Exception):
    pass

class InvalidPassword(Exception):
    pass

class MissingRequiredInformation(Exception):
    pass

class NegativeAmount(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class Forbidden(Exception):
    pass


with open("data.json") as file:
    account_holders = json.load(file)


def deposit(current_user):
    # function to deposit money to current user account
    def deposit_money():
        response = ""
        try:
            deposit_text.delete("1.0", 'end')
            amount = float(deposit_entry.get())
            if amount <= 0:
                raise NegativeAmount
        except ValueError:
            response = "Please enter valid number"
        except NegativeAmount:
            response = "Amount must be positive number"
        else:
            response = "Successful transaction"
            account_holders[current_user]['transactions'].append(f"{amount:.2f}")
            account_holders[current_user]['balance'] += float(f"{amount:.2f}")
        finally:
            deposit_text.insert(tk.END, response)

    #create deposit function window
    deposit_screen = tk.Tk()
    deposit_screen.geometry("200x200+100+500")
    deposit_screen.title("Deposit")

    deposit_label = tk.Label(deposit_screen, text="How much you want to deposit: ")
    deposit_label.pack()
    deposit_entry = tk.Entry(deposit_screen, justify="center")
    deposit_entry.pack()
    deposit_text = tk.Text(deposit_screen, width=40, height=2)
    deposit_text.pack()
    deposit_button = tk.Button(deposit_screen, text="Deposit", command=deposit_money)
    deposit_button.pack()
    deposit_button = tk.Button(deposit_screen, text="Back to Welcome screen",
                                command=lambda: deposit_screen.destroy())
    deposit_button.pack()
    deposit_screen.mainloop()


def withdraw(current_user):
    # function to withdraw money to current user account
    def withdraw_money():
        response = ""
        try:
            withdraw_text.delete("1.0", 'end')
            amount = float(withdraw_entry.get())
            if account_holders[current_user]['balance'] <= 0 or account_holders[current_user]['balance'] < amount:
                raise InsufficientFunds
            elif amount <= 0:
                raise NegativeAmount
        except InsufficientFunds:
            response = "Invalid operation. Insufficient funds!"
        except ValueError:
            response = "Please enter valid number"
        except NegativeAmount:
            response = "Amount must be positive number"
        else:
            response = "Successful transaction"
            account_holders[current_user]['transactions'].append(f"-{amount:.2f}")
            account_holders[current_user]['balance'] -= float(f"{amount:.2f}")
        finally:
            withdraw_text.insert(tk.END, response)

    # create withdraw function window
    withdraw_screen = tk.Tk()
    withdraw_screen.geometry("200x200+100+500")
    withdraw_screen.title("Withdraw")

    withdraw_label = tk.Label(withdraw_screen, text="How much you want to withdraw: ")
    withdraw_label.pack()
    withdraw_entry = tk.Entry(withdraw_screen, justify="center")
    withdraw_entry.pack()
    withdraw_text = tk.Text(withdraw_screen, width=40, height=2)
    withdraw_text.pack()
    withdraw_button = tk.Button(withdraw_screen, text="Withdraw", command=withdraw_money)
    withdraw_button.pack()
    withdraw_button = tk.Button(withdraw_screen, text="Back to Welcome screen", command= lambda: withdraw_screen.destroy())
    withdraw_button.pack()
    withdraw_screen.mainloop()


def check_balance(current_user):
    #function that checks and shows current user balance

    response = f"Current balance: {account_holders[current_user]['balance']:.2f}"
    #create balance window
    balance_screen = tk.Tk()
    balance_screen.geometry("200x200+100+500")
    balance_screen.title("Show balance")
    balance_text = tk.Text(balance_screen, width=50, height=2)
    balance_text.pack()
    balance_text.insert(tk.END, response)
    balance_button = tk.Button(balance_screen, text="Back to Welcome screen",
                                command=lambda: balance_screen.destroy())
    balance_button.pack()
    balance_screen.mainloop()


def view_transaction_history(current_user):
    #function that shows all current user transactions

    response = f'Recent transactions: \n{", ".join(list(map(str,account_holders[current_user]['transactions'])))}'
    #create transactions window
    transactions_screen = tk.Tk()
    transactions_screen.geometry("600x600+100+500")
    transactions_screen.title("Deposit")
    transactions_text = tk.Text(transactions_screen, width=60, height=15)
    transactions_text.pack()
    transactions_text.insert(tk.END, response)
    transactions_button = tk.Button(transactions_screen, text="Back to Welcome screen",
                               command=lambda: transactions_screen.destroy())
    transactions_button.pack()
    transactions_screen.mainloop()


def list_accounts():
    # function that shows all accounts

    response = f"Accounts: \n\n{'\n'.join([f'{username}:\n  '
                                       f'Balance: {account_holders[username]['balance']}\n  '
                                           f'Transactions: {', '.join(account_holders[username]['transactions'])}\n' 
                                       for username in account_holders if username != 'administrator'])}"
    # create window to view accounts
    listing_screen = tk.Tk()
    listing_screen.geometry("600x600+100+500")
    listing_screen.title("Accounts")
    listing_text = tk.Text(listing_screen, width=80, height=25)
    listing_text.pack()
    listing_text.insert(tk.END, response)
    listing_button = tk.Button(listing_screen, text="Back to ADMIN panel",
                               command=lambda: listing_screen.destroy())
    listing_button.pack()
    listing_screen.mainloop()


def remove_username():
    # function to remove username from account holders
    def remove_user():
        response = ""
        try:
            remove_text.delete("1.0", 'end')
            username = remove_entry.get()
            password = password_entry.get()
            if username == 'administrator':
                raise Forbidden
            if username not in account_holders:
                raise InvalidUsername
            if password != account_holders['administrator']['password']:
                raise InvalidPassword
        except Forbidden:
            response = "Operation not allowed."
        except InvalidUsername:
            response = f"{username} doesn't exist"
        except InvalidPassword:
            response = "Wrong ADMIN password. Please try again.."
        else:
            response = f"{username} successfully removed"
            del account_holders[username]
        finally:
            remove_text.insert(tk.END, response)

    # create remove username window
    remove_screen = tk.Tk()
    remove_screen.geometry("200x200+100+500")
    remove_screen.title("Remove user")

    remove_label = tk.Label(remove_screen, text="Enter username you want to be removed:")
    remove_label.pack()
    remove_entry = tk.Entry(remove_screen, justify="center")
    remove_entry.pack()
    password_label = tk.Label(remove_screen, text="Enter ADMIN password: ")
    password_label.pack()
    password_entry = tk.Entry(remove_screen, justify="center", show="*")
    password_entry.pack()
    remove_text = tk.Text(remove_screen, width=40, height=2)
    remove_text.pack()
    remove_button = tk.Button(remove_screen, text="Remove", command=remove_user)
    remove_button.pack()
    remove_button = tk.Button(remove_screen, text="Back to ADMIN panel",
                               command=lambda: remove_screen.destroy())
    remove_button.pack()
    remove_screen.mainloop()

def encrypt_password(password):
    #funtion to encrypt user password for better security
    key = np.array([[4, 2], [1, 9]])
    process_init_password = [ord(character) for character in password]

    while len(process_init_password) % 2 != 0:
        process_init_password.append(0)
    process_init_password = np.array(process_init_password)
    process_init_password = process_init_password.reshape(len(process_init_password) // 2, 2)
    encrypted_matrix = np.dot(process_init_password, key)
    encrypted_password = ''.join([chr(int(character)) for row in encrypted_matrix for character in row])
    return encrypted_password

def valid_username(current_username):
    #user validation
    if (current_username not in account_holders
            and current_username.lower() != "admin"
            and len(current_username) in range(6,21)
            and all(char.isalnum for char in current_username)):
        return True
    return False


def valid_password(current_password):
    #password validation with RegEx
    password_pattern = r"[A-Z][a-z0-9]{7,19}"
    result = re.search(password_pattern, current_password)
    if result:
        return True
    return False


def register():
    #register function with registration form interface and registration form logic
    def register_username():
        response = ""
        try:
            register_text.delete("1.0", 'end')
            username = username_entry.get()
            password = password_entry.get()
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            if valid_username(username) and valid_password(password) and username and password and first_name and last_name:
                account_holders[username] = {'password': encrypt_password(password),
                                             'name':f"{first_name} {last_name}",
                                             'balance': 0,
                                             'loans': 0,
                                             'transactions': []}
                with open("data.json", "w") as f:
                    json.dump(account_holders, f)
                response = "User Successfully Registered!"
            elif not username or not password or not first_name or not last_name:
                raise MissingRequiredInformation
            elif not valid_username(username):
                raise InvalidUsername
            elif not valid_password(password):
                raise InvalidPassword
        except MissingRequiredInformation:
            response = "All fields marked with * are required..."
        except InvalidUsername:
            response = "Invalid username or username already taken. Please try again..."
        except InvalidPassword:
            response = "Invalid password! Please try again..."
        finally:
            register_text.insert(tk.END, response)


    #create register form interface
    register_screen = tk.Tk()
    register_screen.geometry("600x600+100+500")
    register_screen.title("Register")

    username_label = tk.Label(register_screen, text="*Enter username (6-20 symbols, only letters and digits: ")
    username_label.pack()
    username_entry = tk.Entry(register_screen, justify="center")
    username_entry.pack()
    password_label = tk.Label(register_screen, text="*Enter password "
                                                    "(8-20 symbols,first letter must be Capital then only letters and digits: ")
    password_label.pack()
    password_entry = tk.Entry(register_screen, justify="center", show="*")
    password_entry.pack()
    first_name_label = tk.Label(register_screen, text="*Enter first name: ")
    first_name_label.pack()
    first_name_entry = tk.Entry(register_screen, justify="center")
    first_name_entry.pack()
    last_name_label = tk.Label(register_screen, text="*Enter last name: ")
    last_name_label.pack()
    last_name_entry = tk.Entry(register_screen, justify="center")
    last_name_entry.pack()
    information = tk.Label(register_screen, text="*Required fields")
    information.pack()
    register_text = tk.Text(register_screen,width=70, height=2 )
    register_text.pack()
    register_screen_button = tk.Button(register_screen, text="Register", command=register_username)
    register_screen_button.pack()
    register_screen_button = tk.Button(register_screen, text="back", command=lambda: (register_screen.destroy(), logout()))
    register_screen_button.pack()
    register_screen.mainloop()


def login():
    #login function with login form interface and login form logic

    def login_username():
        #login form logic
        response = ""
        try:
            login_text.delete("1.0", "end")
            user_id = username_entry.get()
            password = password_entry.get()

            if user_id not in account_holders:
                raise InvalidUsername
            if encrypt_password(password) != account_holders[user_id]['password']:
                raise InvalidPassword
        except InvalidUsername:
            response = "Invalid username. Please try again..."
            login_text.insert(tk.END, response)
        except InvalidPassword:
            response = "Wrong password! Please try again..."
            login_text.insert(tk.END, response)
        else:
            if user_id == "administrator" and password == account_holders[user_id]['password']:
                # root.destroy()
                login_screen.destroy()
                admin_panel()
            else:
                # root.destroy()
                login_screen.destroy()
                welcome_screen(user_id, account_holders[user_id]['name'])


    #create login form screen
    login_screen = tk.Tk()
    login_screen.geometry("600x600+100+500")
    login_screen.title("Login")

    username_label = tk.Label(login_screen, text="Enter your username: ")
    username_label.pack()
    username_entry = tk.Entry(login_screen, justify="center")
    username_entry.pack()
    password_label = tk.Label(login_screen, text="Enter your password: ")
    password_label.pack()
    password_entry = tk.Entry(login_screen, show="*", justify="center")
    password_entry.pack()
    login_text = tk.Text(login_screen, width=60, height=2)
    login_text.pack()
    login_screen_button = tk.Button(login_screen, text="Login", command=login_username)
    login_screen_button.pack()
    login_screen_button = tk.Button(login_screen, text="back", command= lambda: (login_screen.destroy(), logout()))
    login_screen_button.pack()
    login_screen.mainloop()

def admin_panel():
    #admin panel
    admin_panel = tk.Tk()
    admin_panel.geometry("600x600+100+500")
    admin_panel.title("Welcome")

    admin_canvas = tk.Canvas(admin_panel, width=600, height=600)
    admin_canvas.pack(fill="both", expand=True)
    admin_canvas.create_text(290, 40, text=f"ADMIN panel", font=("Arial", 25, "bold"),
                               fill="RED")
    admin_canvas.create_text(300, 550,
                               text="To ensure your operations are saved, please click 'Log Out' before exiting.",
                               font=("Arial", 15, "bold"), fill="white")
    admin_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    list_account_button = ttk.Button(admin_canvas, width=15, text="Show accounts", command=lambda: list_accounts())
    remove_user_button = ttk.Button(admin_canvas, width=15, text="Remove username", command=lambda: remove_username())

    exit_from_admin_panel_button = ttk.Button(admin_canvas, width=15, text="Log out", command=lambda: (admin_panel.destroy(), logout()))
    list_account_button.place(x=210, y=150)
    remove_user_button.place(x=210, y=200)
    exit_from_admin_panel_button.place(x=210, y=500)


    admin_panel.mainloop()


def logout():
    with open("data.json", "w") as f:
        json.dump(account_holders, f)
    #function to log out of account and back to main screen
    main()


def welcome_screen(user, name):
    #create welcome screen after successful login
    welcome = tk.Tk()
    welcome.geometry("600x600+100+500")
    welcome.title("Welcome")

    welcome_canvas = tk.Canvas(welcome, width=600, height=600)
    welcome_canvas.pack(fill="both", expand=True)
    welcome_canvas.create_text(290, 40, text=f"Welcome to your account, {name}", font=("Arial", 25, "bold"), fill="white")
    welcome_canvas.create_text(300, 140, text="Actions:", font=("Arial", 15), fill="white")
    welcome_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15,"bold"), fill="white")
    welcome_canvas.create_text(300, 550, text="To ensure your operations are saved, please click 'Log Out' before exiting.", font=("Arial", 15,"bold"), fill="white")
    deposit_button = ttk.Button(welcome_canvas, width=15, text="Deposit", command=lambda: deposit(user))
    withdraw_button = ttk.Button(welcome_canvas, width=15, text="Withdraw", command=lambda: withdraw(user))
    check_balance_button = ttk.Button(welcome_canvas, width=15, text="Check balance", command=lambda: check_balance(user))
    view_transaction_history_button = ttk.Button(welcome_canvas, width=15, text="View transactions", command=lambda: view_transaction_history(user))
    exit_from_welcome_button = ttk.Button(welcome_canvas, width=15, text="Log out", command=lambda: (welcome.destroy(), logout()))
    deposit_button.place(x=210, y=150)
    withdraw_button.place(x=210, y=200)
    check_balance_button.place(x=210, y=250)
    view_transaction_history_button.place(x=210, y=300)
    exit_from_welcome_button.place(x=210, y=500)
    welcome.mainloop()

def main():
    # create main window
    root = tk.Tk()
    root.title("Bank Account System")
    root.geometry("600x600+100+500")

    my_canvas = tk.Canvas(root, width=600, height=600)
    my_canvas.pack(fill="both", expand=True)

    # create main screen
    my_canvas.create_text(310, 100, text="Welcome to Bank Account System ", font=("Arial", 20, "bold"), fill="white")
    my_canvas.create_text(300, 190, text="Don't have account? ", font=("Arial", 15), fill="white")
    my_canvas.create_text(300, 290, text="Already registered? ", font=("Arial", 15), fill="white")
    my_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    my_canvas.create_text(520, 550, text="made by Milen Nikolov ", font=("Arial", 10, "bold"), fill="white")
    my_canvas.create_text(520, 570, text="www.milen-nikolov.com ", font=("Arial", 10, "bold"), fill="white")
    register_button = ttk.Button(my_canvas, width=15, text="Register", command=lambda: (root.destroy(), register()))
    login_button = ttk.Button(my_canvas, width=15, text="Login", command=lambda: (root.destroy(), login()))
    exit_button = ttk.Button(my_canvas, width=15, text="Exit", command=lambda: exit())
    register_button.place(x=210, y=200)
    login_button.place(x=210, y=300)
    exit_button.place(x=210, y=500)
    root.mainloop()

if __name__ == "__main__":
    main()
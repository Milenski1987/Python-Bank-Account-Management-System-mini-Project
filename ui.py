from bank_system import *
import tkinter as tk
from tkinter import ttk

WINDOW_SIZE = "600x600+100+500"

def deposit_screen(user_id):
    def deposit_money():
        deposit_text.delete("1.0", 'end')
        amount = deposit_entry.get()
        response = deposit(amount, user_id)
        deposit_text.insert(tk.END, response)


    deposit_screen = tk.Tk()
    deposit_screen.geometry(WINDOW_SIZE)
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


def withdraw_screen(user_id):
    def withdraw_money():
        withdraw_text.delete("1.0", 'end')
        amount = withdraw_entry.get()
        response = withdraw(amount, user_id)
        withdraw_text.insert(tk.END, response)

    withdraw_screen = tk.Tk()
    withdraw_screen.geometry(WINDOW_SIZE)
    withdraw_screen.title("Withdraw")
    withdraw_label = tk.Label(withdraw_screen, text="How much you want to withdraw: ")
    withdraw_label.pack()
    withdraw_entry = tk.Entry(withdraw_screen, justify="center")
    withdraw_entry.pack()
    withdraw_text = tk.Text(withdraw_screen, width=40, height=2)
    withdraw_text.pack()
    withdraw_button = tk.Button(withdraw_screen, text="Withdraw", command=withdraw_money)
    withdraw_button.pack()
    withdraw_button = tk.Button(withdraw_screen, text="Back to Welcome screen",
                                command=lambda: withdraw_screen.destroy())
    withdraw_button.pack()


def check_balance_screen(user_id):
    response = check_balance(user_id)
    balance_screen = tk.Tk()
    balance_screen.geometry(WINDOW_SIZE)
    balance_screen.title("Show balance")
    balance_text = tk.Text(balance_screen, width=50, height=2)
    balance_text.pack()
    balance_text.insert(tk.END, response)
    balance_button = tk.Button(balance_screen, text="Back to Welcome screen",
                               command=lambda: balance_screen.destroy())
    balance_button.pack()


def transactions_history(user_id):
    response = view_transaction_history(user_id)
    transactions_screen = tk.Tk()
    transactions_screen.geometry(WINDOW_SIZE)
    transactions_screen.title("Deposit")
    transactions_text = tk.Text(transactions_screen, width=60, height=15)
    transactions_text.pack()
    transactions_text.insert(tk.END, response)
    transactions_button = tk.Button(transactions_screen, text="Back to Welcome screen",
                                    command=lambda: transactions_screen.destroy())
    transactions_button.pack()


def welcome_screen(user_id):
    welcome = tk.Tk()
    welcome.geometry(WINDOW_SIZE)
    welcome.title("Welcome")
    welcome.title("Welcome")

    welcome_canvas = tk.Canvas(welcome, width=600, height=600)
    welcome_canvas.pack(fill="both", expand=True)
    welcome_canvas.create_text(290, 40, text=f"Welcome to your account, {account_holders[user_id]['name']}", font=("Arial", 25, "bold"),
                               fill="white")
    welcome_canvas.create_text(300, 140, text="Actions:", font=("Arial", 15), fill="white")
    welcome_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    welcome_canvas.create_text(300, 550,
                               text="To ensure your operations are saved, please click 'Log Out' before exiting.",
                               font=("Arial", 15, "bold"), fill="white")
    deposit_button = ttk.Button(welcome_canvas, width=15, text="Deposit", command=lambda: deposit_screen(user_id))
    withdraw_button = ttk.Button(welcome_canvas, width=15, text="Withdraw", command=lambda: withdraw_screen(user_id))
    check_balance_button = ttk.Button(welcome_canvas, width=15, text="Check balance",
                                      command=lambda: check_balance_screen(user_id))
    view_transaction_history_button = ttk.Button(welcome_canvas, width=15, text="View transactions",
                                                 command=lambda: transactions_history(user_id))
    exit_from_welcome_button = ttk.Button(welcome_canvas, width=15, text="Log out",
                                          command=lambda: (welcome.destroy(), logout()))
    deposit_button.place(x=210, y=150)
    withdraw_button.place(x=210, y=200)
    check_balance_button.place(x=210, y=250)
    view_transaction_history_button.place(x=210, y=300)
    exit_from_welcome_button.place(x=210, y=500)


def list_accounts_screen():
    response = list_accounts()
    listing_screen = tk.Tk()
    listing_screen.geometry(WINDOW_SIZE)
    listing_screen.title("Accounts")
    listing_text = tk.Text(listing_screen, width=80, height=25)
    listing_text.pack()
    listing_text.insert(tk.END, response)
    listing_button = tk.Button(listing_screen, text="Back to ADMIN panel",
                               command=lambda: listing_screen.destroy())
    listing_button.pack()


def remove_username_screen():
    def remove_user():
        user_id = remove_entry.get()
        password = password_entry.get()
        response = remove_username(user_id, password)
        remove_text.delete("1.0", "end")
        remove_text.insert(tk.END, response)

    remove_screen = tk.Tk()
    remove_screen.geometry(WINDOW_SIZE)
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


def admin_panel():
    #admin panel
    admin_panel = tk.Tk()
    admin_panel.geometry(WINDOW_SIZE)
    admin_panel.title("Welcome")

    admin_canvas = tk.Canvas(admin_panel, width=600, height=600)
    admin_canvas.pack(fill="both", expand=True)
    admin_canvas.create_text(290, 40, text=f"ADMIN panel", font=("Arial", 25, "bold"),
                               fill="RED")
    admin_canvas.create_text(300, 550,
                               text="To ensure your operations are saved, please click 'Log Out' before exiting.",
                               font=("Arial", 15, "bold"), fill="white")
    admin_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    list_account_button = ttk.Button(admin_canvas, width=15, text="Show accounts", command=lambda: list_accounts_screen())
    remove_user_button = ttk.Button(admin_canvas, width=15, text="Remove username", command=lambda: remove_username_screen())

    exit_from_admin_panel_button = ttk.Button(admin_canvas, width=15, text="Log out", command=lambda: (admin_panel.destroy(), logout()))
    list_account_button.place(x=210, y=150)
    remove_user_button.place(x=210, y=200)
    exit_from_admin_panel_button.place(x=210, y=500)


def register_screen():
    def registration():
        register_text.delete("1.0", 'end')
        username = username_entry.get()
        password = password_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        response = user_registration(username, password, first_name, last_name)
        register_text.insert(tk.END, response)


    register_screen = tk.Tk()
    register_screen.geometry(WINDOW_SIZE)
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
    register_text = tk.Text(register_screen, width=70, height=2)
    register_text.pack()

    register_screen_button = tk.Button(register_screen, text="Register", command=registration)
    register_screen_button.pack()
    register_screen_button = tk.Button(register_screen, text="back",
                                       command=lambda: (register_screen.destroy(), logout()))
    register_screen_button.pack()


def login_screen():
    def login_username():
        user_id = username_entry.get()
        password = password_entry.get()
        response = login(user_id, password)
        login_text.delete("1.0", "end")
        if response == "admin":
            login_screen.destroy()
            admin_panel()
        elif response == "regular":
            login_screen.destroy()
            welcome_screen(user_id)
        else:
            login_text.insert(tk.END, response)

    login_screen = tk.Tk()
    login_screen.geometry(WINDOW_SIZE)
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
    login_screen_button = tk.Button(login_screen, text="back", command=lambda: (login_screen.destroy(), logout()))
    login_screen_button.pack()
    login_screen.mainloop()


def logout():
    user_logout()
    main_screen()


def main_screen():
    root = tk.Tk()
    root.title("Bank Account System")
    root.geometry(WINDOW_SIZE)
    my_canvas = tk.Canvas(root, width=600, height=600)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_text(310, 100, text="Welcome to Bank Account System ", font=("Arial", 20, "bold"), fill="white")
    my_canvas.create_text(300, 190, text="Don't have account? ", font=("Arial", 15), fill="white")
    my_canvas.create_text(300, 290, text="Already registered? ", font=("Arial", 15), fill="white")
    my_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    my_canvas.create_text(520, 550, text="made by Milen Nikolov ", font=("Arial", 10, "bold"), fill="white")
    my_canvas.create_text(520, 570, text="www.milen-nikolov.com ", font=("Arial", 10, "bold"), fill="white")
    register_button = ttk.Button(my_canvas, width=15, text="Register", command=lambda: (root.destroy(), register_screen()))
    login_button = ttk.Button(my_canvas, width=15, text="Login", command=lambda: (root.destroy(), login_screen()))
    exit_button = ttk.Button(my_canvas, width=15, text="Exit", command=lambda: exit())
    register_button.place(x=210, y=200)
    login_button.place(x=210, y=300)
    exit_button.place(x=210, y=500)
    root.mainloop()


if __name__ == '__main__':
    main_screen()


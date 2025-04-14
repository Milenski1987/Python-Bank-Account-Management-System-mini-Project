import bank_system as bs
import tkinter as tk
from tkinter import ttk


WINDOW_SIZE = "600x600+100+500"


def deposit_screen(user_id):
    def deposit_money():
        deposit_text.delete("1.0", 'end')
        amount = deposit_entry.get()
        response = bs.deposit(amount, user_id)
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
    deposit_button = tk.Button(deposit_screen, text="Back to User Panel",
                               command=lambda: deposit_screen.destroy())
    deposit_button.pack()


def withdraw_screen(user_id):
    def withdraw_money():
        withdraw_text.delete("1.0", 'end')
        amount = withdraw_entry.get()
        response = bs.withdraw(amount, user_id)
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
    withdraw_button = tk.Button(withdraw_screen, text="Back to User Panel",
                                command=lambda: withdraw_screen.destroy())
    withdraw_button.pack()


def check_balance_screen(user_id):
    response = bs.check_balance(user_id)
    balance_screen = tk.Tk()
    balance_screen.geometry(WINDOW_SIZE)
    balance_screen.title("Show balance")
    balance_text = tk.Text(balance_screen, width=50, height=2)
    balance_text.pack()
    balance_text.insert(tk.END, response)
    balance_button = tk.Button(balance_screen, text="Back to User Panel",
                               command=lambda: balance_screen.destroy())
    balance_button.pack()


def check_iban_screen(user_id):
    response = bs.check_iban(user_id)
    balance_screen = tk.Tk()
    balance_screen.geometry(WINDOW_SIZE)
    balance_screen.title("IBAN")
    balance_text = tk.Text(balance_screen, width=50, height=2)
    balance_text.pack()
    balance_text.insert(tk.END, response)
    balance_button = tk.Button(balance_screen, text="Back to User Panel",
                               command=lambda: balance_screen.destroy())
    balance_button.pack()


def transactions_history(user_id):
    response = bs.view_transaction_history(user_id)
    transactions_screen = tk.Tk()
    transactions_screen.geometry(WINDOW_SIZE)
    transactions_screen.title("Transactions History")
    transactions_text = tk.Text(transactions_screen, width=60, height=15)
    transactions_text.pack()
    transactions_text.insert(tk.END, response)
    transactions_button = tk.Button(transactions_screen, text="Back to User Panel",
                                    command=lambda: transactions_screen.destroy())
    transactions_button.pack()


def loan_screen(user_id):
    def loan():
        loan_apply_screen_text.delete("1.0", 'end')
        amount = loan_apply_screen_entry_amount.get()
        term = loan_apply_screen_entry_term.get()
        response = bs.apply_for_loan(user_id, amount, term)
        loan_apply_screen_text.insert(tk.END, response)

    loan_apply_screen_screen = tk.Tk()
    loan_apply_screen_screen.geometry(WINDOW_SIZE)
    loan_apply_screen_screen.title("Apply for Loan")
    loan_apply_screen_label = tk.Label(loan_apply_screen_screen, text=f"Minimal amount: {bs.MIN_LOAN_AMOUNT}, Maximal amount: {bs.MAX_LOAN_AMOUNT}")
    loan_apply_screen_label.pack()
    loan_apply_screen_label = tk.Label(loan_apply_screen_screen,
                                       text=f"Minimal term in months: {bs.MIN_LOAN_TERM}, Maximal term in months: {bs.MAX_LOAN_TERM}")
    loan_apply_screen_label.pack()
    loan_apply_screen_label = tk.Label(loan_apply_screen_screen, text=f"Current annual interest rate: {bs.INTEREST_RATE}%")
    loan_apply_screen_label.pack()
    loan_apply_screen_label = tk.Label(loan_apply_screen_screen, text="Enter desired amount: ")
    loan_apply_screen_label.pack()
    loan_apply_screen_entry_amount = tk.Entry(loan_apply_screen_screen, justify="center")
    loan_apply_screen_entry_amount.pack()
    loan_apply_screen_label = tk.Label(loan_apply_screen_screen, text="Enter Desired  term: ")
    loan_apply_screen_label.pack()
    loan_apply_screen_entry_term = tk.Entry(loan_apply_screen_screen, justify="center")
    loan_apply_screen_entry_term.pack()
    loan_apply_screen_text = tk.Text(loan_apply_screen_screen, width=50, height=5)
    loan_apply_screen_text.pack()
    loan_apply_screen_button = tk.Button(loan_apply_screen_screen, text="Apply", command=loan)
    loan_apply_screen_button.pack()
    loan_apply_screen_button = tk.Button(loan_apply_screen_screen, text="Back to User Panel",
                                command=lambda: loan_apply_screen_screen.destroy())
    loan_apply_screen_button.pack()



def change_password_screen(user_id):
    def change_password():
        password_text.delete("1.0", 'end')
        current_password = current_password_entry.get()
        new_password = password_entry.get()
        new_password_2 = new_password_entry_2.get()
        response = bs.user_change_password(user_id, current_password, new_password, new_password_2)
        password_text.insert(tk.END, response)


    password_screen = tk.Tk()
    password_screen.geometry(WINDOW_SIZE)
    password_screen.title("Password Change")
    current_password_label = tk.Label(password_screen, text="*Enter current password: ")
    current_password_label.pack()
    current_password_entry = tk.Entry(password_screen, justify="center", show="*")
    current_password_entry.pack()
    new_password_label = tk.Label(password_screen, text="*Enter new password "
                                                    "(8-20 symbols,first letter must be Capital then only letters and digits: ")
    new_password_label.pack()
    password_entry = tk.Entry(password_screen, justify="center", show="*")
    password_entry.pack()
    new_password_2_label = tk.Label(password_screen, text="*Re-Enter new password "
                                                        "(8-20 symbols,first letter must be Capital then only letters and digits: ")
    new_password_2_label.pack()
    new_password_entry_2 = tk.Entry(password_screen, justify="center", show="*")
    new_password_entry_2.pack()

    information = tk.Label(password_screen, text="*Required fields")
    information.pack()
    password_text = tk.Text(password_screen, width=70, height=2)
    password_text.pack()

    change_password_screen_button = tk.Button(password_screen, text="Change Password", command=change_password)
    change_password_screen_button.pack()
    change_password_screen_button = tk.Button(password_screen, text="Back to User Panel",
                                       command=lambda: (password_screen.destroy()))
    change_password_screen_button.pack()


def welcome_screen(user_id):
    welcome = tk.Tk()
    welcome.geometry(WINDOW_SIZE)
    welcome.title("Welcome")
    welcome.title("Welcome")

    welcome_canvas = tk.Canvas(welcome, width=600, height=600)
    welcome_canvas.pack(fill="both", expand=True)
    welcome_canvas.create_text(290, 40, text=f"Welcome to your account, {bs.account_holders[user_id]['name']}", font=("Arial", 25, "bold"),
                               fill="white")
    welcome_canvas.create_text(300, 160, text="Actions:", font=("Arial", 15), fill="white")
    welcome_canvas.create_text(300, 490, text="Want to quit? ", font=("Arial", 15, "bold"), fill="white")
    welcome_canvas.create_text(300, 550,
                               text="To ensure your operations are saved, please click 'Log Out' before exiting.",
                               font=("Arial", 15, "bold"), fill="white")
    actions = {
        "Deposit": deposit_screen,
        "Withdraw": withdraw_screen,
        "Check Balance": check_balance_screen,
        "View Recent Transactions": transactions_history,
        "Check IBAN": check_iban_screen,
        "Apply for Loan": loan_screen,
        "Change Password": change_password_screen,
    }
    available_actions = ["Deposit", "Withdraw", "Check Balance", "View Recent Transactions", "Check IBAN", "Apply for Loan", "Change Password"]
    chosen_action = tk.StringVar(welcome_canvas)
    chosen_action.set(" ")
    choose_action = tk.OptionMenu(welcome_canvas, chosen_action, *available_actions)
    choose_action.config(width=15)
    choose_action.place(x=210, y=180)
    action_button = ttk.Button(welcome_canvas, width=15, text="Go", command=lambda: actions[chosen_action.get()](user_id))
    action_button.place(x = 210, y=210)
    exit_from_welcome_button = ttk.Button(welcome_canvas, width=15, text="Log out",command=lambda: (welcome.destroy(), logout()))
    exit_from_welcome_button.place(x= 210, y=500)


def list_accounts_screen():
    response = bs.list_accounts()
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
        response = bs.remove_username(user_id, password)
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


def change_loan_screen(command):
    def change_loan():
        new_value = change_entry.get()
        password = password_entry.get()
        response = bs.change_rate(new_value, password) if command == "Interest Rate" else bs.change_amount(new_value, password)
        remove_text.delete("1.0", "end")
        remove_text.insert(tk.END, response)

    change_screen = tk.Tk()
    change_screen.geometry(WINDOW_SIZE)
    change_screen.title("Change Loan")
    change_label = tk.Label(change_screen, text="Enter new interest rate (integer number): " if command == "Interest Rate" else "Enter new max loan amount:")
    change_label.pack()
    change_entry = tk.Entry(change_screen, justify="center")
    change_entry.pack()
    password_label = tk.Label(change_screen, text="Enter ADMIN password: ")
    password_label.pack()
    password_entry = tk.Entry(change_screen, justify="center", show="*")
    password_entry.pack()
    remove_text = tk.Text(change_screen, width=40, height=2)
    remove_text.pack()
    remove_button = tk.Button(change_screen, text="Change", command=change_loan)
    remove_button.pack()
    remove_button = tk.Button(change_screen, text="Back to ADMIN panel",
                              command=lambda: change_screen.destroy())
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
    change_interest_rate_button = ttk.Button(admin_canvas, width=15, text="Change Loan Rate", command=lambda: change_loan_screen("Interest Rate"))
    change_max_amount_button = ttk.Button(admin_canvas, width=15, text="Change Loan Max Amount", command=lambda: change_loan_screen("Max Amount"))

    exit_from_admin_panel_button = ttk.Button(admin_canvas, width=15, text="Log out", command=lambda: (admin_panel.destroy(), logout()))
    list_account_button.place(x=210, y=150)
    remove_user_button.place(x=210, y=200)
    change_interest_rate_button.place(x=210, y=250)
    change_max_amount_button.place(x=210, y=300)
    exit_from_admin_panel_button.place(x=210, y=500)


def register_screen():
    def registration():
        register_text.delete("1.0", 'end')
        username = username_entry.get()
        password = password_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        response = bs.user_registration(username, password, first_name, last_name)
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
        response = bs.login(user_id, password)
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
    bs.file_save()
    main_screen()


def main_screen():
    root = tk.Tk()
    root.title("Bank Account System")
    root.geometry(WINDOW_SIZE)
    my_canvas = tk.Canvas(root,width=600, height=600)
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



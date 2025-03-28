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


def deposit(amount, user_id):
    try:
        money_amount = float(amount)
        if money_amount <= 0:
            raise NegativeAmount
    except ValueError:
        return "Please enter valid number"
    except NegativeAmount:
        return "Amount must be positive number"
    else:
        account_holders[user_id]['transactions'].append(f"{money_amount:.2f}")
        account_holders[user_id]['balance'] += float(f"{money_amount:.2f}")
        return "Successful transaction"


def withdraw(amount, user_id):
    try:
        money_amount = float(amount)
        if account_holders[user_id]['balance'] <= 0 or account_holders[user_id]['balance'] < money_amount:
            raise InsufficientFunds
        elif money_amount <= 0:
            raise NegativeAmount
    except InsufficientFunds:
        return "Invalid operation. Insufficient funds!"
    except ValueError:
        return "Please enter valid number"
    except NegativeAmount:
        return "Amount must be positive number"
    else:
        account_holders[user_id]['transactions'].append(f"-{money_amount:.2f}")
        account_holders[user_id]['balance'] -= float(f"{money_amount:.2f}")
        return "Successful transaction"


def check_balance(user_id):
    return f"Current balance: {account_holders[user_id]['balance']:.2f}"


def view_transaction_history(user_id):
    return f'Recent transactions: \n{", ".join(list(map(str,account_holders[user_id]['transactions'])))}'


def list_accounts():
    return f"Accounts: \n\n{'\n'.join([f'{username}:\n  '
                                       f'Balance: {account_holders[username]['balance']}\n  '
                                           f'Transactions: {', '.join(account_holders[username]['transactions'])}\n'
                                       for username in account_holders if username != 'administrator'])}"


def remove_username(user_id, password):
        response = ""
        try:
            if user_id == 'administrator':
                raise Forbidden
            if user_id not in account_holders:
                raise InvalidUsername
            if password != account_holders['administrator']['password']:
                raise InvalidPassword
        except Forbidden:
            return "Operation not allowed."
        except InvalidUsername:
            return f"{user_id} doesn't exist"
        except InvalidPassword:
            return "Wrong ADMIN password. Please try again.."
        else:
            del account_holders[user_id]
            return f"{user_id} successfully removed"


def encrypt_password(password):
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
    if (current_username not in account_holders
            and current_username.lower() != "admin"
            and len(current_username) in range(6,21)
            and all(char.isalnum for char in current_username)):
        return True
    return False


def valid_password(current_password):
    password_pattern = r"[A-Z][a-z0-9]{7,19}"
    result = re.search(password_pattern, current_password)
    if result:
        return True
    return False


def user_registration(username, password, first_name, last_name):
    if valid_username(username) and valid_password(password) and username and password and first_name and last_name:
        account_holders[username] = {'password': encrypt_password(password),
                                     'name':f"{first_name} {last_name}",
                                     'balance': 0,
                                     'loans': 0,
                                     'transactions': []}
        with open("data.json", "w") as f:
            json.dump(account_holders, f)
        return True
    elif not username or not password or not first_name or not last_name:
        raise MissingRequiredInformation
    elif not valid_username(username):
        raise InvalidUsername
    elif not valid_password(password):
        raise InvalidPassword


def login(user_id, password):
    #login function with login form interface and login form logic
    try:
        if user_id == "administrator" and password == "Admin12345":
            return "admin"
        elif user_id in account_holders and encrypt_password(password) == account_holders[user_id]['password']:
            return "regular"
        elif user_id not in account_holders:
            raise InvalidUsername
        elif encrypt_password(password) != account_holders[user_id]['password']:
            raise InvalidPassword

    except InvalidUsername:
        return "Invalid username. Please try again..."
    except InvalidPassword:
        return "Wrong password! Please try again..."



def user_logout():
    with open("data.json", "w") as f:
        json.dump(account_holders, f)
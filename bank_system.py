import json
import os
import re
import sys
import base64
import datetime


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


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


with open(resource_path("data.json")) as file:
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
        account_holders[user_id]['transactions'].append(f"{get_current_time()}  {money_amount:.2f}")
        account_holders[user_id]['balance'] += float(f"{money_amount:.2f}")
        return "Successful transaction"

def get_current_time():
    x = datetime.datetime.now()
    return f"{x.strftime('%x')}  {x.strftime('%X')}"

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
        account_holders[user_id]['transactions'].append(f"{get_current_time()}  -{money_amount:.2f}")
        account_holders[user_id]['balance'] -= float(f"{money_amount:.2f}")
        return "Successful transaction"


def check_balance(user_id):
    return f"Current balance: {account_holders[user_id]['balance']:.2f}"


def check_iban(user_id):
    return f"Your IBAN: {account_holders[user_id]['IBAN']}"


def view_transaction_history(user_id):
    return f'Recent transactions: \n{"\n".join(list(map(str,account_holders[user_id]['transactions'])))}'


def list_accounts():
    return f"Accounts: \n\n{'\n'.join([f'{username}:\n  '
                                       f'Balance: {account_holders[username]['balance']}\n  '
                                           f'Transactions:\n   {'\n   '.join(account_holders[username]['transactions'])}\n'
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


def generate_iban(counter):
    return f"BG18MNBB204719{counter:04d}{counter:04d}"


def encrypt_password(password):
    encrypted_password = str(base64.b64encode(password.encode()))
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
    try:
        if valid_username(username) and valid_password(password) and username and password and first_name and last_name:
            account_holders[username] = {'user_id': 1,
                                         'password': encrypt_password(password),
                                         'name':f"{first_name} {last_name}",
                                         'IBAN': generate_iban(account_holders['administrator']['counter']),
                                         'balance': 0,
                                         'loans': 0,
                                         'transactions': []}
            account_holders['administrator']['counter'] += 1
            with open("data.json", "w") as f:
                json.dump(account_holders, f, indent=1)
            return "User Successfully Registered!"
        elif not username or not password or not first_name or not last_name:
            raise MissingRequiredInformation
        elif not valid_username(username):
            raise InvalidUsername
        elif not valid_password(password):
            raise InvalidPassword
    except MissingRequiredInformation:
        return "All fields marked with * are required..."
    except InvalidUsername:
        return "Invalid username or username already taken. Please try again..."
    except InvalidPassword:
        return "Invalid password! Please try again..."


def login(user_id, password):
    try:
        if user_id == "administrator" and password == "Admin12345":
            return "admin"
        elif user_id in account_holders and str(encrypt_password(password)) == account_holders[user_id]['password']:
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
        json.dump(account_holders, f, indent=1)
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

class InvalidNewPassword(Exception):
    pass

class MissingRequiredInformation(Exception):
    pass

class NegativeAmount(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class Forbidden(Exception):
    pass

class PasswordNotMatch(Exception):
    pass


INTEREST_RATE = 4
MAX_LOAN_AMOUNT = 10000
MIN_LOAN_AMOUNT = 1000
MIN_LOAN_TERM = 6
MAX_LOAN_TERM = 96


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


with open(resource_path("data.json")) as file:
    account_holders = json.load(file)


def deposit(amount: str, user_id: str) -> str:
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
        file_save()
        return "Successful transaction"

def get_current_time() -> str:
    x = datetime.datetime.now()
    return f"{x.strftime('%x')}  {x.strftime('%X')}"

def withdraw(amount: str, user_id: str) -> str:
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
        file_save()
        return "Successful transaction"


def check_balance(user_id: str) -> str:
    return f"Current balance: {account_holders[user_id]['balance']:.2f}"


def check_iban(user_id: str) -> str:
    return f"Your IBAN: {account_holders[user_id]['IBAN']}"


def view_transaction_history(user_id: str) -> str:
    return f'Recent transactions: \n{"\n".join(list(map(str,account_holders[user_id]['transactions'])))}'


def user_change_password(user_id: str, current_password: str, new_password: str, new_password_again: str) -> str:
    try:
        if ((encrypt_password(current_password) == account_holders[user_id]['password']
                and valid_password(new_password)
                and new_password == new_password_again)
                and current_password != new_password):
            account_holders[user_id]['password'] = encrypt_password(new_password)
            file_save()
            return "Password changed successfully"
        elif not current_password or not new_password or not new_password_again:
            raise MissingRequiredInformation
        elif encrypt_password(current_password) != account_holders[user_id]['password']:
            raise InvalidPassword
        elif new_password != new_password_again:
            raise PasswordNotMatch
        elif not valid_password(new_password):
            raise InvalidNewPassword
        elif account_holders[user_id]['password'] == encrypt_password(new_password):
            raise Forbidden
    except MissingRequiredInformation:
        return "All fields are required..."
    except InvalidPassword:
        return "Wrong current password, try again.."
    except InvalidNewPassword:
        return "Invalid new password! Please try again..."
    except PasswordNotMatch:
        return "New password entered in both fields is different"
    except Forbidden:
        return "New password can't be same as current password"


def list_accounts() -> str:
    return f"Accounts: \n\n{'\n'.join([f'{username}:\n  '
                                       f'Balance: {account_holders[username]['balance']}\n  '
                                           f'Transactions:\n   {'\n   '.join(account_holders[username]['transactions'])}\n'
                                       for username in account_holders if username != 'administrator'])}"


def remove_username(user_id: str, password: str) -> str:
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
            file_save()
            return f"{user_id} successfully removed"


def loan_monthly_payment(amount: float, term: int) -> float:
    interest_rate_per_month = (INTEREST_RATE / 12) / 100
    monthly_payment = (amount * interest_rate_per_month * (1 + interest_rate_per_month)**term)/((1 + interest_rate_per_month)**term - 1)
    return float(f"{monthly_payment:.2f}")


def apply_for_loan(user_id: str, amount: str, term: str) -> str:
    try:
        if not amount or not term:
            raise MissingRequiredInformation
        elif float(account_holders[user_id]['loan']) > 0:
            raise Forbidden
        elif int(amount) not in range(MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT + 1):
            raise ChosenNumberOutOfRange
        elif int(term) not in range(MIN_LOAN_TERM, MAX_LOAN_TERM + 1):
            raise ChosenNumberOutOfRange
    except Forbidden:
        return f"Denied! You already have loan!"
    except MissingRequiredInformation:
        return "Amount field and Term field are required!"
    except ChosenNumberOutOfRange:
        return (f"Please enter valid numbers in range:\n"
                f" {MIN_LOAN_AMOUNT} - {MAX_LOAN_AMOUNT} for amount\n "
                f"{MIN_LOAN_TERM} - {MAX_LOAN_TERM} for term")
    except ValueError:
        return "Please enter valid number"
    else:
        amount = float(amount)
        term = int(term)

        account_holders[user_id]['loan'] = float(f"{amount:.2f}")
        monthly_payment = loan_monthly_payment(amount, term)
        account_holders[user_id]['monthly_payment'] = monthly_payment
        account_holders[user_id]['balance'] += float(f"{amount:.2f}")
        account_holders[user_id]['transactions'].append(f"{get_current_time()}  {amount:.2f}")
        file_save()
        return (f"Your loan is approved and will be in your account in short time!"
                f"\nYour monthly payment will be {monthly_payment}")


def generate_iban(counter: int) -> str:
    return f"BG18MNBB204719{counter:04d}{counter:04d}"


def encrypt_password(password: str) -> str:
    encrypted_password = str(base64.b64encode(password.encode()))
    return encrypted_password


def valid_username(current_username:str) -> bool:
    if (current_username not in account_holders
            and current_username.lower() != "admin"
            and len(current_username) in range(6,21)
            and all(char.isalnum for char in current_username)):
        return True
    return False


def valid_password(current_password: str) -> bool:
    password_pattern = r"[A-Z][a-z0-9]{7,19}"
    result = re.search(password_pattern, current_password)
    if result:
        return True
    return False


def user_registration(username: str, password: str, first_name: str, last_name: str) -> str:
    try:
        if valid_username(username) and valid_password(password) and username and password and first_name and last_name:
            account_holders[username] = {'user_id': 1,
                                         'password': encrypt_password(password),
                                         'name':f"{first_name} {last_name}",
                                         'IBAN': generate_iban(account_holders['administrator']['counter']),
                                         'balance': 0,
                                         'loan': 0,
                                         'transactions': []}
            account_holders['administrator']['counter'] += 1
            file_save()
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


def login(user_id: str, password: str) -> str:
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



def file_save() -> None:
    with open("data.json", "w") as f:
        json.dump(account_holders, f, indent=1)
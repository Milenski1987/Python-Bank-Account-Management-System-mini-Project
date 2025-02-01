# Enhanced Bank Account Management System

# 🏦 Data Structures to Store Information
account_holders = []# Account names
account_passwords = []      #Account password
balances = []         # Account balances
transaction_histories = []  # Account transaction logs
loans = []            # Account loan details

MAX_LOAN_AMOUNT = 10000
INTEREST_RATE = 0.03

def display_menu():
    """Main menu for banking system."""
    print("\n🌟 Welcome to Enhanced Bank System 🌟")
    print("1️⃣ Create Account")
    print("2️⃣ Deposit Money")
    print("3️⃣ Withdraw Money")
    print("4️⃣ Check Balance")
    print("5️⃣ List All Accounts")
    print("6️⃣ Transfer Funds")
    print("7️⃣ View Transaction History")
    print("8️⃣ Apply for Loan")
    print("9️⃣ Repay Loan")
    print("🔟 Identify Credit Card Type")
    print("0️⃣ Exit")

def create_account() -> str:
    """Create a new account."""
    username = input("Please add desired username:")
    if username in account_holders:
        return "This username is already in use. Please try again."
    else:
        password = input("Enter desired password for your account:")
        account_holders.append(username)
        balances.append(0)
        loans.append({})
        transaction_histories.append([])
        account_passwords.append(password)
        return "Account created successfully!"

def deposit() -> str:
    """Deposit money into an account."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            money_to_deposit = float(input("Enter amount to deposit:"))

            balances[user_id] += money_to_deposit
            transaction_histories[user_id].append(+money_to_deposit)
            return f"{money_to_deposit:.2f} successfully deposited!"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def withdraw() -> str:
    """Withdraw money from an account."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            money_to_withdraw = float(input("Enter amount to withdraw:"))

            if money_to_withdraw <= balances[user_id]:
                balances[user_id] -= money_to_withdraw
                transaction_histories[user_id].append(-money_to_withdraw)
                return f"{money_to_withdraw:.2f} withdrawn successfully!"
            return "Sorry, not enough money!"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def check_balance() -> str:
    """Check balance of an account."""
    username = input("Please enter your username:")

    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            return f"{username}'s account balance:\n{balances[user_id]:.2f}"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def list_accounts() -> str:
    """List all account holders and details."""
    for user_id in range(len(account_holders)):
        return f"{account_holders[user_id]}: Current balance: {balances[user_id]:.2f}, \
        Loans: {loans[user_id]['remaining amount']:.2f}"

def transfer_funds() -> str:
    """Transfer funds between two accounts."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            recipient = input("Please enter recipient username:")
            if recipient in account_holders:
                recipient_id = account_holders.index(recipient)
                money_to_transfer = float(input("Enter amount to transfer:"))
                if money_to_transfer <= balances[user_id]:
                    balances[user_id] -= money_to_transfer
                    transaction_histories[user_id].append(-money_to_transfer)
                    balances[recipient_id] += money_to_transfer
                    transaction_histories[recipient_id].append(+money_to_transfer)
                    return f"{money_to_transfer} successfully transferred to {recipient} "
                return "Sorry, not enough money!"
            return "Invalid recipient username"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def view_transaction_history() -> str:
    """View transactions for an account."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            return f"{username}'s transaction history: \n{'\n'.join([str(pay) for pay in transaction_histories])}"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def apply_for_loan() -> str:
    """Allow user to apply for a loan."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            loan_amount = float(input("Enter amount you want to loan:"))
            if loan_amount not in range(0, 10001):
                return "Wrong amount!Amount must be in range 1 to 10000"
            else:
                term_in_years = int(input("Enter desired term in years:"))
                interest = loan_amount * INTEREST_RATE * term_in_years
                amount_due = loan_amount + interest
                minimal_monthly_payment = amount_due / (term_in_years * 12)

                loans[user_id]['remaining amount'] = amount_due
                loans[user_id]["monthly_payment"] = minimal_monthly_payment
                balances[user_id] += amount_due
                transaction_histories[user_id].append(+amount_due)

                return f"Your interest rate is: {INTEREST_RATE*100}%\
                \nAmount due on the loan is {amount_due:.2f}\
                \nMinimum monthly loan payment: {minimal_monthly_payment:.2f}"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def repay_loan() -> str:
    """Allow user to repay a loan."""
    username = input("Please enter your username:")
    if username in account_holders:
        user_id = account_holders.index(username)
        password = input("Please enter your password:")

        if password == account_passwords[user_id]:
            payment = float(input(f"Enter amount to repay (minimum payment:{loans[user_id]['monthly_payment']:.2f}):"))
            if loans[user_id]['monthly_payment'] <= payment <= loans[user_id]['remaining amount']:
                loans[user_id]['remaining amount'] -= payment
                balances[user_id] -= payment
                transaction_histories[user_id].append(-payment)
                return "Successful payment!"

            elif loans[user_id]['monthly_payment'] > payment:
                return "Amount is lower than minimum monthly payment!"

            elif payment > loans[user_id]['remaining amount']:
                return "Amount is greater than remaining amount on loan"
        return "Wrong password. Please try again."
    return "Invalid username. Please try again."

def identify_card_type() -> str:
    """Identify type of credit card."""
    card_number = input("Please enter your card number (must be 16 digits long):")

    if len(card_number) != 16:
        return "Wrong length of card number!"
    else:
        card_type = ""
        if card_number.startswith("4"):
            card_type = "Visa"
        elif card_number.startswith(("51", "52", "53", "54", "55")):
            card_type = "MasterCard"
        elif card_number.startswith(("34", "37")):
            card_type = "American Express"
        else:
            card_type = "Other"

        return card_type

def main():
    """Run the banking system."""
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        # Map choices to functions
        if choice == 1:
            print(create_account())
        elif choice == 2:
            print(deposit())
        elif choice == 3:
            print(withdraw())
        elif choice == 4:
            print(check_balance())
        elif choice == 5:
            print(list_accounts())
        elif choice == 6:
            print(transfer_funds())
        elif choice == 7:
            print(view_transaction_history())
        elif choice == 8:
            print(apply_for_loan())
        elif choice == 9:
            print(repay_loan())
        elif choice == 10:
            print(identify_card_type())
        elif choice == 0:
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Try again!")


if __name__ == "__main__":
    main()

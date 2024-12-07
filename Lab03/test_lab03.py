from lab03 import User, Account, ATMCard, ATMMachine

# Initialize ATMMachines from the atm dictionary
atm_machines = []
atm_data = {'1001': 1000000, '1002': 200000}
for machine_id, initial_amount in atm_data.items():
    atm_machines.append(ATMMachine(machine_id, initial_amount))

# Add users and their accounts
user_data = {
    '1-1101-12345-67-0': ['Harry', '1234567890', '12345', 20000],
    '1-1101-12345-68-0': ['Hermione', '1234567891', '12346', 1000],
}

users = {}
cards = {}
for citizen_id, details in user_data.items():
    name, account_number, card_number, balance = details
    user = User(citizen_id, name)
    account = Account(account_number, user, balance)
    card = ATMCard(card_number, account, '1234')
    user.add_account(account)
    users[citizen_id] = user
    cards[card_number] = card

# Test Case #1: Insert card into ATM
def test_insert_card(atm, card):
    try:
        account = atm.insert_card(card, '1234')
        print(f"Test Case #1: Insert card {card.get_card_number()} into ATM {atm.get_machine_id()}")
        print(f"Account Number: {account.get_account_number()}, Card Number: {card.get_card_number()}, Success")
    except ValueError as e:
        print(e)

# Test Case #2: Deposit
def test_deposit(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #2: Deposit {amount} into account {account.get_account_number()}")
        print(f"Hermione account before test: {account.get_balance()}")
        atm.deposit(card, amount)
        print(f"Hermione account after test: {account.get_balance()}")
        print(f"Transaction: {account.get_transactions()[-1]}")
    except ValueError as e:
        print(e)

# Test Case #3: Deposit but send a negative
def test_deposit_negative(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #3: Deposit {amount} into account {account.get_account_number()}")
        atm.deposit(card, amount)
    except ValueError as e:
        print(e)

# Test Case #4: Withdraw
def test_withdraw(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #4: Withdraw {amount} from account {account.get_account_number()}")
        print(f"Hermione account before test: {account.get_balance()}")
        atm.withdraw(card, amount)
        print(f"Hermione account after test: {account.get_balance()}")
        print(f"Transaction: {account.get_transactions()[-1]}")
    except ValueError as e:
        print(e)

# Test Case #5: Withdraw more money than the money in the account
def test_withdraw_exceed_balance(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #5: Withdraw {amount} from account {account.get_account_number()}")
        atm.withdraw(card, amount)
    except ValueError as e:
        print(e)

# Test Case #6: Transfer money
def test_transfer(atm, card, amount, target_account):
    try:
        account = card.get_account()
        print(f"Test Case #6: Transfer {amount} from account {account.get_account_number()} to account {target_account.get_account_number()}")
        print(f"Harry account before test: {account.get_balance()}")
        print(f"Hermione account before test: {target_account.get_balance()}")
        atm.transfer(card, amount, target_account)
        print(f"Harry account after test: {account.get_balance()}")
        print(f"Hermione account after test: {target_account.get_balance()}")
        print(f"Transaction: {account.get_transactions()[-1]}")
    except ValueError as e:
        print(e)

# Test Case #7: Show statement
def test_show_statement(account):
    owner_name = account.get_owner().get_name()
    print(f"Test Case #7: Show statement for account {account.get_account_number()}")
    for transaction in account.get_transactions():
        if transaction[0] == 'D':
            print(f"{owner_name} transaction : D-ATM:{transaction[2]}-{transaction[1]}-{account.get_balance()}")
        elif transaction[0] == 'W':
            print(f"{owner_name} transaction : W-ATM:{transaction[2]}-{transaction[1]}-{account.get_balance()}")
        elif transaction[0] == 'TD':
            print(f"{owner_name} transaction : TD-ATM:{transaction[2]}-{transaction[1]}-{account.get_balance()}")

# Test Case #8: Insert card with incorrect PIN
def test_insert_card_incorrect_pin(atm, card):
    print(f"Test Case #8: Insert card {card.get_card_number()} with incorrect PIN")
    try:
        atm.insert_card(card, '9999')
    except ValueError as e:
        print(e)

# Test Case #9: Withdraw more than daily limit
def test_withdraw_exceed_daily_limit(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #9: Withdraw {amount} from account {account.get_account_number()}")
        atm.withdraw(card, amount)
    except ValueError as e:
        print(e)

# Test Case #10: Withdraw when ATM has insufficient funds
def test_withdraw_insufficient_atm_funds(atm, card, amount):
    try:
        account = card.get_account()
        print(f"Test Case #10: Withdraw {amount} from account {account.get_account_number()}")
        atm.withdraw(card, amount)
    except ValueError as e:
        print(e)

# Helper function to run test cases
def run_test_case(test_case, *args):
    test_case(*args)
    print("\n=================================================\n")

# Running the test cases
first_atm = atm_machines[0]
second_atm = atm_machines[1]
harry_card = cards['12345']
hermione_card = cards['12346']

run_test_case(test_insert_card, first_atm, harry_card)
run_test_case(test_deposit, second_atm, hermione_card, 1000)
run_test_case(test_deposit_negative, second_atm, hermione_card, -1)
run_test_case(test_withdraw, second_atm, hermione_card, 500)
run_test_case(test_withdraw_exceed_balance, second_atm, hermione_card, 2000)
run_test_case(test_transfer, second_atm, harry_card, 10000, hermione_card.get_account())
run_test_case(test_show_statement, hermione_card.get_account())
run_test_case(test_insert_card_incorrect_pin, first_atm, harry_card)
run_test_case(test_withdraw_exceed_daily_limit, first_atm, harry_card, 45000)
run_test_case(test_withdraw_insufficient_atm_funds, second_atm, harry_card, 250000)
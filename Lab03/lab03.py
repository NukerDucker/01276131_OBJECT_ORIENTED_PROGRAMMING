class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name

    @property
    def citizen_id(self) -> str:
        return self.__citizen_id

    @property
    def full_name(self) -> str:
        return self.__name
class Account:
    def __init__(self, account_number: str, owner: User, initial_balance: float = 0.0):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = initial_balance
        self.__transactions = []

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def transactions(self) -> list:
        return self.__transactions

    @balance.setter
    def balance(self, balance: float):
        self.__balance = balance

    def add_transaction(self, transaction):
        self.__transactions.append(transaction)


class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str = '0000'):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin

    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def account(self) -> Account:
        return self.__account

    @property
    def pin(self) -> str:
        return self.__pin
    
    @property
    def balance(self) -> float:
        return self.__account.balance
    
    @balance.setter
    def balance(self, balance: float):
        self.__account.balance = balance
        
    @property
    def account_number(self) -> str:
        return self.__account.account_number

    @property
    def owner(self) -> User:
        return self.__account.owner

    def add_transaction(self, transaction):
        self.__account.add_transaction(transaction)

class ATMMachine:
    ANNUAL_FEE: int = 150
    MAXIMUM_WITHDRAWAL: int = 40_000

    def __init__(self, machine_id: str, initial_amount: float = 1_000_000):
        self.__machine_id = machine_id
        self.__atm_balance = initial_amount

    @property
    def machine_id(self) -> str:
        return self.__machine_id

    @property
    def atm_balance(self) -> float:
        return self.__atm_balance

    def insert_card(self, card_number: str, pin: str):
        card = bank.find_card(card_number)
        if card and card.pin == pin:
            return card
        return "Invalid PIN or card not found"

    def deposit(self, account: Account, amount: float):
        if amount <= 0:
            return "Deposit amount must be positive"
        account.balance += amount
        self.__atm_balance += amount
        account.add_transaction(Transaction('D', amount, self.__machine_id))

    def withdraw(self, account: Account, amount: float):
        if amount > self.__atm_balance:
            return 'ATM has insufficient funds'
        if amount > self.MAXIMUM_WITHDRAWAL:
            return f'Exceeds daily maximum withdrawal limit of {self.MAXIMUM_WITHDRAWAL:,} baht'
        if amount > account.balance:
            return "Insufficient account balance"
        if amount <= 0:
            return "Withdrawal amount must be positive"
        account.balance -= amount
        self.__atm_balance -= amount
        account.add_transaction(Transaction('W', amount, self.__machine_id))

    def transfer(self, sender: Account, receiver: Account, amount: float):
        if amount <= 0:
            return "Transfer amount must be positive"
        if amount > sender.balance:
            return "Insufficient sender account balance"
        sender.balance -= amount
        receiver.balance += amount
        sender.add_transaction(Transaction('TW', amount, self.__machine_id, receiver.account_number))
        receiver.add_transaction(Transaction('TD', amount, self.__machine_id, sender.account_number))


class Transaction:
    def __init__(self, transaction_type: str, amount: float, atm_id: str, account_number: str = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__atm_id = atm_id
        self.__account_number = account_number

    def __str__(self):
        if self.__transaction_type in ('TW', 'TD'):
            return f'{self.__transaction_type}-ATM : {self.__atm_id}-{self.__amount}-{self.__account_number}'
        return f'{self.__transaction_type}-ATM : {self.__atm_id}-{self.__amount}'


class Bank:
    def __init__(self):
        self.__users = []
        self.__accounts = []
        self.__cards = []
        self.__atms = []

    def add_user(self, user: User):
        self.__users.append(user)

    def add_account(self, account: Account):
        self.__accounts.append(account)

    def add_card(self, card: ATMCard):
        self.__cards.append(card)

    def add_atm(self, atm: ATMMachine):
        self.__atms.append(atm)

    def get_atm(self, machine_id: str) -> ATMMachine:
        for atm in self.__atms:
            if atm.machine_id == machine_id:
                return atm

    def find_card(self, card_number: str) -> ATMCard:
        for card in self.__cards:
            if card.card_number == card_number:
                return card

    def find_account(self, account_number: str) -> Account:
        for account in self.__accounts:
            if account.account_number == account_number:
                return account


# Data Initialization
user_data = {
    '1-1101-12345-12-0': ['Harry Potter', '1234567890', '12345', 20_000],
    '1-1101-12345-13-0': ['Hermione Granger', '0987654321', '12346', 1_000]
}

atm_data = {'1001': 1_000_000, '1002': 200_000}

bank = Bank()

# Initialize users, accounts, and cards
for citizen_id, data in user_data.items():
    user = User(citizen_id, data[0])
    account = Account(data[1], user, data[3])
    card = ATMCard(data[2], account, '1234')

    bank.add_user(user)
    bank.add_account(account)
    bank.add_card(card)

# Initialize ATMs
for machine_id, balance in atm_data.items():
    atm = ATMMachine(machine_id, balance)
    bank.add_atm(atm)

###############################################

SEPARATOR = "-------------------------\n"

# Test case 1
print()
print("\033[1m\033[4mTest case 1\033[0m")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print(card.card_number, card.account.account_number, 'Success')
print(SEPARATOR)

# Test case 2
print("\033[1m\033[4mTest case 2\033[0m")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(f'Hermione account balance before: {card.account.balance}')
atm.deposit(card.account, 1000)
print(f'Hermione account balance after: {card.account.balance}')
print(SEPARATOR)

# Test case 3
print("\033[1m\033[4mTest case 3\033[0m")
atm = bank.get_atm('1002')
account = atm.insert_card('12346', '1234')
print(atm.deposit(account, -1))
print(SEPARATOR)

# Test case 4
print("\033[1m\033[4mTest case 4\033[0m")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print(f'Harry account balance before: {card.account.balance}')
print(atm.withdraw(card.account, 500))
print(f'Harry account balance after: {card.account.balance}')
print(SEPARATOR)

# Test case 5
print("\033[1m\033[4mTest case 5\033[0m")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print(atm.withdraw(card.account, 20000))
print(SEPARATOR)

# Test case 6
print("\033[1m\033[4mTest case 6\033[0m")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print(atm.withdraw(card.account, -500))
print(SEPARATOR)

# Test case 7
print("\033[1m\033[4mTest case 7\033[0m")
atm = bank.get_atm('1001')
sender_card = atm.insert_card('12345', '1234')
receiver_card = atm.insert_card('12346', '1234')
print(f'Sender balance before: {sender_card.account.balance}')
print(f'Receiver balance before: {receiver_card.account.balance}')
print(atm.transfer(sender_card.account, receiver_card.account, 300))
print(f'Sender balance after: {sender_card.account.balance}')
print(f'Receiver balance after: {receiver_card.account.balance}')
print(SEPARATOR)

# Test case 8
print("\033[1m\033[4mTest case 8\033[0m")
atm = bank.get_atm('1001')
sender_card = atm.insert_card('12345', '1234')
receiver_card = atm.insert_card('12346', '1234')
print(atm.transfer(sender_card.account, receiver_card.account, -300))
print(SEPARATOR)

# Test case 9
print("\033[1m\033[4mTest case 9\033[0m")
atm = bank.get_atm('1001')
sender_card = atm.insert_card('12345', '1234')
receiver_card = atm.insert_card('12346', '1234')
print(atm.transfer(sender_card.account, receiver_card.account, 20000))
print(SEPARATOR)

# Test case 10
print("\033[1m\033[4mTest case 10\033[0m")
atm_machine = bank.get_atm('1002')
account = atm_machine.insert_card('12345', '1234')
print(f"ATM machine balance before: {atm_machine.atm_balance:,}")
print("Attempting to withdraw 250,000 baht...")
result = atm_machine.withdraw(account, 250000)
print("Expected result: ATM has insufficient funds")
print(f"Actual result: {result}")
print(f"ATM machine balance after: {atm_machine.atm_balance:,}")
print(SEPARATOR)
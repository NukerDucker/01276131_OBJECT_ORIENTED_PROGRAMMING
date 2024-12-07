class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__accounts = []

    def get_citizen_id(self):
        return self.__citizen_id

    def get_name(self):
        return self.__name

    def add_account(self, account):
        self.__accounts.append(account)

    def get_accounts(self):
        return self.__accounts


class Account:
    def __init__(self, account_number: str, owner: User, balance: float = 0.0):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = balance
        self.__transactions = []

    def get_account_number(self):
        return self.__account_number

    def get_owner(self):
        return self.__owner

    def get_balance(self):
        return self.__balance

    def deposit(self, amount: float, atm_id: str):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(('D', amount, atm_id))
        else:
            raise ValueError("Cannot deposit a negative amount")

    def withdraw(self, amount: float, atm_id: str):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(('W', amount, atm_id))
        else:
            raise ValueError("Insufficient funds or invalid amount")

    def transfer(self, amount: float, atm_id: str, target_account):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(('TW', amount, atm_id, target_account.get_account_number()))
            target_account.deposit(amount, atm_id)
            target_account.add_transaction(('TD', amount, atm_id, self.__account_number))
        else:
            raise ValueError("Insufficient funds or invalid amount")

    def add_transaction(self, transaction):
        self.__transactions.append(transaction)

    def get_transactions(self):
        return self.__transactions


class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin

    def get_card_number(self):
        return self.__card_number

    def get_account(self):
        return self.__account

    def get_pin(self):
        return self.__pin


class ATMMachine:
    MAX_WITHDRAWAL_PER_DAY = 40000
    ANNUAL_FEE = 150

    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__amount = initial_amount

    def insert_card(self, card: ATMCard, pin: str):
        if card.get_pin() == pin:
            return card.get_account()
        else:
            raise ValueError("Invalid PIN")

    def deposit(self, card: ATMCard, amount: float):
        account = card.get_account()
        account.deposit(amount, self.__machine_id)
        self.__amount += amount

    def withdraw(self, card: ATMCard, amount: float):
        if amount > self.MAX_WITHDRAWAL_PER_DAY:
            raise ValueError("Exceeds daily withdrawal limit of 40,000 baht")
        if amount > self.__amount:
            raise ValueError("ATM has insufficient funds")
        account = card.get_account()
        account.withdraw(amount, self.__machine_id)
        self.__amount -= amount

    def transfer(self, card: ATMCard, amount: float, target_account: Account):
        if amount > self.MAX_WITHDRAWAL_PER_DAY:
            raise ValueError("Exceeds daily withdrawal limit of 40,000 baht")
        account = card.get_account()
        account.transfer(amount, self.__machine_id, target_account)
        self.__amount -= amount

    def get_machine_id(self):
        return self.__machine_id

    def get_amount(self):
        return self.__amount
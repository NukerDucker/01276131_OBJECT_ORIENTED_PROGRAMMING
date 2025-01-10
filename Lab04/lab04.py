class User:
    def __init__(self, citizen_id: str, name: str) -> None:
        self.__citizen_id: str = citizen_id
        self.__name: str = name
        self.__accounts: list[Account] = []

    @property
    def citizen_id(self) -> str:
        return self.__citizen_id

    @property
    def full_name(self) -> str:
        return self.__name

    @property
    def accounts(self) -> list:
        return self.__accounts

    def add_account(self, account: 'Account') -> None:
        self.__accounts.append(account)

    def search_account(self, account_number: str) -> 'Account | None':
        for account in self.__accounts:
            if account.account_number == account_number:
                return account
        return None

class Account:
    def __init__(self, account_number: str, owner: User, initial_balance: float = 0.0) -> None:
        self.__account_number: str = account_number
        self.__owner: User = owner
        self.__balance: float = initial_balance
        self.__transactions: list[Transaction] = []

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def amount(self) -> float:
        return self.__balance

    @property
    def transactions(self) -> list['Transaction']:
        return self.__transactions

    @amount.setter
    def amount(self, balance: float) -> None:
        self.__balance = balance

    def add_transaction(self, transaction: 'Transaction') -> None:
        self.__transactions.append(transaction)

    def transfer(self, amount: float, receiver: 'Account') -> str:
        if amount <= 0:
            return "Invalid amount"
        if amount > self.__balance:
            return "Insufficient funds"
        self.__balance -= amount
        receiver.__balance += amount
        self.add_transaction(Transaction('TW', amount, self.__account_number, receiver.account_number, source='ACC'))
        receiver.add_transaction(Transaction('TD', amount, receiver.account_number, self.__account_number, source='ACC'))

    def __add__(self, amount: float) -> None:
        self.__balance += amount

    def __sub__(self, amount: float) -> None:
        self.__balance -= amount

    def __iter__(self):
        return iter(self.__transactions)


class SavingsAccount(Account):
    interest_rate: float = 0.5
    type: str = "Saving"

    def __init__(self, account_number: str, user: User, amount: float, card: 'Card | None' = None) -> None:
        super().__init__(account_number, user, amount)
        self.__card: Card | None = card

    @property
    def card(self) -> 'Card | None':
        return self.__card

    @card.setter
    def card(self, card: 'Card | None') -> None:
        self.__card = card


class FixDepositAccount(Account):
    interest_rate: float = 2.5
    type: str = "Fix Deposit"

    def __init__(self, account_number: str, user: User, amount: float, card: 'Card | None' = None) -> None:
        super().__init__(account_number, user, amount)


class Card:
    def __init__(self, card_no: str, account: Account, pin: str) -> None:
        self.__card_no: str = card_no
        self.__account: Account = account
        self.__pin: str = pin

    @property
    def account(self) -> Account:
        return self.__account

    @property
    def pin(self) -> str:
        return self.__pin

    @property
    def card_no(self) -> str:
        return self.__card_no

    @property
    def amount(self) -> float:
        return self.__account.amount

    @property
    def account_no(self) -> str:
        return self.__account.account_number
class ATMCard(Card):
    FEE: int = 150

    def __init__(self, card_no: str, account: Account, pin: str = '0000') -> None:
        super().__init__(card_no, account, pin)
    

class DebitCard(ATMCard):
    FEE: int = 300
    
    def __init__(self, card_no: str, account: Account, pin: str = '0000') -> None:
        super().__init__(card_no, account, pin)

class ATM:
    MAXIMUM_WITHDRAWAL: int = 20_000

    def __init__(self, machine_id: str, initial_amount: float = 1_000_000):
        self.__machine_id = machine_id
        self.__atm_balance = initial_amount

    @property
    def machine_id(self) -> str:
        return self.__machine_id

    @property
    def atm_balance(self) -> float:
        return self.__atm_balance

    def insert_card(self, card: Card, pin: str) -> str:
        if card.pin == pin:
            return "Success"
        return "Invalid card or PIN"

    def deposit(self, account: Account, amount: float) -> None | str:
        if amount < 0:
            return "Invalid amount"
        account + amount
        account.add_transaction(Transaction('D', amount, self.__machine_id, source='ATM'))
        self.__atm_balance += amount           

    def withdraw(self, account: Account, amount: float) -> str | None:
        if amount <= 0:
            return "Withdrawal amount must be positive"
        if amount > self.__atm_balance:
            return 'ATM has insufficient funds'
        if amount > self.MAXIMUM_WITHDRAWAL:
            return f'Exceeds daily maximum withdrawal limit of {self.MAXIMUM_WITHDRAWAL:,} baht'
        if amount > account.amount:
            return "Insufficient account balance"
        account - amount
        account.add_transaction(Transaction('W', amount, self.__machine_id, source='ATM'))
        self.__atm_balance -= amount


    def transfer(self, sender: Account, receiver: Account, amount: float) -> str | None:
        if amount <= 0:
            return "Transfer amount must be positive"
        if amount > sender.balance:
            return "Insufficient sender account balance"
        sender - amount
        receiver + amount
        sender.add_transaction(Transaction('TW', amount, self.__machine_id, receiver.account_number, source='ATM'))
        receiver.add_transaction(Transaction('TD', amount, self.__machine_id, sender.account_number, source='ATM'))


class Transaction:
    def __init__(self, transaction_type: str, amount: float, machine_id: str, account_number: str = None, source: str = None) -> None:
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__machine_id = machine_id
        self.__destination = account_number
        self.__source = source

    def __str__(self) -> str: 
        if self.__transaction_type in ('TW', 'TD', 'P', 'R'):
            return f"{self.__transaction_type}-{self.__source} : {self.__machine_id}-{self.__amount}-{self.__destination}"
        return f"{self.__transaction_type}-{self.__source} : {self.__machine_id}-{self.__amount}"

class Seller:
    def __init__(self, seller_id: str, name: str):
        self.__seller_id = seller_id
        self.__name = name
        self.__edc = []

    @property
    def seller_id(self) -> str:
        return self.__seller_id

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def edc(self) -> list:
        return self.__edc
    
    def add_edc(self, edc) -> None:
        self.__edc.append(edc)
        
    def search_edc_from_no(self, edc_no: str) -> 'EDCMachine':
        for edc in self.__edc:
            if edc.edc_id == edc_no:
                return edc
    def paid(self, card: Card, amount: float, seller_account: Account) -> str:
        if amount <= 0:
            return "Payment amount must be positive"
        if card.amount < amount:
            return "Insufficient funds"
        card - amount
        seller_account + amount 
        card.add_transaction(Transaction('P', amount, self.__seller_id, seller_account.account_number, source='COUT'))
        seller_account.add_transaction(Transaction('R', amount, self.__seller_id,card.account_number, source='COUT'))
        return "Payment successful"
class EDCMachine:
    def __init__(self, edc_id: str, seller: Seller) -> None:
        self.__edc_id = edc_id
        self.__seller = seller

    @property
    def edc_id(self) -> str:
        return self.__edc_id

    @property
    def seller(self) -> Seller:
        return self.__seller

    def paid(self, card: Card, amount: float, seller_account: Account) -> str:
        if amount <= 0:
            return "Payment amount must be positive"
        if card.account.amount < amount:
            return "Insufficient funds"
        card.account - amount
        seller_account + amount
        card.account.add_transaction(Transaction('P', amount, self.__edc_id, seller_account.account_number, source='EDC'))
        seller_account.add_transaction(Transaction('R', amount, self.__edc_id, card.account.account_number, source='EDC'))
        return "Payment successful"    

class Bank:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__users = []
        self.__atms = []
        self.__sellers = []
        
    @property
    def name(self) -> str:
        return self.__name

    def add_user(self, user: User) -> None:
        self.__users.append(user)

    def add_atm(self, atm: ATM) -> None:
        self.__atms.append(atm)
        
    def add_seller(self, seller) -> None:
        self.__sellers.append(seller)

    def search_user_from_id(self, citizen_id: str) -> User:
        for user in self.__users:
            if user.citizen_id == citizen_id:
                return user
            
    def search_atm_machine(self, machine_id: str) -> ATM:
        for atm in self.__atms:
            if atm.machine_id == machine_id:
                return atm
            
    def search_account_from_card(self, card_no: str) -> Account:
        for user in self.__users:
            for account in user.accounts:
                if account.card.card_no == card_no:
                    return account
                
    def search_account_from_account_no(self, account_no: str) -> Account:
        for user in self.__users:
            for account in user.accounts:
                if account.account_number == account_no:
                    return account
                
    def search_seller(self, name: str) -> Seller:
        for seller in self.__sellers:
            if seller.name == name:
                return seller

    
###############################################
def seperator():
    print("-------------------------\n")

user = {
    '1-1101-12345-12-0': [['Harry Potter', 'Savings', '1234567890', 20000, 'ATM', '12345', '1234']],
    '1-1101-12345-13-0': [['Hermione Jean Granger', 'Saving', '0987654321', 1000, 'Debit', '12346', '1234'],['Hermione Jean Granger', 'Fix Deposit', '0987654322', 1000, '', '']],
    '9-0000-00000-01-0': [['KFC', 'Savings', '0000000321', 0, '', '']],
    '9-0000-00000-02-0': [['Tops', 'Savings', '0000000322', 0, '', '']]
}

atm ={'1001':1000000,'1002':200000}

seller_dic = {'210':"KFC", '220':"Tops"}

EDC = {'2101':"KFC", '2201':"Tops"}

################################################
scb = Bank('SCB')
for citizen_id, data in user.items():
    for info in data:
        user = User(citizen_id, info[0])
        account = Account(info[2], user, info[3])
        user.add_account(account)
        if info[4] == 'ATM':
            card = ATMCard(info[5], account, info[6])
        elif info[4] == 'Debit':
            card = DebitCard(info[5], account, info[6])
        account.card = card
        scb.add_user(user)
        
for machine_id, atm_balance in atm.items():
    atm = ATM(machine_id, atm_balance)
    scb.add_atm(atm)

for seller_id, name in seller_dic.items():
    seller = Seller(seller_id, name)
    scb.add_seller(seller)
    for edc_id, edc_seller_name in EDC.items():
        if edc_seller_name == name:
            edc = EDCMachine(edc_id, seller)
            seller.add_edc(edc)
            
print("Welcome to SCB Bank")
seperator()

# Test case #1: Test deposit from an ATM using Harry's ATM card.
# The card must be inserted first. Locate ATM machine 1 and Harry's ATM card.
# Then call the function or method `deposit` from the ATM machine and use `+` from the account.
# Expected outcome:
# Test Case #1
# Harry's ATM No :  12345
# Harry's Account No :  1234567890
# Success
# Harry account before deposit :  20000
# Deposit 1000
# Harry account after deposit :  21000

atm_machine = scb.search_atm_machine('1001')
harry_account = scb.search_account_from_card('12345')
atm_card = harry_account.card
print(atm_card.account_no)
print("Test Case #1")
print("Harry's ATM No : ",atm_card.card_no)
print("Harry's Account No : ",harry_account.account_number)
print(atm_machine.insert_card(atm_card, "1234"))
print("Harry account before deposit : ",harry_account.amount)
print("Deposit 1000")
atm_machine.deposit(harry_account,1000)
print("Harry account after deposit : ",harry_account.amount)
print("")
seperator()

'''----------------------------------------------------------'''
# Test case #2: Test withdrawal from an ATM using Hermione's ATM card.
# The card must be inserted first. Locate ATM machine 2 and Hermione's ATM card.
# Then call the function or method `withdraw` from the ATM machine and use `-` from the account.
# Expected outcome:
# Test Case #2
# Hermione's ATM No :  12346
# Hermione's Account No :  0987654321
# Success
# Hermione account before withdraw :  2000
# withdraw 1000
# Hermione account after withdraw :  1000

atm_machine = scb.search_atm_machine('1002')
hermione_account = scb.search_account_from_card('12346')
atm_card = hermione_account.card
print("Test Case #2")
print("Hermione's ATM No : ", atm_card.card_no)
print("Hermione's Account No : ", hermione_account.account_number)
print(atm_machine.insert_card(atm_card, "1234"))
print("Hermione account before withdraw : ",hermione_account.amount)
print("withdraw 1000")
atm_machine.withdraw(hermione_account,1000)
print("Hermione account after withdraw : ",hermione_account.amount)
print("")
seperator()

'''----------------------------------------------------------'''
# Test case #3: Test transferring 10,000 THB from Harry's account to Hermione's account at the counter.
# Call the method for performing the money transfer.
# Expected outcome:
# Test Case #3
# Harry's Account No :  1234567890
# Hermione's Account No :  0987654321
# Harry account before transfer :  21000
# Hermione account before transfer :  1000
# Harry account after transfer :  11000
# Hermione account after transfer :  11000

harry_account = scb.search_account_from_card('12345')
hermione_account = scb.search_account_from_card('12346')
print("Test Case #3")
print("Harry's Account No : ",harry_account.account_number)
print("Hermione's Account No : ", hermione_account.account_number)
print("Harry account before transfer : ",harry_account.amount)
print("Hermione account before transfer : ",hermione_account.amount)
harry_account.transfer(10000, hermione_account)
print("Harry account after transfer : ",harry_account.amount)
print("Hermione account after transfer : ",hermione_account.amount)
print("")
seperator()
    
'''----------------------------------------------------------'''

# Test case #4: Test payment using a card reader. Call the `paid` method from the card reader.
# Hermione makes a payment of 500 THB to KFC using her own card.
# Expected outcome:
# Hermione's Debit Card No :  12346
# Hermione's Account No :  0987654321
# Seller :  KFC
# KFC's Account No :  0000000321
# KFC account before paid :  0
# Hermione account before paid :  11000
# KFC account after paid :  500
# Hermione account after paid :  10500

hermione_account = scb.search_account_from_account_no('0987654321')
debit_card = hermione_account.card
kfc_account = scb.search_account_from_account_no('0000000321')
kfc = scb.search_seller('KFC')
edc = kfc.search_edc_from_no('2101')

print("Test Case #4")
print("Hermione's Debit Card No : ", debit_card.card_no)
print("Hermione's Account No : ",hermione_account.account_number)
print("Seller : ", kfc.name)
print("KFC's Account No : ", kfc_account.account_number)
print("KFC account before paid : ",kfc_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
edc.paid(debit_card, 500, kfc_account)
print("KFC account after paid : ",kfc_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")
seperator()

'''----------------------------------------------------------'''
# Test case #5: Test electronic payment by calling the `paid` method from KFC.
# Hermione makes a payment of 500 THB to Tops.
# Expected outcome:
# Test Case #5
# Hermione's Account No :  0987654321
# Tops's Account No :  0000000322
# Tops account before paid :  0
# Hermione account before paid :  10500
# Tops account after paid :  500
# Hermione account after paid :  10000

hermione_account = scb.search_account_from_account_no('0987654321')
debit_card = hermione_account.card
tops_account = scb.search_account_from_account_no('0000000322')
tops = scb.search_seller('Tops')
print("Test Case #5")
print("Hermione's Account No : ",hermione_account.account_number)
print("Tops's Account No : ", tops_account.account_number)
print("Tops account before paid : ",tops_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
tops.paid(hermione_account,500,tops_account)
print("Tops account after paid : ",tops_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")
seperator()

'''----------------------------------------------------------'''
# Test case #6: Display all transactions of Hermione using a `for` loop.
print("Test Case #7")
hermione_account = scb.search_account_from_account_no('0987654321')
print("Hermione's Account No : ",hermione_account.account_number)
print("Transaction : ")
for transaction in hermione_account:
    print(transaction)
seperator()

'''----------------------------------------------------------'''
# Test case #7: Display all transactions of Harry using a `for` loop.
print("Test Case #8")
harry_account = scb.search_account_from_account_no('1234567890')
print("Harry's Account No : ",harry_account.account_number)
print("Transaction : ")
for transaction in harry_account:
    print(transaction)
seperator()
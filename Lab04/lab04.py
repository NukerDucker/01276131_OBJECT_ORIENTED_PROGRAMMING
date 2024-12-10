class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__accounts = []

    @property
    def citizen_id(self) -> str:
        return self.__citizen_id

    @property
    def full_name(self) -> str:
        return self.__name
    
    @property
    def accounts(self):
        return self.__accounts

    def add_account(self, account):
        self.__accounts.append(account)

    def search_account(self, account_number: str):
        for account in self.__accounts:
            if account.account_number == account_number:
                return account
            
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
    def amount(self) -> float:
        return self.__balance

    @property
    def transactions(self) -> list:
        return self.__transactions
    
    @amount.setter
    def amount(self, balance: float):
        self.__balance = balance

    def add_transaction(self, transaction):
        self.__transactions.append(transaction)
        
    def transfer(self, amount: float, receiver):
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                receiver.__balance += amount
                # Use '*' for direct transfers
                self.add_transaction(Transaction('TW', amount, self.__account_number, receiver.account_number, source='ACC'))
                receiver.add_transaction(Transaction('TD', amount, receiver.account_number, self.__account_number, source='ACC'))
            else:
                return "Insufficient funds"
        else:
            return "Invalid amount"

        
    def __add__(self, amount: float):
        self.__balance += amount
        
    def __sub__(self, amount: float):
        self.__balance -= amount
        
    def __iter__(self):
        return iter(self.__transactions)

class SavingsAccount(Account):
    interest_rate = 0.5
    type = "Saving"

    def __init__(self, account_number, user, amount, card=None):
        super().__init__(account_number, user, amount)
        self.__card = card
        
    @property
    def card(self):
        return self.__card
    
    @card.setter
    def card(self, card):
        self.__card = card
        
class FixDepositAccount(Account):
    interest_rate = 2.5
    type = "FixDeposit"

    def __init__(self, account_number, user, amount, card=None):
        super().__init__(account_number, user, amount)
    
class Card:
    def __init__(self, card_no, account, pin):
        self.__card_no = card_no
        self.__account = account
        self.__pin = pin
    
    @property
    def account(self):
        return self.__account
    
    @property
    def pin(self):
        return self.__pin
    
    @property
    def card_no(self):
        return self.__card_no
    
    @property
    def amount(self) -> float:
        return self.__account.amount
        
    @property
    def account_no(self) -> str:
        return self.__account.account_number

class ATMCard(Card):
    FEE = 150
    
    def __init__(self, card_no: str, account: Account, pin: str = '0000'):
        super().__init__(card_no, account, pin)
    

class DebitCard(ATMCard):
    FEE = 300
    
    def __init__(self, card_no: str, account: Account, pin: str = '0000'):
        super().__init__(card_no, account, pin)


class ATMMachine:
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

    def insert_card(self, card: Card, pin: str):
        if card.pin == pin:
            return "Success"
        return "Invalid card or PIN"

    def deposit(self, account: Account, amount: float):
        if amount > 0:
            account + amount
            # Use ATM ID as machine_id
            account.add_transaction(Transaction('D', amount, self.__machine_id, source='ATM'))
            self.__atm_balance += amount
        else:
            return "Invalid amount"

    def withdraw(self, account: Account, amount: float):
        if amount <= 0:
            return "Withdrawal amount must be positive"
        if amount > self.__atm_balance:
            return 'ATM has insufficient funds'
        if amount > self.MAXIMUM_WITHDRAWAL:
            return f'Exceeds daily maximum withdrawal limit of {self.MAXIMUM_WITHDRAWAL:,} baht'
        if amount > account.amount:
            return "Insufficient account balance"
        account - amount
        # Use ATM ID as machine_id
        account.add_transaction(Transaction('W', amount, self.__machine_id, source='ATM'))
        self.__atm_balance -= amount


    def transfer(self, sender: Account, receiver: Account, amount: float):
        if amount <= 0:
            return "Transfer amount must be positive"
        if amount > sender.balance:
            return "Insufficient sender account balance"
        sender - amount
        receiver + amount
        sender.add_transaction(Transaction('TW', amount, self.__machine_id, receiver.account_number, source='ATM'))
        receiver.add_transaction(Transaction('TD', amount, self.__machine_id, sender.account_number, source='ATM'))


class Transaction:
    def __init__(self, transaction_type: str, amount: float, machine_id: str, account_number: str = None, source: str = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__machine_id = machine_id  # Update machine_id dynamically
        self.__destination = account_number
        self.__source = source

    def __str__(self):
        if self.__transaction_type in ('TW', 'TD', 'P', 'R'):
            return f"{self.__transaction_type}-{self.__source} : {self.__machine_id}-{self.__amount}-{self.__destination}"
        return f"{self.__transaction_type}-{self.__source} : {self.__machine_id}-{self.__amount}"


class Bank:
    def __init__(self, name: str):
        self.__name = name
        self.__users = []
        self.__atms = []
        self.__sellers = []
        
    @property
    def name(self) -> str:
        return self.__name

    def add_user(self, user: User):
        self.__users.append(user)

    def add_atm(self, atm: ATMMachine):
        self.__atms.append(atm)
        
    def add_seller(self, seller):
        self.__sellers.append(seller)

    def search_user_from_id(self, citizen_id: str) -> User:
        for user in self.__users:
            if user.citizen_id == citizen_id:
                return user
            
    def search_atm_machine(self, machine_id: str) -> ATMMachine:
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
                
    def search_seller(self, name: str):
        for seller in self.__sellers:
            if seller.name == name:
                return seller

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
    def edc(self):
        return self.__edc
    
    def add_edc(self, edc):
        self.__edc.append(edc)
        
    def search_edc_from_no(self, edc_no: str):
        for edc in self.__edc:
            if edc.edc_id == edc_no:
                return edc
    def paid(self, card: Card, amount: float, seller_account: Account):
        if amount <= 0:
            return "Payment amount must be positive"
        if card.amount >= amount:
            card - amount
            seller_account + amount 
            
            card.add_transaction(Transaction('P', amount, self.__seller_id, seller_account.account_number, source='COUT'))
            seller_account.add_transaction(Transaction('R', amount, self.__seller_id,card.account_number, source='COUT'))
            return "Payment successful"
        else:
            return "Insufficient funds"

class EDCMachine:
    def __init__(self, edc_id: str, seller: Seller):
        self.__edc_id = edc_id
        self.__seller = seller

    @property
    def edc_id(self) -> str:
        return self.__edc_id

    @property
    def seller(self) -> Seller:
        return self.__seller

    def paid(self, card: Card, amount: float, seller_account: Account):
        if amount <= 0:
            return "Payment amount must be positive"
        if card.account.amount >= amount:
            card.account - amount  # Deduct amount from the user's account
            seller_account + amount  # Add the amount to the seller's account

            # Use EDC ID as machine_id
            card.account.add_transaction(Transaction('P', amount, self.__edc_id, seller_account.account_number, source='EDC'))
            seller_account.add_transaction(Transaction('R', amount, self.__edc_id, card.account.account_number, source='EDC'))
            return "Payment successful"
        else:
            return "Insufficient funds"


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
    atm = ATMMachine(machine_id, atm_balance)
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

# Test case #1 : ทดสอบ การฝาก จากเครื่อง ATM โดยใช้บัตร ATM ของ harry
# ต้องมีการ insert_card ก่อน ค้นหาเครื่อง atm เครื่องที่ 1 และบัตร atm ของ harry
# และเรียกใช้ function หรือ method deposit จากเครื่อง ATM และเรียกใช้ + จาก account
# ผลที่คาดหวัง :
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
# Test case #2 : ทดสอบ การถอน จากเครื่อง ATM โดยใช้บัตร ATM ของ hermione
# ต้องมีการ insert_card ก่อน ค้นหาเครื่อง atm เครื่องที่ 2 และบัตร atm ของ hermione
# และเรียกใช้ function หรือ method withdraw จากเครื่อง ATM และเรียกใช้ - จาก account
# ผลที่คาดหวัง :
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
# Test case #3 : ทดสอบการโอนเงินจากบัญชีของ Harry ไปยัง Hermione จำนวน 10000 บาท ที่เคาน์เตอร์
# ให้เรียกใช้ method ที่ทำการโอนเงิน
# ผลที่คาดหวัง
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

# Test case #4 : ทดสอบการชำระเงินจากเครื่องรูดบัตร ให้เรียกใช้ method paid จากเครื่องรูดบัตร
# โดยให้ hermione ชำระเงินไปยัง KFC จำนวน 500 บาท ผ่านบัตรของตัวเอง
# ผลที่คาดหวัง
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
# Test case #5 : ทดสอบการชำระเงินแบบอิเล็กทรอนิกส์ ให้เรียกใช้ method paid จาก kfc
# โดยให้ Hermione ชำระเงินไปยัง Tops จำนวน 500 บาท
# ผลที่คาดหวัง
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
# Test case #7 : แสดง transaction ของ Hermione ทั้งหมด โดยใช้ for loop 

print("Test Case #7")
hermione_account = scb.search_account_from_account_no('0987654321')
print("Hermione's Account No : ",hermione_account.account_number)
print("Transaction : ")
for transaction in hermione_account:
    print(transaction)
seperator()

'''----------------------------------------------------------'''
# Test case #8 : แสดง transaction ของ Harry ทั้งหมด โดยใช้ for loop
print("Test Case #8")
harry_account = scb.search_account_from_account_no('1234567890')
print("Harry's Account No : ",harry_account.account_number)
print("Transaction : ")
for transaction in harry_account:
    print(transaction)
seperator()
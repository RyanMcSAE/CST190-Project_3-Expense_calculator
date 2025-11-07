from enum import Enum
from datetime import date, timedelta
from typing import List
import os
import json
# from os.path import exists # <- "exists" can be used instead of "os.path.exists" 
# import date
# from abc import ABCMeta, abstractmethod, abstractstaticmethod


# Need to implement some checks here for new files and last_used_ID being null / none
class UniqueIDGenerator():
    _last_ID_used: int

    @staticmethod
    def __init__(last_used_ID: int):
        UniqueIDGenerator._last_used_ID: int = last_used_ID

    @staticmethod
    def generate_ID() -> int:
        UniqueIDGenerator._last_used_ID += 1
        return UniqueIDGenerator._last_used_ID
    
    @staticmethod
    def get_last_used_ID() -> int:
        return UniqueIDGenerator._last_ID_used

# Enum probably not the best choice as modification in future may produce errors
class ExpenseType(Enum):
    Other = 1
    Repayment = 2
    Discretionary = 3
    Bill = 4
    Mortgage = 5

class Expense:
    
    def __init__(self, _ID: int, _name: str, _amount: int, _expense_type: ExpenseType, _date_of_expense: date):
        self._ID: int = _ID
        self._name: str = _name
        self._amount: int = _amount
        self._expense_type: ExpenseType = _expense_type
        self._date_of_expense: date = _date_of_expense

    # No ID setter required as ID field should not be changed after initialisation of object

    def get_ID(self):
        return self._ID  

    def get_name(self):
        return self._name
    
    def set_name(self, name: str):
        self._name = name

    # Expense amount is stored in cents and as int type variable, getter should return in either cents (int) or dollars (float) as dictated by caller,
    # setter should be able to take in cents (int) or dollars (float) and convert to int for attribute assignment as required

    def get_amount_in_cents(self):
        return self._amount    

    def get_amount_in_decimal(self):
        x: float = float(self._amount) / 100
        return x
    
    def set_amount_in_cents(self, amount: int):
        self._amount = amount

    def set_amount_in_decimal(self, amount: float):
        x: int = int(amount * 100)
        self._amount = x

    def get_expense_type(self):
        return self._expense_type.name
    
    def set_expense_type(self, expense_type: ExpenseType):
        self._expense_type = expense_type

    def get_date_of_expense(self):
        return self._date_of_expense
    
    def set_date_of_expense(self, date_of_expense: date):
        self._date_of_expense = date_of_expense


    # def get_info(self) -> str:
    #     s = ""
    #     s += "Expense ID: " + str(self.get_ID()) + "\n"
    #     s += "Name: " + str(self.get_name()) + "\n"
    #     s += "Amount: $" + str(self.get_amount_in_decimal()) + "\n"
    #     s += "Expense Type: " + str(self.get_expense_type()) + "\n"
    #     s += "Date of Expense: " + str(self.get_date_of_expense())
    #     return s
    
    def get_info(self) -> str:
        s = ""
        s += "Expense ID: " + str(self._ID) + "\n"
        s += "Name: " + str(self._name) + "\n"
        s += "Amount: $" + str(self.get_amount_in_decimal()) + "\n"
        s += "Expense Type: " + str(self.get_expense_type()) + "\n"
        s += "Date of Expense: " + str(self.get_date_of_expense())
        return s

class ReoccurringExpense:

    def __init__(self, ID: int, name: str, amount: int, expense_type: ExpenseType, frequency: int, start_date: date, end_date: date, expense_list: List[Expense] = None):
        self._ID: int = ID
        self._name: str = name
        self._amount: int = amount
        self._expense_type: ExpenseType = expense_type
        self._frequency: int = frequency
        self._start_date: date = start_date
        self._end_date: date = end_date
        self._expense_list: List[Expense] = expense_list
        # self._expense_list: List[Expense] = []

        ### Populate _expense_list if no List[Expense] provided in parameters
        if self._expense_list == None:
            self._current_date: date = self._start_date
            while self._current_date <= self._end_date:
                n = Expense(UniqueIDGenerator.generate_ID(), self._name, self._amount, self._expense_type, self._current_date)
                self._expense_list.append(n)
                self._current_date += timedelta(days = self._frequency)
 
    # No ID setter required as ID should remain constant after object creation
    def get_ID(self):
        return self._ID
    
    def get_name(self):
        return self._name
    
    def set_name(self, name: str):
        self._name: str = name
    
    def get_expense_type(self):
        return self._expense_type
    
    def set_expense_type(self, expense_type: ExpenseType):
        self._expense_type = expense_type

    def get_frequency(self):
        return self._frequency

    def set_frequency(self, frequency: int):
        self._frequency = frequency

    def get_start_date(self) -> date:
        return self._start_date
    
    def set_start_date(self, start_date: date):
        self._start_date = start_date

    def get_end_date(self):
        return self._end_date
    
    def get_expense_list(self) -> List[Expense]:
        return self._expense_list
    
    def get_info(self) -> str:
        s = "Type: Reoccurring Expense" + "\n"
        s += "ID: " + str(self.get_ID()) + "\n"
        s += "Name: " + str(self.get_name()) + "\n"
        s += "Frequency: " + str(self.get_frequency()) + "\n"
        s += "Start Date: " + str(self.get_start_date()) + "\n"
        s += "End Date: " + str(self.get_end_date()) + "\n"
        s += "-----  Expenses -----" + "\n"
        for expense in self._expense_list:
            s += expense.get_info() + "\n"
            s += " - - - - - - - - - - -" + "\n"
        # s += str(self._expense_list[0].get_info())


        # s += str(type(self._expense_list)) + "\n"
        # s += str(type(self._expense_list[0])) + "\n"
        # s += str(self._expense_list[0]) + "\n"
        # s += str(self._expense_list[1]) + "\n"
        # s += str(self._expense_list[2]) + "\n"
        # s += str(self._expense_list[3])
        return s
            
    

def main():
    testing()

def testing():
    print("\n" + "------------------------- TESTING -------------------------" + "\n")
    reoccurring_expenses = load_reoccurring_save_file()
    print(reoccurring_expenses[0].get_info())
    

def create_expense_obj_from_dict(expense: dict) -> Expense:
    id = expense["id"]
    name = expense["name"]
    amount = expense["amount"]

    t = expense["expense_type"]
    expense_type: ExpenseType = ExpenseType(t)

    s: str = str(expense["date_of_expense"])
    year: int = int(s[0:4])
    month: int = int(s[4:6])
    day: int = int(s[6:8])
    date_of_expense: date = date(year, month, day)

    expense: Expense = Expense(id, name, amount, expense_type, date_of_expense)
    return expense
    
# UniqueIDGenerator needs to be set up when load files functions are combined
def load_save_file() -> List[Expense]:
    path = os.getcwd() + r'\Expense Data.json'
    with open(path) as f:
        expenses = json.load(f)

    expense_list: List[Expense] = []

    for index in range(len(expenses["Expense"])):
        id = expenses["Expense"][index]["id"]
        name = expenses["Expense"][index]["name"]
        amount = expenses["Expense"][index]["amount"]

        t = expenses["Expense"][index]["expense_type"]
        expense_type: ExpenseType = ExpenseType(t)

        s: str = str(expenses["Expense"][index]["date_of_expense"])
        year: int = int(s[0:4])
        month: int = int(s[4:6])
        day: int = int(s[6:8])
        date_of_expense: date = date(year, month, day)

        expense: Expense = Expense(id, name, amount, expense_type, date_of_expense)
        expense_list.append(expense)

    return expense_list


def load_reoccurring_save_file() -> List[ReoccurringExpense]:
    path = os.getcwd() + r'\Expense Data.json'
    with open(path) as f:
        expenses = json.load(f)

    reoccurring_expenses: List[ReoccurringExpense] = []
    for index in range(len(expenses["ReoccurringExpense"])):
        id = expenses["ReoccurringExpense"][index]["id"]
        name = expenses["ReoccurringExpense"][index]["name"]
        amount = expenses["ReoccurringExpense"][index]["amount"]

        t = expenses["ReoccurringExpense"][index]["expense_type"]
        expense_type: ExpenseType = ExpenseType(t)

        frequency = expenses["ReoccurringExpense"][index]["frequency"]
        s: str = str(expenses["ReoccurringExpense"][index]["start_date"])
        year: int = int(s[0:4])
        month: int = int(s[4:6])
        day: int = int(s[6:8])
        start_date: date = date(year, month, day)

        s: str = str(expenses["ReoccurringExpense"][index]["end_date"])
        year: int = int(s[0:4])
        month: int = int(s[4:6])
        day: int = int(s[6:8])
        end_date: date = date(year, month, day)

        expense_list: List[Expense] = []
        # for expense in expenses["ReoccurringExpense"][index]["expense_list"]:
        #     expense_list.append(expense)

        for expense_dict in expenses["ReoccurringExpense"][index]["expense_list"]:
            expense_obj: Expense = create_expense_obj_from_dict(expense_dict)
            expense_list.append(expense_obj)

        m: ReoccurringExpense = ReoccurringExpense(id, name, amount, expense_type, frequency, start_date, end_date, expense_list)
        reoccurring_expenses.append(m)

    return reoccurring_expenses


def save_file_exists() -> bool:
    path = os.getcwd() + r'\Expense Data.json'
    file_exists = os.path.exists(path)
    return file_exists

def create_save_file() -> bool:
    try:
        path = os.getcwd() + r'\Expense Data.json'
        with open(path, "w") as f:
            f.close
        return True
    except:
        return False
    
def save_file_delete() -> bool:
    try:
        path = os.getcwd() + r'\Expense Data.json'
        os.remove(path)
        return True
    except:
        return False



def testing_generate_expense() -> Expense:
    n = Expense(UniqueIDGenerator.generate_ID(), "Electricity Bill", 14508, ExpenseType(1), date(2022, 12, 10))
    return n

def testing_generate_reoccurring_expense() -> ReoccurringExpense:
    m = ReoccurringExpense(UniqueIDGenerator.generate_ID(), "Hamburger Payments", 1500, ExpenseType(3), 3, date(2025,9,9), date(2025, 11, 11))
    return m


    
# Fuck python and this shitty conditional statement having to exist at the very end of the code for anythin above it run 
if __name__ == "__main__":
    main()

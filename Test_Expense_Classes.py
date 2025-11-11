from enum import Enum
from datetime import date, timedelta
from typing import List, Union
import os
import json
# from os.path import exists # <- "exists" can be used instead of "os.path.exists" 
# import date
# from abc import ABCMeta, abstractmethod, abstractstaticmethod


# --------------------------------------------------------------------


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
    
    @staticmethod
    def set_last_used_ID(last_used_ID: int):
        UniqueIDGenerator._last_ID_used = last_used_ID

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
    
    def get_expense_type_index(self):
        return self._expense_type.value
    
    def set_expense_type(self, expense_type: ExpenseType):
        self._expense_type = expense_type

    def get_date_of_expense(self):
        return self._date_of_expense
    
    def set_date_of_expense(self, date_of_expense: date):
        self._date_of_expense = date_of_expense
    
    def get_info(self) -> str:
        s = ""
        s += "Expense ID: " + str(self._ID) + "\n"
        s += "Name: " + str(self._name) + "\n"
        s += "Amount: $" + str(self.get_amount_in_decimal()) + "\n"
        s += "Expense Type: " + str(self.get_expense_type()) + "\n"
        s += "Date of Expense: " + str(self.get_date_of_expense())
        return s

class ReoccurringExpense:

    def __init__(self, ID: int, name: str, amount: int, expense_type: ExpenseType, frequency: int, start_date: date, end_date: date, expense_list = None):
        self._ID: int = ID
        self._name: str = name
        self._amount: int = amount
        self._expense_type: ExpenseType = expense_type
        self._frequency: int = frequency
        self._start_date: date = start_date
        self._end_date: date = end_date
        self._expense_list: List[Expense] = []

        if expense_list == None:
            self._current_date: date = self._start_date
            while self._current_date <= self._end_date:
                n = Expense(UniqueIDGenerator.generate_ID(), self._name, self._amount, self._expense_type, self._current_date)
                self._expense_list.append(n)
                self._current_date += timedelta(days = self._frequency)
        else:
            self._expense_list: List[Expense] = expense_list

 
    # No ID setter required as ID should remain constant after object creation
    def get_ID(self):
        return self._ID
    
    def get_name(self):
        return self._name
    
    def set_name(self, name: str):
        self._name: str = name

    def get_amount_in_cents(self):
        return self._amount
    
    def set_amount_in_cents(self, amount: int):
        self._amount = amount

    def get_amount_in_decimal(self):
        x: float = float(self._amount / 100)
        return x
    
    def get_expense_type(self):
        return self._expense_type
    
    def get_expense_type_index(self):
        return self._expense_type.value
    
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
        s += "Amount: " + str(self.get_amount_in_decimal()) + "\n"
        s += "Frequency: " + str(self.get_frequency()) + "\n"
        s += "Start Date: " + str(self.get_start_date()) + "\n"
        s += "End Date: " + str(self.get_end_date()) + "\n"
        s += "-----  Expenses -----" + "\n"
        for expense in self._expense_list:
            s += expense.get_info() + "\n"
            s += " - - - - - - - - - - -" + "\n"

        return s
            
class CurrrentExpenseLists:
    current_expense_list: List[Expense]
    current_reoccuring_expense_list: List[ReoccurringExpense]

    @staticmethod
    def set_current_expense_list(expense_list_input: List[Expense]):
        CurrrentExpenseLists.current_expense_list = expense_list_input

    @staticmethod
    def get_current_expense_list() -> List[Expense]:
        return CurrrentExpenseLists.current_expense_list
    
    @staticmethod
    def set_current_reoccurrring_expense_list(reoccurring_epense_list_input: List[ReoccurringExpense]):
        CurrrentExpenseLists.current_reoccuring_expense_list = reoccurring_epense_list_input

    @staticmethod
    def get_current_reoccurring_expense_list() -> List[ReoccurringExpense]:
        return CurrrentExpenseLists.current_reoccuring_expense_list

    ####################################### ##### #### #### ## ### #######################################
    ####################################### # # # ### # ### ## # # #######################################
    ####################################### ## ## ## ### ## ## ### #######################################

def main():
    expense_list: List[Expense]
    reoccurring_expense_list: List[ReoccurringExpense]
    # Check if save file exists and load it into the program is if does
    if save_file_exists() == True:
        last_used_ID: int = int(load_last_used_ID())
        UniqueIDGenerator.set_last_used_ID(last_used_ID)
        expense_list = load_expense_data()
        reoccurring_expense_list = load_reoccurring_expense_data()
    else:
        UniqueIDGenerator.set_last_used_ID(0)
        expense_list = []
        reoccurring_expense_list = []
        create_save_file()

    # Load CurrentExpenseLists static class with expense lists
    # Not sure if this a good way to go about it but the static CurrentExpenseList class will hold the currently used expense lists and can be called easily by other functions
    CurrrentExpenseLists.set_current_expense_list(expense_list)
    CurrrentExpenseLists.set_current_reoccurrring_expense_list(reoccurring_expense_list)

    create_dict_from_reoccurring_expense_obj(reoccurring_expense_list[0])


    ####################################### ##### #### #### ## ### #######################################
    ####################################### # # # ### # ### ## # # #######################################
    ####################################### ## ## ## ### ## ## ### #######################################

def testing():
    print("\n" + "------------------------- TESTING -------------------------" + "\n")
    UniqueIDGenerator(0)

    reoccurring_expenses = load_reoccurring_expense_data()
    print(reoccurring_expenses[0].get_info())

    v = testing_generate_reoccurring_expense()
    print(v.get_info())

def testing_generate_expense() -> Expense:
    n = Expense(UniqueIDGenerator.generate_ID(), "Electricity Bill", 14508, ExpenseType(1), date(2022, 12, 10))
    return n

def testing_generate_reoccurring_expense() -> ReoccurringExpense:
    m = ReoccurringExpense(UniqueIDGenerator.generate_ID(), "Hamburger Payments", 1500, ExpenseType(3), 3, date(2025,9,9), date(2025, 11, 11))
    return m
    
def create_dict_from_expense_obj(expense_obj_input: Expense) -> dict[str, Union[int, str]]:
    output_dict: dict[str, Union[int, str]] = {}
    output_dict["id"] = int(expense_obj_input.get_ID())
    output_dict["name"] = str(expense_obj_input.get_name())
    output_dict["amount"] = int(expense_obj_input.get_amount_in_cents())   
    output_dict["expense_type"] = int(expense_obj_input.get_expense_type_index())
    date_string: str = create_string_from_date(expense_obj_input.get_date_of_expense())
    output_dict["date_of_expense"] = date_string
    return output_dict

def create_dict_from_reoccurring_expense_obj(reoccurring_expense_input: ReoccurringExpense) -> dict[str, Union[int, str, List[dict[str, Union[int, str]]]]]:
    output_dict: dict[str, Union[int, str, List[dict[str, Union[int, str]]]]] = {}
    output_dict["id"] = int(reoccurring_expense_input.get_ID())
    output_dict["name"] = str(reoccurring_expense_input.get_name())
    output_dict["amount"] = int(reoccurring_expense_input.get_amount_in_cents())
    output_dict["expense_type"] = int(reoccurring_expense_input.get_expense_type_index())
    start_date_string = create_string_from_date(reoccurring_expense_input.get_start_date())
    output_dict["start_date"] = start_date_string
    end_date_string = create_string_from_date(reoccurring_expense_input.get_end_date())
    output_dict["end_date"] = end_date_string

    expense_list: List[dict[str, Union[int, str]]] = []
    for expense in reoccurring_expense_input.get_expense_list():
        expense_dict: dict[str, Union[int, str]] = create_dict_from_expense_obj(expense)
        print(expense_dict)
        expense_list.append(expense_dict)

    output_dict["expense_list"] = expense_list

    return output_dict


def create_string_from_date(date_input: date) -> str:
    year = date_input.year
    month = date_input.month
    day = date_input.day
    s = str(year) + str(month) + str(day)
    return s


def create_expense_obj_from_dict(expense_input: dict[str, Union[int, str]]) -> Expense:
    id: int = int(expense_input["id"])
    name: str = str(expense_input["name"])
    amount: int = int(expense_input["amount"])

    t = expense_input["expense_type"]
    expense_type: ExpenseType = ExpenseType(t)

    s: str = str(expense_input["date_of_expense"])
    year: int = int(s[0:4])
    month: int = int(s[4:6])
    day: int = int(s[6:8])
    date_of_expense: date = date(year, month, day)

    expense: Expense = Expense(id, name, amount, expense_type, date_of_expense)
    return expense

def load_last_used_ID() -> int:
    path = os.getcwd() + r"\Expense Data.json"
    with open(path) as f:
        expense_data = json.load(f)
    
    last_used_ID = expense_data["LastUsedID"]
    return last_used_ID

# UniqueIDGenerator needs to be set up when load files functions are combined
def load_expense_data() -> List[Expense]:
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


def load_reoccurring_expense_data() -> List[ReoccurringExpense]:
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

def save_expense_to_file(Expense) -> bool:
    return True



    
# Fuck python and this shitty conditional statement having to exist at the very end of the code for anythin above it run 
if __name__ == "__main__":
    main()

import os
import pickle
import datetime
import matplotlib.pyplot as plt

cache_dir = "./cache"

def set_cache_dir(new_cache_dir):
    global cache_dir
    cache_dir = new_cache_dir

def cache_object(obj, cache_dir=cache_dir):
    with open(f"{cache_dir}/{obj.name}.pkl", "wb") as f:
                pickle.dump(obj, f)


def to_datetime(date='1999-02-11'):
    return datetime.datetime.strptime(date, '%Y-%m-%d')

def to_datestring(date=datetime.datetime.now()):
    return date.strftime('%Y-%m-%d')

today_datetime = datetime.datetime.now()
today_datestring = to_datestring(today_datetime)

FinancialObjects = {}


class FinancialObject:
    def __init__(self, _name, _type, _value, _date_acquired):
        self.name = _name
        self.type = _type
        self.value = _value
        self.date_acquired = _date_acquired
        self.date_updated = datetime.datetime.now()
        FinancialObjects[self.name] = self

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Value: {self.value}, Date Acquired: {self.date_acquired.strftime('%Y-%m-%d')}, Date Updated: {self.date_updated.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return f"FinancialObject(name={self.name}, type={self.type}, value={self.value}, date_acquired={self.date_acquired.strftime('%Y-%m-%d')}, date_updated={self.date_updated.strftime('%Y-%m-%d')})"

    def time_since_acquired(self):
        return datetime.datetime.now() - self.date_acquired

    def time_since_updated(self):
        return datetime.datetime.now() - self.date_updated

    def update_value(self, new_value):
        self.value = new_value
        self.date_updated = datetime.datetime.now()


Employers = {}


class Employer:
    def __init__(self, name, bonus_rate, raise_rate):
        self.name = name
        self.bonus_rate = bonus_rate
        self.raise_rate = raise_rate
        self.date_updated = datetime.datetime.now()
        Employers[self.name] = self

    def __str__(self):
        return f"Name: {self.name}, Type: Employer, Bonus Rate: {self.bonus_rate}, Raise Rate: {self.raise_rate}"

    def __repr__(self):
        return f"Employer(name={self.name}, bonus_rate={self.bonus_rate}, raise_rate={self.raise_rate})"

    def time_since_updated(self):
        return datetime.datetime.now() - self.date_updated


Jobs = {}


class Job(FinancialObject):
    def __init__(self, name, value, date_acquired, employer):
        super().__init__(name, "Job", value, date_acquired)
        self.salary = value
        self.bonus = value * employer.bonus_rate
        self.salary_prediction = value * (1 + employer.raise_rate) 
        self.employer = employer
        Jobs[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Salary: {self.salary}, Salary Prediction: {self.salary_prediction}, Bonus: {self.bonus}"

    def __repr__(self):
        return f"Job({super().__repr__()}, value={self.salary})"


Assets = {}


class Asset(FinancialObject):
    def __init__(self, name, value, date_acquired, depreciation_rate):
        super().__init__(name, "Asset", value, date_acquired)
        self.depreciation_rate = depreciation_rate
        Assets[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Depreciation Rate: {self.depreciation_rate}"

    def __repr__(self):
        return f"Asset({super().__repr__()}, depreciation_rate={self.depreciation_rate})"
    
    def __predict_next_month(self, value=-1, depreciation_rate=-1):
        if value == -1:
            value = self.value
        if depreciation_rate == -1:
            depreciation_rate = self.depreciation_rate
        return value * (1 - (depreciation_rate / 12))
    
    def predict(self, years):
        base_value = self.value
        base_date = today_datestring
        self.predictions = {}
        self.predictions[base_date] = base_value
        for _ in range(years * 12):
            base_value = self.__predict_next_month(base_value)
            base_date = to_datestring(to_datetime(base_date) + datetime.timedelta(days=365/12))
            self.predictions[base_date] = base_value
        return self.predictions


Brokers = {}


class Broker:
    def __init__(self, name):
        self.name = name
        self.date_updated = datetime.datetime.now()
        Brokers[self.name] = self

    def __str__(self):
        return f"Name: {self.name}, Type: Broker"

    def __repr__(self):
        return f"Broker(name={self.name})"

    def time_since_updated(self):
        return datetime.datetime.now() - self.date_updated


Accounts = {}


class Account(FinancialObject):
    def __init__(
        self,
        name,
        value,
        date_acquired,
        broker,
        account_type,
        return_rate,
    ):
        super().__init__(name, "Account", value, date_acquired)
        self.broker = broker
        self.account_type = account_type
        self.return_rate = return_rate
        Accounts[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Broker: {self.broker}, Return Rate: {self.return_rate}"

    def __repr__(self):
        return f"Account({super().__repr__()}, broker={self.broker}, return_rate={self.return_rate})"


Expenditures = {}


class Expenditure(FinancialObject):
    def __init__(
        self,
        name,
        value,
        date_acquired,
        category,
        recurring=False,
    ):
        super().__init__(
            name, "Expenditure", value, date_acquired
        )
        self.category = category
        self.recurring = recurring
        Expenditures[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Expenditure Category: {self.category}, Recurring: {self.recurring}"

    def __repr__(self):
        return f"Expenditure({super().__repr__()}, category={self.category}, recurring={self.recurring})"

def cache_project(cache_dir=cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    for financial_object in FinancialObjects.values():
        cache_object(financial_object)

    for employer in Employers.values():
        cache_object(employer)

    for broker in Brokers.values():
        cache_object(broker)

def load_cached_project(cache_dir=cache_dir):
    if not os.path.exists(cache_dir):
        return

    for filename in os.listdir(cache_dir):
        with open(f"{cache_dir}/{filename}", "rb") as f:
            obj = pickle.load(f)
            if isinstance(obj, FinancialObject):
                FinancialObjects[obj.name] = obj
            elif isinstance(obj, Employer):
                Employers[obj.name] = obj
            elif isinstance(obj, Broker):
                Brokers[obj.name] = obj
            else:
                # Handle other types of objects if needed
                pass
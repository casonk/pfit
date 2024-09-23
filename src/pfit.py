import os
import pickle
import shutil
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
    def __init__(
            self, 
            _name, 
            _type, 
            _value, 
            _date_acquired, 
            _date_terminated=None, 
            _depreciation_rate=0.05, 
            _recurring=False
            ):
        self.name = _name
        self.type = _type
        self.value = _value
        self.depreciation_rate = _depreciation_rate
        self.recurring = _recurring
        self.date_acquired = _date_acquired
        self.date_terminated = _date_terminated
        self.date_updated = datetime.datetime.now()
        self.is_terminated()
        self.time_to_termination()
        self.time_since_termination()
        FinancialObjects[self.name] = self

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Value: {self.value}, Depreciation Rate: {self.depreciation_rate}, Recurring: {self.recurring}, Date Acquired: {self.date_acquired.strftime('%Y-%m-%d')}, Date Updated: {self.date_updated.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return f"FinancialObject(name={self.name}, type={self.type}, value={self.value}, depreciation_rate={self.depreciation_rate}, recurring={self.recurring}, date_acquired={self.date_acquired.strftime('%Y-%m-%d')}, date_updated={self.date_updated.strftime('%Y-%m-%d')})"

    def __predict_next_month(self, value=-1, depreciation_rate=-1):
        if value == -1:
            value = self.value
        if depreciation_rate == -1:
            depreciation_rate = self.depreciation_rate
        predicted_value = value * (1 - (depreciation_rate / 12))
        if isinstance(self, Account) and (len(self.flows) != 0):
            for flow in self.flows:
                if flow.recurring:
                    if self == flow.source_account:
                        predicted_value -= flow.value
                    elif self == flow.sink_account:
                        predicted_value += flow.value
        return predicted_value

    
    def predict(self, years):
        _base_value = self.value
        _base_date = today_datestring
        self.predictions = {}
        self.predictions[_base_date] = _base_value
        self.is_terminated()
        self.time_to_termination()
        for month in range(years * 12):
            time_delta = datetime.timedelta(days=((month+1)*(365/12)))
            base_date = to_datestring(to_datetime(_base_date) + time_delta)
            if  (self._is_terminated == True):
                self.predictions[base_date] = 0
            elif (self._time_to_termination != None) and (time_delta > self._time_to_termination):
                self.predictions[base_date] = 0
            else:
                base_value = self.__predict_next_month(_base_value)
                self.predictions[base_date] = base_value
                _base_value = base_value
        return self.predictions
    
    def is_terminated(self):
        if self.date_terminated == None:
            self._is_terminated = None
        elif datetime.datetime.now() > self.date_terminated:
            self._is_terminated = False
        else:
            self._is_terminated = True
        return self._is_terminated
    
    def time_to_termination(self):
        if self.date_terminated == None:
            self._time_to_termination = None
        else:
            self._time_to_termination = self.date_terminated - datetime.datetime.now()
        return self._time_to_termination
    
    def time_since_termination(self):
        if self.date_terminated == None:
            self._time_since_termination = None
        else:
            self._time_since_termination = datetime.datetime.now() - self.date_terminated
        return self._time_since_termination
    
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
    def __init__(
            self, 
            name, 
            value, 
            date_acquired, 
            employer, 
            date_terminated=None, 
            depreciation_rate=0.00, 
            recurring=False
            ):
        super().__init__(
            _name=name, 
            _type="Job", 
            _value=value, 
            _date_acquired=date_acquired, 
            _date_terminated=date_terminated,
            _depreciation_rate=depreciation_rate, 
            _recurring=recurring
            )
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
    def __init__(
            self, 
            name, 
            value, 
            date_acquired, 
            date_terminated=None, 
            depreciation_rate=0.025, 
            recurring=False
            ):
        super().__init__(
            _name=name, 
            _type="Asset", 
            _value=value, 
            _date_acquired=date_acquired, 
            _date_terminated=date_terminated,
            _depreciation_rate=depreciation_rate, 
            _recurring=recurring
            )
        Assets[self.name] = self

    def __str__(self):
        return f"{super().__str__()}"

    def __repr__(self):
        return f"Asset({super().__repr__()})"


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
        date_terminated=None, 
        depreciation_rate=0.00,
        recurring=False,
        flows=[],
    ):
        super().__init__(
            _name=name, 
            _type="Account", 
            _value=value, 
            _date_acquired=date_acquired, 
            _date_terminated=date_terminated,
            _depreciation_rate=depreciation_rate, 
            _recurring=recurring
            )
        self.broker = broker
        self.account_type = account_type
        self.return_rate = return_rate
        self.flows = flows
        Accounts[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Broker: {self.broker}, Return Rate: {self.return_rate}, Flows: {self.flows}"

    def __repr__(self):
        return f"Account({super().__repr__()}, broker={self.broker}, return_rate={self.return_rate}, flows={self.flows})"


Flows = {}


class Flow(FinancialObject):
    def __init__(
        self,
        name,
        value,
        date_acquired, 
        category,
        source_account=None,
        sink_account=None,
        date_terminated=None, 
        depreciation_rate=0.00,
        recurring=False,
    ):
        super().__init__(
            _name=name, 
            _type="Flow", 
            _value=value, 
            _date_acquired=date_acquired, 
            _date_terminated=date_terminated,
            _depreciation_rate=depreciation_rate, 
            _recurring=recurring
        )
        self.category = category
        self.source_account = source_account
        self.sink_account = sink_account
        if source_account != None:
            if len(source_account.flows) != 0:
                source_account.flows = source_account.flows + [self]
            else:
                source_account.flows = [self]
        if sink_account != None:
            if len(sink_account.flows) != 0:
                sink_account.flows = sink_account.flows + [self]
            else:
                sink_account.flows = [self]
        Flows[self.name] = self

    def __str__(self):
        return f"{super().__str__()}, Flow Category: {self.category}"

    def __repr__(self):
        return f"Flow({super().__repr__()}, category={self.category})"

def clear_project(cache_dir=cache_dir):
    shutil.rmtree(cache_dir)

def cache_project(cache_dir=cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    for financial_object in FinancialObjects.values():
        cache_object(financial_object)

    for employer in Employers.values():
        cache_object(employer)

    for broker in Brokers.values():
        cache_object(broker)

def load_project(cache_dir=cache_dir):
    if not os.path.exists(cache_dir):
        return

    for filename in os.listdir(cache_dir):
        with open(f"{cache_dir}/{filename}", "rb") as f:
            obj = pickle.load(f)
            if isinstance(obj, FinancialObject):
                FinancialObjects[obj.name] = obj
                if isinstance(obj, Job):
                    Jobs[obj.name] = obj
                elif isinstance(obj, Asset):
                    Assets[obj.name] = obj
                elif isinstance(obj, Account):
                    Accounts[obj.name] = obj
                elif isinstance(obj, Flow):
                    Flows[obj.name] = obj
            elif isinstance(obj, Employer):
                Employers[obj.name] = obj
            elif isinstance(obj, Broker):
                Brokers[obj.name] = obj
            else:
                # Handle other types of objects if needed
                pass
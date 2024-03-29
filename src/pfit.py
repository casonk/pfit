import datetime


class FinancialObject:
    def __init__(self, _name, _type, _value, _date_acquired):
        self.name = _name
        self.type = _type
        self.value = _value
        self.date_acquired = _date_acquired
        self.date_updated = datetime.datetime.now()

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Value: {self.value}, Date Acquired: {self.date_acquired}, Date Updated: {self.date_updated}"

    def __repr__(self):
        return f"FinancialObject({self.name}, {self.type}, {self.value}, {self.date_acquired}, {self.date_updated})"
    
    def time_since_acquired(self):
        return datetime.datetime.now() - self.date_acquired
    
    def time_since_updated(self):
        return datetime.datetime.now() - self.date_updated

    def update_value(self, new_value):
        self.value = new_value
        self.date_updated = datetime.datetime.now()

class Employer:
    def __init__(self, employer_name, bonus_rate, raise_rate):
        self.employer_name = employer_name
        self.bonus_rate = bonus_rate
        self.raise_rate = raise_rate
        self.date_updated = datetime.datetime.now()

    def __str__(self):
        return f"Name: {self.employer_name}, Type: Employer, Bonus Rate: {self.bonus_rate}, Raise Rate: {self.raise_rate}"

    def __repr__(self):
        return f"Employer({self.employer_name}, {self.bonus_rate})"

    def time_since_updated(self):
        return datetime.datetime.now() - self.date_updated

class Job(FinancialObject):
    def __init__(self, job_title, salary, date_acquired, employer):
        super().__init__(job_title, "Job", salary, date_acquired)
        self.salary = salary
        self.bonus = salary * employer.bonus_rate
        self.employer = employer

    def __str__(self):
        return f"{super().__str__()}, Salary: {self.salary}, Bonus: {self.bonus}"

    def __repr__(self):
        return f"Job({super().__repr__()}, {self.salary})"


class Asset(FinancialObject):
    def __init__(self, name, value, date_acquired, depreciation_rate):
        super().__init__(name, "Asset", value, date_acquired)
        self.depreciation_rate = depreciation_rate

    def __str__(self):
        return f"{super().__str__()}, Depreciation Rate: {self.depreciation_rate}"

    def __repr__(self):
        return f"Asset({super().__repr__()}, {self.depreciation_rate})"


class Account(FinancialObject):
    def __init__(self, name, value, date_acquired, interest_rate):
        super().__init__(name, "Account", value, date_acquired)
        self.interest_rate = interest_rate

    def __str__(self):
        return f"{super().__str__()}, Interest Rate: {self.interest_rate}"

    def __repr__(self):
        return f"Account({super().__repr__()}, {self.interest_rate})"


class Expenditure(FinancialObject):
    def __init__(self, name, value, date_acquired, category):
        super().__init__(name, "Expenditure", value, date_acquired)
        self.category = category

    def __str__(self):
        return f"{super().__str__()}, Category: {self.category}"

    def __repr__(self):
        return f"Expenditure({super().__repr__()}, {self.category})"

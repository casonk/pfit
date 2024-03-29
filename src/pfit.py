# Evolution of Personal Finance
class BasePersonalFinance:
    def __init__(self, income, savings, spending):
        self.income = income
        self.savings = savings
        self.spending = spending

    def calculate_net_income(self):
        return self.salary - self.spending

    def calculate_savings_rate(self):
        return (self.savings / self.salary) * 100

class SuperPersonalFinance(BasePersonalFinance):
    # def __init__(self, salary, bonus, cash, checking_account, savings_account, expected_raise, debt, debt_interest_rate):
    def __init__(self, salary, bonus, cash, checking_account, savings_account, travel_spend, shelter_spend, food_spend, other_spend):
        self.salary = salary
        self.bonus = bonus
        self.cash = cash
        self.checking_account = checking_account
        self.savings_account = savings_account
        self.travel_spend = travel_spend
        self.shelter_spend = shelter_spend
        self.food_spend = food_spend
        self.other_spend = other_spend
        # self.expected_raise = expected_raise
        # self.debt = debt
        # self.debt_interest_rate = debt_interest_rate

        income = salary + bonus
        savings = cash + checking_account + savings_account
        spending = travel_spend + shelter_spend + food_spend + other_spend
        # spending = grocery_spend + rent + utilities + dining_out + shopping + travel + entertainment + other
        super().__init__(income, savings, spending)

    # def calculate_net_income(self):
    #     net_income = super().calculate_net_income()
    #     return net_income + self.expected_raise

    # def calculate_debt_payment(self):
    #     return self.debt * self.debt_interest_rate
    
# Evolution of Economic Finance
class BaseEconomicFinance:
    def __init__(self, interest_rate, inflation_rate, mortgage_rate):
        self.interest_rate = interest_rate
        self.inflation_rate = inflation_rate
        self.mortgage_rate = mortgage_rate

    def calculate_real_interest_rate(self):
        return self.interest_rate - self.inflation_rate

    def calculate_mortgage_payment(self, loan_amount, loan_term):
        monthly_interest_rate = self.mortgage_rate / 12
        num_payments = loan_term * 12
        return (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)

class SuperEconomicFinance(BaseEconomicFinance):
    def __init__(self, interest_rate, inflation_rate, mortgage_rate, bond_rate, market_rate):
        super().__init__(interest_rate, inflation_rate, mortgage_rate)
        self.bond_rate = bond_rate
        self.market_rate = market_rate

    def calculate_real_interest_rate(self):
        real_interest_rate = super().calculate_real_interest_rate()
        return real_interest_rate + self.bond_rate

    def calculate_market_value(self, investment):
        return investment * self.market_rate
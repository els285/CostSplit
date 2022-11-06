class Person:
    '''
    The Person class defines each individual, in terms of their individual transactions: 
        those payments they made and those they participates in.
    The Person class underlies the calculations, with the Transaction class existing to assign payments and participation to Persons
    The Trip class combines many Transactions, and initiates the overall splitwise calculation 
    '''

    def __init__(self,name,**kwargs):
        self.name           = name
        self.net            = 0
        self.total_paid     = 0
        self.total_due      = 0
        self.payments       = {}
        self.expenses       = {}

        self.running_net  = 0
        self.paid_by        = {} # A dictionary containg the name and amount 
        self.paid_to        = {} # A dictionary containg the name and amount 

        self.account_number = kwargs["account_number"] if "account_number" in kwargs else None
        self.sort_code      = kwargs["sort_code"]      if "sort_code"      in kwargs else None

    @staticmethod
    def compute_total(d):
        ''' Compute the sum of all values in a dictionary'''
        return sum(list(d.values()))

    def add_payment(self,transaction,amount):
        self.payments[transaction] = amount

    def add_expense(self,transaction,amount):
        self.expenses[transaction] = amount

    def self_total(self):
        self.total_paid  = self.compute_total(self.payments)
        self.total_due   = self.compute_total(self.expenses)
        self.net         = self.total_paid - self.total_due
        self.running_net = self.net


    # def add_payment(self,new_payment): # This should be a dictionary with name of payment and amount
    #     # self.payments = combine_dictionaries([self.payments,new_payment])
    #     self.payments = {**self.payments , **new_payment}
    #     self.net_paid = sum(self.payments.values())
    #     self.net = self.net_paid - self.net_due

    # def add_expense(self,new_expense): # This should be a dictionary with name of expense and amount
    #     # self.expenses = combine_dictionaries([self.expenses,new_expense])
    #     self.expenses = {**self.expenses , **new_expense}
    #     self.net_due  = sum(self.expenses.values())
    #     self.net = self.net_paid - self.net_due


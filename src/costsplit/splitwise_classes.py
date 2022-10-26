## Classes
import networkx as nx
import matplotlib.pyplot as plt
# from nwf import nxgraph_plotly
# from splitwise_classes import Person,Transaction,Trip


from splitwise_functions import *

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
        self.net_paid       = 0
        self.net_due        = 0
        self.payments       = {}
        self.expenses       = {}

        self.splitwise_net  = 0
        self.paid_by        = {} # A dictionary containg the name and amount 
        self.paid_to        = {} # A dictionary containg the name and amount 

        if "account_number" in kwargs: self.account_number     = kwargs["account_number"]     
        else: self.account_number =  None
        if "sort_code"        in kwargs: self.sort_code        = kwargs["sort_code"]     
        else: self.sort_code = None

    # def set_net(self,additional_amount):
    #     self.net = self.net + additional_amount

    def add_payment(self,new_payment): # This should be a dictionary with name of payment and amount
        self.payments = combine_dictionaries([self.payments,new_payment])
        self.net_paid = sum(self.payments.values())
        self.net = self.net_paid - self.net_due

    def add_expense(self,new_expense): # This should be a dictionary with name of expense and amount
        self.expenses = combine_dictionaries([self.expenses,new_expense])
        self.net_due  = sum(self.expenses.values())
        self.net = self.net_paid - self.net_due


###########################################################################################################################

class Pre_Payment:

    '''
    Pre-payments may have been made which must be taken into account.
    '''
    def __init__(self,giver,recipient,amount):

        self.giver      = giver
        self.recipient  = recipient
        self.amount     = amount

        recipient.net += -self.amount 
        giver.net += self.amount
        recipient.paid_by[giver] = amount
        giver.paid_to[giver] = amount




class Transaction:

    '''
    The Transaction class defines any one payment, in terms of those who paid and those who pariticipated in the transaction.
    They main point of the Transaction class is assigning payments and participation to Person through the assign_to_persons funciton.
    There is also a perTransaction_compute function which does an individual splitwise calculation 
    '''

    def assign_to_persons(self):
        '''
        This loops over the individuals in payers (those who contributed to payment) and those would pariticpate in Transaction
        For each, it adds this to their totals
        '''

        for individual in self.payers:
            individual.add_payment({self  :  self.payers[individual]})

        for individual in self.individual_amounts:
            individual.add_expense({self  :  self.individual_amounts[individual]})


    # def add_prepayment(self):
    #     '''
    #     Do this before calling assign_to_persons?
    #     '''
    #     for person in self.pre_contributed:




    def perTransaction_compute(self):
        '''
        Does a splitwise calculation for this transaction only
        Creates local copies of the Persons involved
        Applies the splitwise calculation to them
        '''
        indiv_copies = []
        for person in self.involved:

            inner_person = Person(person.name)
            if person in self.payers:
                inner_person.add_payment({self: self.payers[person]})

            if person in self.individual_amounts:
                inner_person.add_expense({self:self.individual_amounts[person]})

            indiv_copies.append(inner_person)

        # Does the splitwise computation
        compute(indiv_copies)


    def Generate_Participation_Graph(self):
        '''
        The participation graph is an undirected networkx graph which simply thinks all Persons to the Transaction
        '''
        G = nx.Graph()
        for person in self.involved:
            G.add_edge(person,self.Transaction)
        self.participation_network = G

        # nxgraph_plotly(G)
        nx.draw_networkx(G)

        # plt.show()
        # input()


    ################################################################################################

    def __init__(self,Transaction,**kwargs):
        self.Transaction    = Transaction
        self.payers         = {}
        self.participants   = {}
        self.involved       = []
        self.pre_contributed = {}
        # self.type

        if "type" in kwargs: self.type = kwargs["type"] # Use this type part
        if "date" in kwargs: self.date = kwargs["date"]

        if "payers"         in kwargs: 
            self.payers= kwargs["payers"] 
            self.amount_paid = total(self.payers) # This generates the total amount spent of all the payers

        # if self.type == "weighted":

        if "participants"     in kwargs: 
            self.participants     = kwargs["participants"] 
            self.individual_amounts = update_dues(self.participants,self.amount_paid)



        # if "pre_contributed" in kwargs:
        #     self.pre_contributed = kwargs["pre_contributed"]
        #     self.individual_amounts


        self.involved = list(self.payers) + list(set(list(self.participants)) - set(list(self.payers)))

        # Generates network graphs of the transaction
        # self.Generate_Transaction_Graph()
        self.Generate_Participation_Graph()

        # Assign the costs to individuals
        self.assign_to_persons()



        # Do a local splitwise calculation
        if "doPerTransactionSplitwise" in kwargs:
            doPerTransactionSplitwise = kwargs["doPerTransactionSplitwise"]
        else: doPerTransactionSplitwise = False
        if doPerTransactionSplitwise:
            self.perTransaction_compute()


    ##### Just now, the way the dictionaries are combined means that when these edit functions are called, the totals are added, no wiped
    '''
    Not sure about the functionality of all this at the moment - February 4th 2021
    '''

    def edit_payers(self,additional_payers):
        self.payers = combine_dictionaries([self.payers,additional_payers])    # Add functionality to remvoe a player?
        self.amount_paid = total(self.payers)


        # Here we would need to update the amounts people are due
        self.individual_amounts = update_dues(self.participants,self.amount_paid)

    def edit_participants(self,additional_participants):
        # self.participants = {**self.particpants,**additional_participants}
        self.participants = combine_dictionaries([self.participants,additional_participants])

        self.individual_amounts = update_dues(self.participants,self.amount_paid)

    def reinput_payers(self,payers):
        self.payers = payers
        total_paid = total(payers)
        self.amount_paid = total_paid

        self.individual_amounts = update_dues(self.participants,self.amount_paid)


    def reinput_participants(self,participants):
        self.participants = participants
        total_paid = total(self.payers)

        self.amount_paid = total_paid
        self.individual_amounts = update_dues(self.participants,self.amount_paid)


##############################################################################################################################


class Trip:
    def __init__(self,trip_name, **kwargs):
        self.trip_name         = trip_name
        self.transactions = {}
        self.attendees = {}
        self.prepayments = []

        if "list_of_transactions" in kwargs:
            for trans in kwargs["list_of_transactions"]:
                self.transactions[trans.Transaction] = trans


        if "list_of_attendess" in kwargs: self.attendees = kwargs["list_of_attendess"]

    def add_transaction(self,new_transaction):
        self.transactions[new_transaction.Transaction]=new_transaction


    def add_attendee(self,new_attendee):
        self.attendees.update({new_attendee.name : new_attendee})

    def doOverallCalculation(self):
        self.credit_list,self.debt_list,self.splitwise_transactions,self.overall_transaction_graph = compute(self.attendees.values())

    def add_prepayment(self,prepayment):
        self.prepayments.append(prepayment)



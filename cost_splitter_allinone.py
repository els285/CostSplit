################# COSTSPLITTER #######################
'''
Ethan L Simpson
February 6th 2021

Script for carrying out a "splitwise" calculation, where a simple list of exchanges between individuals is computed from a more complex list of transactions.
Computes the "most efficient" way in which money should be exchanged
Saves money going back and forward

Additionally generates graphs which illustrate this process

Will eventually be adapted to a Web app (Flask?)

Will also include interactive graph plots

'''

#### Plots to make:
import networkx as nx
import matplotlib.pyplot as plt

doPerTransactionSplitwise = True


def combine_dictionaries(list_of_dics):
    final_dic = {}
    for dic in list_of_dics:
        for key in dic:
            if key not in final_dic:    final_dic[key] = dic[key]
            elif key in final_dic:        final_dic[key] += dic[key]

    return final_dic

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


def total(dict_num):
    return sum(dict_num.values())


def list2values(list_of_participants,sub_total,individual_amounts):
    individual_amount_value = sub_total/len(list_of_participants)
    for indiv in list_of_participants: individual_amounts[indiv] = (individual_amount_value)
    return individual_amounts

def update_dues(participants,amount_paid):
    individual_amounts = {}


    if          isinstance(participants,str):        individual_amounts = {participants:amount_paid}
    elif      isinstance    (participants,list ):        individual_amounts=list2values(participants,amount_paid,individual_amounts)
    elif isinstance    (participants,tuple):        individual_amounts=list2values(list(participants),amount_paid,individual_amounts)
    elif isinstance    (participants,dict ):
        for sub_party in participants.keys():
            if   isinstance(sub_party,list ):    list2values(sub_party,participants[sub_party],individual_amounts)
            elif isinstance(sub_party,tuple):    list2values(list(sub_party),participants[sub_party],individual_amounts)
            elif isinstance(sub_party,str  ):     individual_amounts[sub_party] = participants[sub_party]
        if total(individual_amounts) != amount_paid: print("WARNING. Amount paid does not match participants' individual costs!")

    return individual_amounts


#########################################################################################


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
            individual.add_expense({self:self.individual_amounts[individual]})

    def perTransaction_compute(self):
        '''
        Does a splitwise calculation for this transaction only
        Creates local copies of the Persons involved
        Applies the splitwise calculation to them
        '''
        indiv_copies = []
        for person in self.involved:

            inner_person = Person(self.Transaction + person.name)
            if person in self.payers:
                inner_person.add_payment({self: self.payers[person]})

            if person in self.individual_amounts:
                print("yess")
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
        nx.draw_networkx(G)

        plt.show()
        input()


    ################################################################################################

    def __init__(self,Transaction,**kwargs):
        self.Transaction    = Transaction
        self.payers         = {}
        self.participants   = {}
        self.involved       = []

        if "type" in kwargs: self.type = kwargs["type"]
        if "date" in kwargs: self.date = kwargs["date"]

        if "payers"         in kwargs: 
            self.payers= kwargs["payers"] 
            total_paid = total(self.payers) # This generates the total amount spent of all the payers
            self.amount_paid = total_paid

        if "participants"     in kwargs: 
            self.participants     = kwargs["participants"] 
            self.individual_amounts = update_dues(self.participants,self.amount_paid)

        self.involved = list(self.payers) + list(set(list(self.participants)) - set(list(self.payers)))

        # Generates network graphs of the transaction
        # self.Generate_Transaction_Graph()
        self.Generate_Participation_Graph()

        # Assign the costs to individuals
        self.assign_to_persons()

        # Do a local splitwise calculation
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


##########################################################################################################


class Trip:
    def __init__(self,trip_name, **kwargs):
        self.trip_name         = trip_name
        self.transactions = {}
        self.attendees = {}

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


def compute(participant_list):
    '''
    Drives the splitwise computation:
        1. Prints summary
        2. Works out who is in credit and who is in debt
        3. Computes the splitwise transactions
        4. Generates the transaction graph
    '''

    # summary(self.attendees.values(),self.transactions.values())

    credit_list,debt_list=credit_or_debt(participant_list)

    overall_state_of_play(participant_list)

    splitwise_transactions = splitwise_oop(credit_list,debt_list)

    # Generate graph
    overall_transaction_graph = g2(credit_list,debt_list)

    return credit_list,debt_list,splitwise_transactions,overall_transaction_graph

########################################################################################################################

def g2(credit_list,debt_list):
    '''
    Generates a transaction network graph using only the credit and debt list.
    Maybe there is a more secure way to generate this but this is reasonably robust
    '''
    graph = nx.DiGraph()

    for person in credit_list:
        graph.add_node(person,name=person.name)

    for person in debt_list:
        graph.add_node(person,name=person.name)

    for person in credit_list:
        print(person.__dict__)
        for payment in person.payments:
            graph.add_edge(person,payment)
        for debtor in person.paid_by:
            graph.add_edge(debtor,person)

    nx.draw_networkx(graph)


    plt.show()
    input()

    return graph




def summary(party,list_of_transactions):
    '''
    Prints summary
    '''
    for indiv in party:
        print(indiv.name +"'s out-goings:")
        print(indiv.payments)
        print(indiv.name + "'s particpcated expenses:")
        print(indiv.expenses)
        print(indiv.name + " paid a total of:")
        print(indiv.net_paid)
        print(indiv.name + "'s overall share of the expenditure comes to:")
        print(indiv.net_due)
        print("\n")

    # for trans in list_of_transactions:
    #     print(trans.Transaction,trans.individual_amounts)
    # print("\n")
    overall_state_of_play(party)
    # input()



def credit_or_debt(party):
    '''
    Computes each individual's net expenditure to work out whether they are in credit or debt
    '''
    credit_list = []
    debt_list     = []
    for individual in party:
        individual.splitwise_net = individual.net
        if individual.net     > 0: credit_list.append(individual)
        elif individual.net < 0: debt_list.append(individual)
        else: print(individual.name + "'s payments balance their debts exactly!")

    return credit_list, debt_list

def overall_state_of_play(party):
    '''
    Prints who is in credit and who is in debt
    '''
    for indiv in party:
        if indiv.net > 0.00: print(indiv.name + " is due a total of " + str(indiv.net))
        if indiv.net < 0.00: print(indiv.name + " owes a total of " + str(abs(indiv.net)))


def splitwise_oop(credit_list,debt_list):
    transaction_counter = 0
    transaction_dictionary = {}
    for indiv1 in credit_list:
        # print(indiv1,indiv1.name,indiv1.s)

        while indiv1.splitwise_net > 0.00:

            for indiv2 in debt_list:

                if indiv2.splitwise_net != 0.00:

                    difference = (indiv1.splitwise_net + indiv2.splitwise_net)
                    # print(difference)

                    if difference >= 0.00:
                        paid = indiv1.splitwise_net - difference
                        indiv1.splitwise_net = difference
                        indiv2.splitwise_net = 0.00
                        print(indiv2.name + " paid " + indiv1.name + " the amount of " + str(paid) )
                        indiv1.paid_by = combine_dictionaries([indiv1.paid_by,{indiv2:paid}])
                        indiv2.paid_to = combine_dictionaries([indiv2.paid_to,{indiv1:paid}])
                        transaction_dictionary[transaction_counter+1] = {"giver": indiv2,"recipient":indiv1,"amount":paid}
                        transaction_counter +=1
                    else:
                        paid = abs(indiv2.splitwise_net - difference)
                        left = abs(difference)
                        indiv1.splitwise_net = 0.00
                        indiv2.splitwise_net = difference
                        indiv1.paid_by = combine_dictionaries([indiv1.paid_by,{indiv2:paid}])
                        indiv2.paid_to = combine_dictionaries([indiv2.paid_to,{indiv1:paid}])
                        if paid != 0:
                            print(indiv2.name + " pays " + indiv1.name + " " + str(paid) + " but has " + str(left) + " left over")
                            transaction_dictionary[transaction_counter+1] = {"giver": indiv2,"recipient":indiv1,"amount":paid}

                            transaction_counter +=1
                        else: pass
                else: pass


    # print(transaction_dictionary)
    # input()

    return transaction_dictionary

                # Return a dictionary of transactions here
                # This could then be used to plot if necessary



###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################



# #### This information can now be passed to the splitwise function, which should loop over all expenses and calculate everybodies net
Ethan = Person("Ethan",account_number="34778883")
Caroline = Person("Caroline")
Chris  = Person("Chris")

Meal  = Transaction("Te Seba",payers={Caroline:30},participants=(Ethan,Caroline,Chris))
Meal2 = Transaction("Pizza Hut",payers={Ethan:24},participants=(Ethan,Caroline,Chris))



xmasD = Trip("xmasD")        ## The transactions contain the individuals present

xmasD.add_attendee(Ethan)
xmasD.add_attendee(Caroline)
xmasD.add_attendee(Chris)

xmasD.add_transaction(Meal)
xmasD.add_transaction(Meal2)



xmasD.doOverallCalculation()


print(xmasD.__dict__)

exit()



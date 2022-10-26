## Functions

import networkx as nx
import matplotlib.pyplot as plt
from nwf import nxgraph_plotly



def combine_dictionaries(list_of_dics):
    final_dic = {}
    for dic in list_of_dics:
        for key in dic:
            if key not in final_dic:    final_dic[key] = dic[key]
            elif key in final_dic:        final_dic[key] += dic[key]

    return final_dic

def total(dict_num):
    return sum(dict_num.values())


def over_paid(dic_of_over_payers,dic_of_payers):
    pass




def list2values(list_of_participants,sub_total,individual_amounts):
    individual_amount_value = sub_total/len(list_of_participants)
    for indiv in list_of_participants: 
        individual_amounts[indiv] = (individual_amount_value)
        print(individual_amounts)
        input()
    return individual_amounts

def update_dues(participants,amount_paid):
    individual_amounts = {}


    if        isinstance(participants,str  ):   individual_amounts = {participants:amount_paid}
    elif      isinstance(participants,list ):   individual_amounts = list2values(participants,amount_paid,individual_amounts)
    elif      isinstance(participants,tuple):   individual_amounts = list2values(list(participants),amount_paid,individual_amounts)
    
    elif      isinstance(participants,dict ):

        # print(participants)
        # input()

        for sub_party in participants.keys():
            if   isinstance(sub_party,list ):    list2values(sub_party,participants[sub_party],individual_amounts)
            elif isinstance(sub_party,tuple):    list2values(list(sub_party),participants[sub_party],individual_amounts)
            elif isinstance(sub_party,str  ):     individual_amounts[sub_party] = participants[sub_party]
        if total(individual_amounts) != amount_paid: 
            print("WARNING. Amount paid does not match participants' individual costs!")
            print(total(individual_amounts))
            print(amount_paid)

    return individual_amounts


#########################################################################################




##########################################################################################################



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

    print(credit_list)
    print(debt_list)
    input()

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
            graph.add_edge(person,payment,amount=float(person.payments[payment]))
        for debtor in person.paid_by:
            graph.add_edge(debtor,person,amount=float(person.paid_by[debtor]))

    nxgraph_plotly(graph)

    # nx.draw_networkx(graph)


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
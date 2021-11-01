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
from nwf import nxgraph_plotly
from splitwise_classes import Person,Transaction,Trip

doPerTransactionSplitwise = True




                # Return a dictionary of transactions here
                # This could then be used to plot if necessary



###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################



# #### This information can now be passed to the splitwise function, which should loop over all expenses and calculate everybodies net
Ethan = Person("Ethan")
Pat = Person("Pat")
Bruce  = Person("Bruce")
James = Person("James")
Martin = Person("Martin")
Cat = Person("Cat")

# Meal  = Transaction("Te Seba",payers={Caroline:30},participants=(Ethan,Caroline,Chris),doPerTransactionSplitwise=True)
# Meal2 = Transaction("Pizza Hut",payers={Ethan:24},participants=(Ethan,Caroline,Chris),doPerTransactionSplitwise=True)
Round1 = Transaction("Tennents",payers={Ethan:21.30},participants=(Ethan,Pat,Bruce,James,Martin,Cat),doPerTransactionSplitwise=False)
Round2 = Transaction("Tennents2",payers={Martin:20.40},participants=(Ethan,Pat,Bruce,Martin,Cat),doPerTransactionSplitwise=False)
Round3 = Transaction("Guinness",payers={Cat:25},participants=(Ethan,Pat,Bruce,James,Martin,Cat),doPerTransactionSplitwise=False)
Round4 = Transaction("Guiness2",payers={Bruce:25.80},participants=(Ethan,Pat,Bruce,James,Martin,Cat),doPerTransactionSplitwise=False)
Aperol = Transaction("Aperol",payers={Ethan:13},participants=[Cat],doPerTransactionSplitwise=False)


pub = Trip("BrewHaus")        ## The transactions contain the individuals present

pub.add_attendee(Ethan)
pub.add_attendee(Bruce)
pub.add_attendee(Pat)
pub.add_attendee(James)
pub.add_attendee(Martin)
pub.add_attendee(Cat)

pub.add_transaction(Round1)
pub.add_transaction(Round2)
pub.add_transaction(Round3)
pub.add_transaction(Round4)
pub.add_transaction(Aperol)

# pub.add_transaction(Meal2)

print(Ethan.__dict__)
input()


pub.doOverallCalculation()



exit()



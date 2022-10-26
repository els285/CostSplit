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
Ethan = Person("Ethan",account_number="34778883")
Caroline = Person("Caroline")
Chris  = Person("Chris")

Meal  = Transaction("Te Seba",payers={Caroline:30},participants=(Ethan,Caroline,Chris),doPerTransactionSplitwise=True)
Meal2 = Transaction("Pizza Hut",payers={Ethan:24},participants=(Ethan,Caroline,Chris),doPerTransactionSplitwise=True)



xmasD = Trip("xmasD")        ## The transactions contain the individuals present

xmasD.add_attendee(Ethan)
xmasD.add_attendee(Caroline)
xmasD.add_attendee(Chris)

xmasD.add_transaction(Meal)
xmasD.add_transaction(Meal2)



xmasD.doOverallCalculation()


print(xmasD.__dict__)

exit()



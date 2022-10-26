import networkx as nx
import matplotlib.pyplot as plt
from nwf import nxgraph_plotly
from splitwise_classes import Person,Transaction,Trip,Pre_Payment

doPerTransactionSplitwise = True


Ethan = Person("Ethan")
Pat = Person("Pat")
Bruce  = Person("Bruce")


pub = Trip("BrewHaus")        ## The transactions contain the individuals present



Round3 = Transaction("Guinness",payers={Ethan:24},participants=(Ethan,Pat,Bruce),doPerTransactionSplitwise=False)


Prepay1 = Pre_Payment(Pat,Ethan,5)



pub.add_attendee(Ethan)
pub.add_attendee(Bruce)
pub.add_attendee(Pat)


pub.doOverallCalculation()
# pub
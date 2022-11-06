import networkx as nx
import matplotlib.pyplot as plt

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
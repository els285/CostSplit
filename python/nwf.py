# Network Plotting
'''
Generating plots of networks using networkx and plotly (Pythonic)
'''
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import plotly.offline as py
# from splitwise_classes import Person,Transaction,Trip




def nxgraph_plotly(G):

	# First thing to do is unpack the information required 
	###Access
	# print(G.nodes)
	# input()

	pos = nx.circular_layout(G)#,k=0.4,iterations=20)

	_2plot = []

	# Draw nodes
	x = [pos[p][0] for p in pos]
	y = [pos[p][1] for p in pos]



	for node in G.nodes:
		if type(node).__name__ == 'Person': text = node.name
		elif type(node).__name__ == 'Transaction': text = node.Transaction
		else: None

		_2plot.append(go.Scatter(x=[pos[node][0]],y=[pos[node][1]],mode='lines+markers+text',marker={"size":200},text=text,textfont_size=40))


	fig = go.Figure(data=_2plot)

	for n1,n2,data in G.edges(data=True):

		x0 = pos[n1][0]
		y0 = pos[n1][1]
		x1 = pos[n2][0]
		y1 = pos[n2][1]

		amount = data["amount"]

		# Should also plot the amount in mid-point between points above
		xm = 0.5*(x1-x0)+x0
		ym = 0.5*(y1-y0)+y0

		fig.add_trace(go.Scatter(x=[xm], y=[ym+0.05],mode='text', text=amount,textfont_size = 55))

		# This plots the arrow
		fig.add_annotation(
		  x=x1,  # arrows' head
		  y=y1,  # arrows' head
		  ax=x0,  # arrows' tail
		  ay=y0,  # arrows' tail
		  xref='x',
		  yref='y',
		  axref='x',
		  ayref='y',
		  showarrow=True,
		  arrowhead=2,
		  arrowsize=4,
		  arrowwidth=3,
		  arrowcolor='grey',
		  # align='center'
		  standoff = 120/2+70/2,
		  startstandoff=120/2+70/2,
		  width=10
		)


	fig.update_layout(
	    title_text='Splitwise Calculation'
	)

	fig.update_layout(uniformtext_minsize=50, uniformtext_mode='hide')

	fig.update_xaxes(visible=False)
	fig.update_yaxes(visible=False)



	fig.show()



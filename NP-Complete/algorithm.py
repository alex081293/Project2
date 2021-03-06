import networkx as nx
from networkx.algorithms import bipartite
import timeit
import random

# function to find cross edges between the two partitions
def findEdgeCount(dictionary1, dictionary2):
	crossEdgeCount = 0
	if len(dictionary1) < len(dictionary2):
		for i in dictionary1:
			for j in range (0, len(dictionary1[i])):
				if dictionary1[str(i)][j] not in dictionary1:
					crossEdgeCount += 1
	else:
		for i in dictionary2:
			for j in range (0, len(dictionary2[i])):
				if dictionary2[str(i)][j] not in dictionary2:
					crossEdgeCount += 1
	return crossEdgeCount

start = timeit.default_timer()

G = nx.Graph()

inputFile = open("input8.txt", "r")
outputFile = open("output8.txt", "w")

# strips the string into the data we need
nodesAndEdges = inputFile.readline().strip().split(" ")

numNodes = int(nodesAndEdges[0])
numEdges = int(nodesAndEdges[1])

# adds nodes
for i in range(1, numNodes + 1):
	G.add_node(str(i))

# adds edges
for i in range(0, numEdges):
	temp = inputFile.readline().strip().split(" ")
	node1 = temp[0]
	node2 = temp[1]
	G.add_edge(node1, node2)

# if the graph is bipartite, we can easily find the optimal soltuion
if nx.is_bipartite(G):
	top_nodes, bottom_nodes = bipartite.sets(G)
	partition1 = list(top_nodes)
	partition2 = list(bottom_nodes)
	maxEdgeCount = 0
	for i in range(0, len(partition1)):
		maxEdgeCount += len(G.neighbors(partition1[i]))

# If it's not bipartite, we must start attempting to find the optimal solution
else:
	graph_dict = dict()
	sorted_graph_dict = dict()
	for i in G.nodes():
		graph_dict[i] = G.neighbors(str(i))
		sorted_graph_dict[i] = G.neighbors(str(i))

	maxEdgeCount = 0

	dict1 = dict()
	dict2 = dict()

	# sorts graph by desc degree
	sorted_graph_dict = dict(sorted(sorted_graph_dict.items(), key = lambda (k,v): len(v), reverse = True))	

	dict1 = sorted_graph_dict

	# goes through each key of the dictionary which is on the left partition
	# and checks to see if it has a greater cross edge count in partition 1 or 
	# partition 2
	for i in dict1.keys():
		edgeCount1 = 0
		edgeCount2 = 0

		for j in dict1[i]:
			if j in dict1:
				edgeCount1 += 1
			else:
				edgeCount2 += 1

		if edgeCount1 > edgeCount2:
			dict2[i] = dict1[i]
			del dict1[i]

	currentEdgeCount = findEdgeCount(dict1, dict2)

	if currentEdgeCount > maxEdgeCount:
		maxEdgeCount = currentEdgeCount
		partition1 = dict1.keys()
		partition2 = dict2.keys()				

	# Runs a randomized algorithm to check if we can beat our previous
	# max edge count. If the a better soltion is found, we keep those partitions
	for k in range(0, 1000):
		temp1 = dict()
		temp2 = dict()
		for i in graph_dict:
			x = random.randint(0, 6564823) % 2

			if x == 0:
				temp1[i] = graph_dict[i]
			else:
				temp2[i] = graph_dict[i]

		currentEdgeCount = findEdgeCount(temp1, temp2)

		if currentEdgeCount > maxEdgeCount:
			maxEdgeCount = currentEdgeCount
			partition1 = temp1.keys()
			partition2 = temp2.keys()
		
stop = timeit.default_timer()

elapsed = (stop - start) * 1000.0

outputFile.write("%s\n" % elapsed)

outputFile.write("%s\n" % maxEdgeCount)

for i in range(0, len(partition1)):
	outputFile.write(partition1[i])
	outputFile.write(" ")

outputFile.write("\n\n")

for i in range(0, len(partition2)):
	outputFile.write(partition2[i])
	outputFile.write(" ")

inputFile.close()
outputFile.close()
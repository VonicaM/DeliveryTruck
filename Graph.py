# This is the vertex class. It has functions for the creation and representation of vertex objects.
class Vertex:
	def __init__(self, label):
		self.label = label
		# The place value will be used to store the minimum distance from this vertex to the hub vertex.
		self.place = 0
		# The distance and pred vertex values are used by the dijkstra function to organize the verticies stored within a graph object based on their minimum distance from a given vertex, and the path from that vertex to this vertex.
		self.distance = float('inf')
		self.predVertex = None
	
	# Whenever a vertex is printed, its ID is what gets printed.
	def __repr__(self):
		return self.label

# This is the graph class. It manages the relationships between a collection of verticies.
class Graph:
	def __init__(self):
		# A dictionary that takes a vertex as a key and returns a list of verticies adjavent to the given vertex.
		self.adjacencyList = {}
		# A dictionary that takes a tuple of adjacent verticies as a key, representing an edge in the graph, and returns the distance from the first vertex in the tuple to the second vertex in the tuple.
		self.edgeWeights = {}
	
	# A function that takes a provided vertex, and adds it into the dictionary of adjacent verticies with an empty list.
	def addVertex(self, newVertex):
		self.adjacencyList[newVertex] = []
	
	# A function that take a from vertex, a to vertex, and the distance from the from vertex to the to vertex. The to vertex is declared adjacent to the from vertex by adding it to the list corresponding to the from vertex in the adjacency list dictionary, and an entry with the distance from the from vertex to the to vertex is added to the edge weights dictionary.
	def addDirectedEdge(self, fromVertex, toVertex, weight = 1.0):
		self.edgeWeights[(fromVertex, toVertex)] = weight
		self.adjacencyList[fromVertex].append(toVertex)
	
	# A function that takes to verticies and the distance between them, and calls the add directed edge function to record these two verticies as adjacent to each other, and to record the distance between them as equal going from a to b, as well as from b to a.
	def addUndirectedEdge(self, vertexA, vertexB, weight = 1.0):
		self.addDirectedEdge(vertexA, vertexB, weight)
		self.addDirectedEdge(vertexB, vertexA, weight)

# A function that takes a graph and starting vertex, and determines the shortest distance from the starting vertex to all points in the graph, as well as the shortest path.
def dijkstraShortestPath(g, startVertex):
	# Put all vertices in an unvisited queue.
	unvisitedQueue = []
	for currentVertex in g.adjacencyList:
		unvisitedQueue.append(currentVertex)
	
	# The start vertex has a distance of 0 from itself
	startVertex.distance = 0
	
	# One vertex is removed with each iteration, and this is repeated until all verticies have been processed.
	while len(unvisitedQueue) > 0:
		# Visit the vertex with minimum distance from the start vertex, including the start vertex itself
		smallestIndex = 0
		for i in range(1, len(unvisitedQueue)):
			if (unvisitedQueue[i].distance < unvisitedQueue[smallestIndex].distance):
				smallestIndex = i
		currentVertex = unvisitedQueue.pop(smallestIndex)
		
		# Check the potential path lengths from the current vertex to all its neighbors.
		for adjVertex in g.adjacencyList[currentVertex]:
			edgeWeight = g.edgeWeights[(currentVertex, adjVertex)]
			alternativePathDistance = currentVertex.distance + edgeWeight
			
			# If a shorter path from the start vertex to the adj vertex is found, update the adj vertex's distance and predecessor vertex.
			if (alternativePathDistance < adjVertex.distance):
				adjVertex.distance = alternativePathDistance
				adjVertex.predVertex = currentVertex

# A function that takes a graph that has been used in the dijkstea shortest path function, and resets it so that it can be put through that function again without any issues.
def dijkstraReset(g):
		for currentVertex in g.adjacencyList:
			currentVertex.distance = float('inf')
			currentVertex.predVertex = None
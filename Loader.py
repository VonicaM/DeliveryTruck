import Package
import Graph
import csv

# This function takes a csv file and graph object, and parses data from the csv file into the graph object.
def loadGraphData(filename, graph):
	# Opens the csv file.
	with open(filename) as map:
		# Divide the file off of commas.
		mapData = csv.reader(map, delimiter=',')
		# A list of already processed locations.
		locationsList = []
		# Skip the header.
		next(mapData)
		# Go through the file line by line.
		for location in mapData:
			# The first column in the file contains the location address. This is used as the label for the new vertex, which is added to the graph.
			lAddress = location[0]
			newVertex = Graph.Vertex(lAddress)
			graph.addVertex(newVertex)
			# An iteration is ran for every previously processed vertex.
			for i in range(0, len(locationsList)):
				# An edge is created between the new vertex and every previously created vertex, with distance data taken from columns in the file in the order that the previous verticies were added.
				adjacentVertex = locationsList[i]
				graph.addUndirectedEdge(newVertex, adjacentVertex, float(location[i+2]))
			# The current vertex is added to the list of processed verticies.
			locationsList.append(newVertex)

# This function takes a csv file, list, hash table, and graph, and parses data from the csv file into the list and hash table as package objects, with links to verticies from the graph object.
def loadPackageData(filename, priority, hash, graph):
	# Open the csv file.
	with open(filename) as packages:
		# Divide the file off of commas.
		packageData = csv.reader(packages, delimiter=',')
		# Skip the header.
		next(packageData)
		# Go through the file line by line.
		for package in packageData:
			 # Each column has a different piece of package data.
			 pID = int(package[0])
			 pAddress = package[1]
			 # Will be a vertex taken from the graph based on the address.
			 pDeliveryLocation = None
			 pCity = package[2]
			 pState = package[3]
			 pZip = package[4]
			 pDeadline = int(package[5])
			 pMass = int(package[6])
			 # The special package note has multiple distinct parts to it, and those parts are seperated into a list.
			 pSpecial = package[7].split('.')
			 
			 # Iterate through every vertex in the graph object, searching for one that contains this package's address. Once the vertex is found, record it as the delivery location, and stop the search.
			 for place in graph.adjacencyList.keys():
			 	if (pAddress in place.label):
			 		pDeliveryLocation = place
			 		break
			 
			 # Create a package with all the recorded attributes.
			 p = Package.Package(pID, pAddress, pDeliveryLocation, pCity, pState, pZip, pDeadline, pMass, pSpecial)
			 
			 # Add the created package to the list and the hash table.
			 priority.append(p)
			 hash.insert(p.ID, p)
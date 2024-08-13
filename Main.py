# Michael Vonica, 001464347

import HashTable
import Graph
import Loader
import Truck
import Event
import heapq
#import pandas as pd

# This graph holds all data on the different delivery locations and the distance between them. It is populated by a function from the Loader file.
myGraph = Graph.Graph()
Loader.loadGraphData("WGUPS Distance Table.csv", myGraph)

# The hub is a special location, and it is useful to have it on hand without the need to search for it. The list of locations from the graph is searched through for any location with a label matching the hub's label, and that location is set as the hub, and the search is terminated.
hub = None
for place in myGraph.adjacencyList.keys():
	if (place.label == "Western Governors University 4001 South 700 East, Salt Lake City, UT 84107"):
		hub = place
		break

# For the purpose of setting package priority later, a function from the Graph file is used to organize the graph by distance from the hub.
Graph.dijkstraShortestPath(myGraph, hub)
for currentVertex in myGraph.adjacencyList:
	currentVertex.place = currentVertex.distance
Graph.dijkstraReset(myGraph)

# Truck creation. Each truck regularly has 16 package slots, but truck 1 is limited to only 6, to make it return more often to the hub to pick up late high priority packages.
truck1 = Truck.Truck(1, hub)
truck1.maxLoad = 6
truck2 = Truck.Truck(2, hub)

# Both a priority queue and a hash table are created to store package data. A loader funtion from the Loader file is used to populate both. The priority queue orders the packages off of the importance of delivery, and is used to decide which package is to be loaded next onto the trucks. The hash table is mostly used for showing the status of all packages to the user.
myHash = HashTable.ChainingHashTable()
priorityPackage = []
Loader.loadPackageData("WGUPS Package File.csv", priorityPackage, myHash, myGraph)
heapq.heapify(priorityPackage)

# A priority queue of event objects from the Event file is created. An event to take user input, as well as an event each for the loading of both trucks, are added.
schedule = []
userInput = Event.UserInput(759, truck1, truck2, myHash, schedule)
start1 = Event.Load(800, truck1, priorityPackage, myGraph, hub, schedule)
start2 = Event.Load(800, truck2, priorityPackage, myGraph, hub, schedule)
heapq.heappush(schedule, userInput)
heapq.heappush(schedule, start1)
heapq.heappush(schedule, start2)

# While there are still events to be processed, the highest priority event, which will always be the event occuring at the earliest time, will be taken off, and have its execute function called. The execution function depends on the type of event that was popped off the queue. All events have an execute function that takes no paramaters.
while (schedule):
	event = heapq.heappop(schedule)
	event.execute()

# Once the program is done, the total truck mileage is posted, as well as the truck routes, and which packages were delivered by which truck.
print("Total combined miles: " + str(truck1.mileage + truck2.mileage))

print("Truck 1 route: " + str(truck1.route))
print()
print("Truck 1 packages: " + str(truck1.packageLoads))
print()
print("Truck 2 route: " + str(truck2.route))
print()
print("Truck 2 packages: " + str(truck2.packageLoads))
'''for bucket in myHash.table:
	for package in bucket:
		print("Package " + str(package[0]) + ", " + package[1].status + "', deadline " + str(package[1].deadline) + "', address " + package[1].address + "', city " + package[1].city + "', zip " + package[1].zip + "', mass " + str(package[1].mass))
		print()
'''
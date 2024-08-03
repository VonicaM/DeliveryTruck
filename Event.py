import Graph
import heapq

# The event class is the parent class for all other classes in the Event file. It has functions for the comparison of event objects. All other classes are children of this class to prevent the repition of these functions.
class Event:
	# These three functions are used to compare events to each other based off of their scheduled time. It is checked if they have the time attribute, and then a comparison is made based on the float value of that time attribute.
	def _is_valid_operand(self, other):
		return(hasattr(other, "time"))
	
	def __eq__(self, other):
		 if not self._is_valid_operand(other):
		 	return NotImplemented 
		 return (self.time == other.time)
	
	def __lt__(self, other):
		 if not self._is_valid_operand(other):
		 	return NotImplemented 
		 return (self.time < other.time)

# The load class is meant to represent the action of loading packages onto a truck. It calls for a time to execute, truck to load packages onto, priority queue of all packages that need loading, graph and hub to pass onto the routing event when called, and schedule to add future routing and loading events to. The loading class, like all events, has one execute function. The loading class's execute function has four outcomes. First, the load class can recognize that there are no more packages to load, and cease execution. Second, it can recognize all packages that can be loaded onto the provided truck, in an optimal order of loading, load them, and call for an event to plot that truck's route. Third, it can recognize that there are no packages in the list that can currently be loaded, but that there is a time in the future when a package will be available to be loaded, and set another loading event for the earlies such future time. Finally, it can recognize there are no packages that can be loaded onto this truck, and that there never will be such packages, and cease execution.
class Load(Event):
	def __init__(self, time, truck, packages, graph, hub, schedule):
		self.time = time
		self.truck = truck
		self.packages = packages
		self.graph = graph
		self.hub = hub
		self.schedule = schedule
	
	def execute(self):
		# Check to see if any packages need loading. If not, cease execution.
		if (not self.packages):
			return None
		
		# The list of temp packages will contain all packages from the priority list that were processed and determined to be currently undeliverable by the given truck. These packages will still need to be delivered later, and so this list will be merged back with the original priority list.
		tempPackages = []
		# This float is used to recognize the earliest time that a currently unloadable package will become available for loading. It is set to infinity to indicate no such packages existing.
		nextLoadTime = float('inf')

		packageLog = []
		
		# Packages are continously pulled off of the priority list until the truck is fully loaded with packages, or the priority list is empty.
		while (not (self.truck.load == self.truck.maxLoad) and self.packages):
			package = heapq.heappop(self.packages)
			# The special note of the current package is now evaluated to determine if this truck can load this package at this time. If it can, it marks the package as en route, increases the teuck load by 1, and adds the package to the hash table of the truck. If it can't, the package is added to the temp packages list, for later merging.
			# 0 means no special note.
			if (package.special[0] == "0"):
				package.status = "en route"
				self.truck.load += 1
				self.truck.packages.insert(package.ID, package)
				packageLog.append(package.ID)
			
			# 1 means truck specified. The current truck is checked to see if it matches the truck specified in the package's special note.
			elif (package.special[0] == "1"):
				if (int(package.special[1]) == self.truck.label):
					package.status = "en route"
					self.truck.load += 1
					self.truck.packages.insert(package.ID, package)
					packageLog.append(package.ID)
				else:
					tempPackages.append(package)
			
			# 2 means late arrival. The current time is checked to see if the package has arrived at the hub yet. If it has not yet arrived, after adding the rejected package to temp packages, the package is checked to see if its arrival time is earlier than nextLoadTime. If it is, nextLoadTime is set to the package's arrival time.
			elif (package.special[0] == "2"):
				if (int(package.special[1]) <= self.time):
					package.status = "en route"
					self.truck.load += 1
					self.truck.packages.insert(package.ID, package)
					packageLog.append(package.ID)
				else:
					tempPackages.append(package)
					if (int(package.special[1]) < nextLoadTime):
						nextLoadTime = int(package.special[1])
			
			# 3 means delivery misprint. The current time is checked to see if the package has arrived at the hub yet. If it has, its adress and delivery location are updated before loading it. If it has not yet arrived, after adding the rejected package to temp packages, the package is checked to see if its arrival time is earlier than nextLoadTime. If it is, nextLoadTime is set to the package's arrival time.
			elif (package.special[0] == "3"):
				if (int(package.special[1]) <= self.time):
					package.status = "en route"
					package.address = package.special[2]
					deliveryLocation = None
					for place in self.graph.adjacencyList.keys():
						if (package.address in place.label):
							deliveryLocation = place
							break
					package.deliveryLocation = deliveryLocation
					self.truck.load += 1
					self.truck.packages.insert(package.ID, package)
					packageLog.append(package.ID)
				else:
					tempPackages.append(package)
					if (int(package.special[1]) < nextLoadTime):
						nextLoadTime = int(package.special[1])
			
			#4 means package delivery group.
			elif (package.special[0] == "4"):
				# The truck's current load and max load are checked to see if it can fit the entire delivery group. If it can not, the current package is rejected.
				if ((self.truck.maxLoad - self.truck.load) >= (len(package.special) - 1)):
					# If the truck can fit the whole group, the current package is loaded into the truck.
					package.status = "en route"
					self.truck.load += 1
					self.truck.packages.insert(package.ID, package)
					packageLog.append(package.ID)
					
					# A list containing all of the IDs of the packages in the group is extracted from the current package's special note, and the ID of the current package is removed from this list.
					packageGroup = package.special[1:]
					packageGroup.remove(str(package.ID))
					
					# The program will now begin iterating through all the packages in the priority queue, until all the packages in the group have been found and loaded. A secondary list of packages that have been rejected and will need to be merged with the priority queue is formed here.
					veryTempPackages = []
					while packageGroup:
						veryTempPackage = heapq.heappop(self.packages)
						# Check to see if the current package's ID is in the list of package IDs for the group. If it is, load the package, and remove the ID of the current package from the list. If it is not, add the current package to the list of rejects.
						if (str(veryTempPackage.ID) in packageGroup):
							veryTempPackage.status = "en route"
							self.truck.load += 1
							self.truck.packages.insert(veryTempPackage.ID, veryTempPackage)
							packageLog.append(veryTempPackage.ID)
							packageGroup.remove(str(veryTempPackage.ID))
						else:
							veryTempPackages.append(veryTempPackage)
					# Merge back the queue and list.
					self.packages[:] = list(heapq.merge(self.packages, veryTempPackages))
				else:
					tempPackages.append(package)
		
		# Now that the load event is done processing packages, the original priority queue of packages given as a refernce to this class instance is set equal to a merging of the current priority queue of remaining packages, and the list of rejected packages. This means any other class instamces that shared a refernce to the priority queue will also now see this updated queue.
		self.packages[:] = list(heapq.merge(self.packages, tempPackages))
		self.truck.packageLoads.append(packageLog)
		# If the truck has any packages loaded, then an event for plotting the truck's delivery route is added to the schedule, to occur immediately.
		if (self.truck.load > 0):
			heapq.heappush(self.schedule, PlotRoute(self.time, self.truck, self.packages, self.graph, self.hub, self.schedule))
		# If there are no loaded packages.
		else:
			# Check to see if there will be any packages in need of loading at a later time. If there are not, cease execution. If there are, then an event for loading the truck is added to the schedule, for when the next earliest package is available to be loaded.
			if (nextLoadTime == float('inf')):
				return None
			else:
				heapq.heappush(self.schedule, Load(nextLoadTime, self.truck, self.packages, self.graph, self.hub, self.schedule))

# The plot route class is meant to represent the action of planning the route for the next destination of the truck. It calls for a time to execute, truck to plot the route of, priority queue to pass onto the next load or plot event, graph to access vertex and edge data from, hub to recognize the loading location, and schedule to add future arrival, delivery, plotting, and loading events. The plotting class, like all events, has one execute function. The plotting class's execute function has two outcomes. First, the plotting class can recognize that there are no more packages to deliver, and plots a route back to the hub, before calling a loading event. Second, it can choose the package with a delivery location nearest to the current location of the delivery truck from all currently loaded packages, plot a route to the delivery location of that package, and then call a deliver event and plotting event.
class PlotRoute(Event):
	def __init__(self, time, truck, packages, graph, hub, schedule):
		self.time = time
		self.truck = truck
		self.packages = packages
		self.graph = graph
		self.hub = hub
		self.schedule = schedule
	
	def execute(self):
		# The shortest path function is called from the graph file to determine the shortest distance of every location on the graph from the current location of the truck.
		Graph.dijkstraShortestPath(self.graph, self.truck.location)
		# A temporary destination vertex is created. This temporary vertex is by default set to be infinitely far from the truck's current location, and so, when compared against the delivery locations of all the truck's packages to find the closest delivery location, it will always be replaced by an eligable option.
		destination = Graph.Vertex("Temp")
		# The truck is checked to see if it has any packages. If it does, the program iterates through all packages in the truck's hash table to find the package with the delivery location closest to the truck's current location. This delivery location is set as the destination. If the truck has no packages, the hub is set as the destination.
		if (self.truck.load > 0):
			for bucket in self.truck.packages.table:
				for package in bucket:
					if (package[1].deliveryLocation.distance < destination.distance):
						destination = package[1].deliveryLocation
		else:
			destination = self.hub
			
		# A path is created from the destination to the location of the truck, by adding the current vertex to the path, and setting the current vertex to its own preceding vertex, until the current vertex is the location of the truck.
		currentVertex = destination
		path = []
		while (currentVertex != self.truck.location):
			path.append(currentVertex)
			currentVertex = currentVertex.predVertex
		path.append(self.truck.location)
		
		# Time is formatted from military time to minutes and hours, so that the travel time between verticies can be added in, before converting back to military time.
		time = self.time
		min = time % 100
		hour = (time - min) / 100
		
		# Every vertex on the path from the truck to the destination is iterated through, and an arrival event is called for every vertex but the one the truck is currently located at.
		while (len(path) > 1):
			# Travel time is determined by the distance from the vertex at the end of the path and the vertex one index closer to the front of the path. This distance is divided by 18 MPH, the travel speed of the truck, and multiplied by 60, to convert it into minutes.
			travelTime = (self.graph.edgeWeights[(path[-1], path[-2])] * 60 / 18)
			# Travel time is converted into minutes and hours, before then combining it with the current time, and once again reformatting to ensure that there are no more than sixty minutes.
			travelMin = travelTime % 60
			travelHour = (travelTime - travelMin) / 60
			totalMin = min + travelMin
			totalHour = hour + travelHour
			min = totalMin % 60
			hour = totalHour + (totalMin - min) / 60
			# An arrival event is added to the schedule, set to occur on the expected arrival time of the truck at the location.
			heapq.heappush(self.schedule, Arrival((hour * 100) + min, self.truck, path[-2], self.graph.edgeWeights[(path[-1], path[-2])]))
			# The last element of the path is removed, as the truck has already moved on from there.
			path.pop(-1)
		# If the truck has any packages to deliver, then it adds a delivery event to the schedule, set to occur directly after the last added arrival event. A plot route event is also added to the schedule, set to occur directly after the delivery event.
		if (self.truck.load > 0):
			heapq.heappush(self.schedule, Deliver((hour *100) + min + 0.001, self.truck ))
			heapq.heappush(self.schedule, PlotRoute((hour *100) + min + 0.002, self.truck, self.packages, self.graph, self.hub, self.schedule))
		# If the truck has no packages to deliver, then it adds a load event to the schedule, set to occur directly after the last added arrival event.
		else:
			heapq.heappush(self.schedule, Load((hour *100) + min + 0.001, self.truck, self.packages, self.graph, self.hub, self.schedule))
		Graph.dijkstraReset(self.graph)

# The arrival class is meant to represent the action of the truck arriving at a vertex. It calls for a time to execute, a truck to arrive, a location for the truck to arrive at, and a distance for the truck to have traveled. The arrival class, like all events, has one execute function. The arrival class's execute function sets the location of the truck to the provided location, and adds the distance traveled to the milage of the truck.
class Arrival(Event):
	def __init__(self, time, truck, location, mileage):
		self.time = time
		self.truck = truck
		self.location = location
		self.mileage = mileage
	
	def execute(self):
		self.truck.location = self.location
		self.truck.mileage += self.mileage
		self.truck.route.append(self.location.label)

# The deliver class is meant to represent the action of the truck delivering packages. It calls for a time to execute, and a truck that will deliver thw packages. The deliver class, like all events, has one execute function. The deliver class's execute function finds all the packages from those currently loaded onto the truck with a delivery location matching the truck's current location, sets their status to delivered, decreases the number of packages currently stored on the truck by one for each package, and removes the packages from the truck's hash table.
class Deliver(Event):
	def __init__(self, time, truck):
		self.time = time
		self.truck = truck
	
	def execute(self):
		# Create a list of package IDs to be removed from the truck's hash table. They are removed after iterating through the hash table, to prevent errors.
		deliveryList = []
		# The program iterates through all packages in the truck's hash table to find any packages with a delivery location equal to the truck's current location. When they are found, these packages have their status set to delivered, the truck has its current load decreased by one, and the ID of the package is added to the delivery list.
		for bucket in self.truck.packages.table:
			for package in bucket:
				if (package[1].deliveryLocation == self.truck.location):
					deliveryList.append(package[1].ID)
					package[1].status = "delivered at " + str(self.time)
					package[1].deliveryTime = self.time
					self.truck.load -= 1
		# The program iterates through the delivery list, removing every ID there from the truck's hash table.
		for delivery in deliveryList:
			self.truck.packages.remove(delivery)

# The user input class is meant to represent the action of a user viewing the delivery progress. It calls for a time to execute, two trucks to view the mileage of, a hash table of packages to view the status of, and a schedule to add more user input events to. The user input class, like all events, has one execute function. The user input class's execute function allows the user to view the delivery status of all packages, view the complete status of a single package specified by the user, view the mileage of all trucks, set a time for another user input event, and cease execution of all user input events.
class UserInput(Event):
	def __init__(self, time, truck1, truck2, packages, schedule):
		self.time = time
		self.truck1 = truck1
		self.truck2 = truck2
		self.packages = packages
		self.schedule = schedule
	
	def execute(self):
		# Continue looping forever.
		while (1):
			# Collect a choice from the user.
			choice = input("The time is " + str(self.time) + ". Input your choice. 1 - View all package delivery statuses. 2 - Search for package information by package ID. 3 - View truck mileages. 4 - Schedule another check for a later time. 5 - End all checks. ")
			# 1 means show the delivery status of all pavkages by looping through the hash table.
			if (choice  == '1'):
				for bucket in self.packages.table:
					for package in bucket:
						print("Package " + str(package[0]) + ", " + package[1].status + "', deadline " + str(package[1].deadline) + "', address " + package[1].address + "', city " + package[1].city + "', zip " + package[1].zip + "', mass " + str(package[1].mass))
						print()
			# 2 means collect an input from the user for the ID of a package, call the hash table's search function to get the package, and print all of that package's data.
			elif (choice  == '2'):
				search = input("Enter the ID of the package you wish to find: ")
				package = self.packages.search(int(search))
				print(package.ID)
				print(package.address)
				print(package.deadline)
				print(package.city)
				print(package.zip)
				print(package.mass)
				print(package.status)
			# 3 means print the mileage information for both trucks.
			elif (choice  == '3'):
				print("Truck 1: " + str(self.truck1.mileage))
				print("Truck 2: " + str(self.truck2.mileage))
				print("Combined: " + str(self.truck1.mileage + self.truck2.mileage))
			# 4 means collect an input from the user and add a user input event to the schedule to be executed at the time provided by the user. The n end execution of this user input event.
			elif (choice  == '4'):
				time = input("Enter next check up time in military format: ")
				heapq.heappush(self.schedule, UserInput(int(time), self.truck1, self.truck2, self.packages, self.schedule))
				return None
			# 5 means cease execution.
			elif (choice  == '5'):
				return None
			else:
				print("Unreadible input.")
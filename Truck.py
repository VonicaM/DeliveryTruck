import HashTable

# This file contains code for the truck class. The class has a function for the creation of truck objects.
class Truck:
	def __init__(self, label, location):
		self.label = label
		# The truck has a hash table of currently loaded packages.
		self.packages = HashTable.ChainingHashTable()
		self.location = location
		self.load = 0
		self.maxLoad = 16
		self.mileage = 0
		self.packageLoads = []
		self.route = []
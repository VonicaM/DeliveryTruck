# This file contains code for the package class. The class has functions for the creation and comprison of package objects.
class Package:
	def __init__(self, ID, address, deliveryLocation, city, state, zip, deadline, mass, special):
		self.ID = ID
		self.address = address
		
		# The delivery location is an actual vertex object, stored so that the vertex only needs to be searched for once to be found.
		self.deliveryLocation = deliveryLocation
		self.city = city
		self.state = state
		self.zip = zip
		self.deadline = deadline
		self.mass = mass
		
		# The special note attached to a package is parsed as a list of strings, with the first element identifying the type of note, and the elements afterwards detailing the specifics of how that package should be handled
		self.special = special
		self.status = "at the hub"
		self.deliveryTime = 2500
		
		# The value attribute is used to rank packages based on the importance of delivery. Packages with earlier deadlines have greater importance, as do packages farther from the hub. Each delivery vertex has an attribute recording distance from the hub. Basing priority off of hub distanve is mainly so that packages from the same locations will be grouped together. In the end, the value is inverted, because a min heap is used to store the package order, where lowest value elemtns are the most important.
		self.value = 2400 - self.deadline
		self.value = self.value*100
		self.value += deliveryLocation.place
		self.value = self.value*-1
	
	# Whenever a package is printed, its ID is what gets printed.
	def __repr__(self):
		return str(self.ID)
	
	# The next three functions are used to compare packages to each other based off of their priority. It is checked if they have the value attribute, and then a comparison is made based on the float value of that value attribute.
	def _is_valid_operand(self, other):
		return(hasattr(other, "value"))
	
	def __eq__(self, other):
		 if not self._is_valid_operand(other):
		 	return NotImplemented 
		 return (self.value == other.value)
	
	def __lt__(self, other):
		 if not self._is_valid_operand(other):
		 	return NotImplemented 
		 return (self.value < other.value)
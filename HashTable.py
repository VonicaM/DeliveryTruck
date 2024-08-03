# This file contains code for the chaining hash table class. The class has functions for the creation and management of hash table data structures.
class ChainingHashTable:
	def __init__(self, initialCapacity=10):
		# This table will be seperated into a number of lists based off of the provided initial capacity. Each list will be a bucket, and will contain tuples with the key and matching element.
		self.table = []
		for i in range(initialCapacity):
			self.table.append([])
	
	# This function takes a key and an object and adds them into the hash table as a tuple, based on the value of the key. If a key is already present, the attached object is uodated with the new object.
	def insert(self, key, item):
		# Get the bucket list where this item will go.
		bucket = hash(key) % len(self.table)
		bucketList = self.table[bucket]
		
		# Update key if it is already in the bucket.
		for kv in bucketList:
			if kv[0] == key:
				kv[1] = item
				return True
		# If not, insert the item to the end of the bucket list.
		keyValue = [key, item]
		bucketList.append(keyValue)
		return True
	
	# This function takes a key and searches the hash table for it. If a matching key is foumd, the attavhed object is returned, and if not, None is returned.
	def search(self, key):
		# Get the bucket list where this key would be.
		bucket = hash(key) % len(self.table)
		bucketList = self.table[bucket]
		
		# Search for the key in the bucket list.
		for kv in bucketList:
			if kv[0] == key:
				return kv[1]
		return None
	
	# This function removes an item with a matching key from the hash table.
	def remove(self, key):
		# Get the bucket list where this item will be removed from.
		bucket = hash(key) % len(self.table)
		bucketList = self.table[bucket]
		
		# Remove the item from the bucket list if it is present.
		for kv in bucketList:
			if kv[0] == key:
				bucketList.remove([kv[0],kv[1]])
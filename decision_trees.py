########################################################################
# FILE : ex11.py
# WRITER : Lidar Abukarat , lidarabu1 , 318929742
# EXERCISE : intro2cs1 ex11 2021
# DESCRIPTION: A program of decision tree.
########################################################################
from itertools import combinations
TypeError_1 = "There is an item in the symptoms list which is not a str type of object"
TypeError_2 = "There is an item in the records list which is not a Record type of object"
ValueError_1 = "The depth argument is invalid"
ValueError_2 = "There is a double symptom in the list"


class Node:
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child


class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms
	
			
def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records
		
		
class Diagnoser:
	def __init__(self, root: Node):
		self.root = root

	def _helper_diagnose(self, node, symptoms):
		"""This function returns the illness that corresponds to the symptoms
		in the list according to the tree.
		This function works recursively, while in each call the function
		receives the node represent the sub-tree we check know.
		:symptoms: list of strings - the symptoms
		:node: Node type of object
		:return: str if illness found, None if not"""
		if node.positive_child is None:  # the node is a leaf.
			return node.data
		if node.data in symptoms:  # the answer is yes - go to the right side
			return self._helper_diagnose(node.positive_child, symptoms)
		if node.data not in symptoms:  # the answer is no - go to the left side
			return self._helper_diagnose(node.negative_child, symptoms)

	def diagnose(self, symptoms):
		"""This function returns the illness that corresponds to the symptoms
		in the list according to the tree
		:param symptoms: list of string - the symptoms
		:return: str if illness found, None if not"""
		return self._helper_diagnose(self.root, symptoms)

	def calculate_success_rate(self, records):
		"""
		This function diagnoses an illness for each record's symptoms
		(using diagnose function) and checks if the result is the actual
		record's illness. The function return the rate between successful
		diagnoses to all records.
		:param records: list of record type of objects
		:return: float - rate between successful diagnoses to all records
		"""
		num_of_successes = 0
		for record in records:
			if record.illness == self.diagnose(record.symptoms):
				num_of_successes += 1
		if not records:
			raise ValueError("The records list is empty")
		return num_of_successes / len(records)

	def _helper_all_illness(self, node, illnesses):
		"""
		This function updates the dictionary that contains all illnesses that
		are leaves in the tree. This function works recursively, while in each
		call the function receives the node represent the sub-tree we check.
		:param node: Node type of object
		:param illnesses: dict of the illness as a key, and the number of
		appearances in the tree as a value
		:return: None
		"""
		if node.positive_child:  # the node has children
			self._helper_all_illness(node.positive_child, illnesses)
			self._helper_all_illness(node.negative_child, illnesses)
		else:  # the node is a leaf
			if node.data:  # append only actual illnesses (not None data)
				if node.data not in illnesses:
					illnesses[node.data] = 1
				else:
					illnesses[node.data] += 1

	def all_illnesses(self):
		"""
		This function returns a list of all illnesses that are leaves in the tree.
		:return: list of strings
		"""
		illnesses = {}
		self._helper_all_illness(self.root, illnesses)
		lst = [(ill, num) for ill, num in illnesses.items()]
		lst.sort(key=lambda x: x[1], reverse=True)  # sort the pairs from the
		# one who appears the most, to the one who appears the least.
		final_illnesses = [pair[0] for pair in lst]
		return final_illnesses

	def _helper_path_to_illness(self, illness, node, paths, path):
		"""
		This function returns list of lists, that each list is a path from the
		root to the illness (which is a leaf in the tree). the path represented
		by list of True and False value, according to if we turn to the 'yes'
		side, or to the 'no' side.
		:param illness: string - the illness we search a paths to
		:param node: the node represent the root of the sub-tree we search in now
		:param paths: list of lists - all paths
		:param path: list of booleans - one path
		:return: None
		"""
		if not node.positive_child:  # this node is a leaf
			if illness == node.data:
				paths.append(path)
			else:
				# if node's data is not the illness we search, return.
				return
		else:  # the node has children
			self._helper_path_to_illness(illness, node.positive_child, paths, path + [True])
			self._helper_path_to_illness(illness, node.negative_child, paths, path + [False])

	def paths_to_illness(self, illness):
		"""
		This function returns list of lists, that each list is a path from the
		root to the illness (which is a leaf in the tree).
		:param illness: string - the illness we search a paths to
		:return: list of lists of booleans - all paths
		"""
		# if the illness is not in the tree
		if illness and illness not in self.all_illnesses():
			return []
		else:
			paths = []
			one_path = []
			self._helper_path_to_illness(illness, self.root, paths, one_path)
			return paths

	def equal_trees(self, node1, node2):
		"""
		This function checks if too two trees are equal.
		:param node1: node - the root of the first tree
		:param node2: node - the root of the second tree
		:return: True oe False
		"""
		if not node1 and not node2:  # the trees are empty
			return True
		# if both trees are not empty we want to chek if the sub trees are equal
		elif node1 and node2:
			return (node1.data == node2.data) and \
				   self.equal_trees(node1.negative_child, node2.negative_child) and \
				   self.equal_trees(node1.positive_child, node2.positive_child)
		# if one tree is empty and the other is not
		else:
			return False

	def _helper_false(self, node):
		"""
		This function removes nodes from the tree if they don't effects the
		diagnose of this branch. Works recursively and uses equal_trees function
		to check if sub-tree are equal and the current node doesnt effect the
		result.
		:param node: the current node we checks if necessary
		:return: the node which is the root of the updated tree
		"""
		if node is None:
			return
		if not node.positive_child and not node.negative_child:
			return node
		else:  # we want to get to father of a leaf
			# set the children to be the node who came back from the last call
			node.positive_child = self._helper_false(node.positive_child)
			node.negative_child = self._helper_false(node.negative_child)
			# if the sub trees are equals, returns the root of one of them
			if self.equal_trees(node.positive_child, node.negative_child):
				return node.positive_child
		return node

	def _helper_true(self, node):
		if node is None:
			return
		# if this node is leaf, we return it.
		if not node.positive_child:
			return node
		else:  # we want to get to father of a leaf
			positive_sub_tree = self._helper_true(node.positive_child)
			negative_sub_tree = self._helper_true(node.negative_child)
		# if the current root's data is None, returns the other tree.
		if positive_sub_tree.data is None:
			return negative_sub_tree
		elif negative_sub_tree.data is None:
			return positive_sub_tree
		return Node(node.data, positive_sub_tree, negative_sub_tree)

	def minimize(self, remove_empty=False):
		"""
		This function change the tree it receives with tree which have no
		unnecessary nodes. Unnecessary nodes are nodes that doesnt affects
		the diagnose while remove_empty's value is False, and in addition
		nodes that the diagnose the lead to is None, while remove_empty's value is True.
		:param remove_empty: True or False
		:return: None
		"""
		if not remove_empty:
			self.root = self._helper_false(self.root)
		if remove_empty:
			self.root = self._helper_true(self.root)
			self.root = self._helper_false(self.root)


def set_illness(path, records, symptoms):
	"""
	This function checks, according to the path, which record from the records
	list is the most suitable to be the leaf of this current path.
	For each record, the function checks if the symptom that it's answer is
	True is in the record's symptoms list, and if the symptom that it's answer
	is False is not in the record's symptoms list. If the answer is yes, the
	record is an optional leaf.
	:param path: list of booleans - the path to the node by True or False steps.
	:param records: list of record type of objects
	:param symptoms: list of string - the original symptoms list
	:return: the data to the leaf
	"""
	records_dict = {}
	for record in records:
		symptoms_ok = True  # represent if the record is an optional leaf or not
		for i in range(len(path)):
			answer = path[i]
			sym = symptoms[i]
			if answer and sym not in record.symptoms:
				symptoms_ok = False
			elif not answer and sym in record.symptoms:
				symptoms_ok = False
		# If all symptoms are suite to the record's symptoms, this record is good
		if symptoms_ok:
			if record.illness in records_dict:
				records_dict[record.illness] += 1
			else:
				records_dict[record.illness] = 1
	# If there is no optional records, the leaf's data will be None
	if not records_dict:
		return None
	else:
		lst = [(ill, num) for ill, num in records_dict.items()]
		lst.sort(key=lambda x: x[1])  # we want the illness that appears in
		# maximum number of records.
		return lst[-1][0]


def _helper_build_tree(records, symptoms, SYMPTOMS, path):
	"""
	This function creates a tree, according to the records list and the symptoms
	list it receives. This function works recursievly, and uses set_illness
	function to set illnesses in the leaves.
	:param records: list of record type of objects
	:param symptoms: list of string - the updated symptoms list
	:param SYMPTOMS: list of string - the original symptoms list
	:param path: list of booleans - the current path to the node by True or False steps.
	:return: Node type of object - the root of the tree
	"""
	if not symptoms:
		leaf = set_illness(path, records, SYMPTOMS)
		node = Node(leaf)
		return node
	# append True to the right node's path in order to have the whole path in
	# in the end. Same to the left node
	root = Node(symptoms[0], _helper_build_tree(records, symptoms[1:], SYMPTOMS, path + [True]),
				_helper_build_tree(records, symptoms[1:], SYMPTOMS, path + [False]))
	return root


def check_exception1(records, symptoms):
	"""
	This function raises exceptions if needed, according to the conditions.
	:param records: list of record type of objects
	:param symptoms: list of string - the symptoms
	:return: None
	"""
	for sym in symptoms:
		if not type(sym) == str:
			raise TypeError(TypeError_1)
	for record in records:
		if not type(record) == Record:
			raise TypeError(TypeError_2)


def build_tree(records, symptoms):
	"""
	This function create a tree (object from type diagnoser), according to the records
	list and the symptoms list it receives. This function uses helper function
	which work recursievly. In addition this function raises exception when
	needed, according to check_exception1 function.
	:param records: list of record type of objects
	:param symptoms: list of string - the symptoms
	:return: diagnoser type of object - the tree
	"""
	check_exception1(records, symptoms)
	SYMPTOMS = symptoms[:]
	root = _helper_build_tree(records, symptoms, SYMPTOMS, [])
	return Diagnoser(root)


def check_exception2(records, symptoms, depth):
	"""
	This function raises exceptions if needed, according to the conditions.
	:param records: list of record type of objects
	:param symptoms: list of string - the symptoms
	:param depth: int - number of symptoms asked in the tree
	:return: None
	"""
	if not (len(symptoms) >= depth >= 0):
		raise ValueError(ValueError_1)
	lst = []
	for sym in symptoms:
		if sym not in lst:
			lst.append(sym)
		else:
			raise ValueError(ValueError_2)
	check_exception1(records, symptoms)


def optimal_tree(records, symptoms, depth):
	"""
	This function build trees using build_tree function, according to
	the symptoms and the records it recives, and returns the tree with
	the largest success rate. Calculates the rates by using  calculate_success_rate
	function.
	:param records: list of record type of objects
	:param symptoms: list of string - the symptoms
	:param depth:  int - number of symptoms asked in the tree
	:return: diagnoser type of object
	"""
	check_exception2(records, symptoms, depth)
	dict = {}
	for symps in combinations(symptoms, depth):
		diagnoser = build_tree(records, symps)
		success = diagnoser.calculate_success_rate(records)
		dict[diagnoser] = success
	lst = [(tree, rate) for tree, rate in dict.items()]
	lst.sort(key=lambda x: x[1])
	return lst[-1][0]

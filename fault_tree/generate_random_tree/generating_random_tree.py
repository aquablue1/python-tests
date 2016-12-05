# -*- coding:utf-8 -*-

import sys,re,os,random
import math
import copy

#generate gate_dataSource
def generating_gate_dataSource(ngate):
	gate_dataSource = []
	gate_dataSource.insert(0,'r1')
	for i in xrange(1,ngate):
		gate_dataSource.append('g'+'%d' % i)	
	#print str(gate_dataSource)
	return gate_dataSource

#generate event_dataSource
def generating_event_dataSource(nevent):
	event_dataSource = []
	for i in xrange(1,nevent+1):
		event_dataSource.append('e'+'%d' % i)
	#print str(event_dataSource)
	return event_dataSource

#add gates
def get_gate_dag(gate_dataSource,len_gate):
	gate_dag = {}	
	n = len_gate
	for gate in gate_dataSource:
		gate_num_children = random.randint(1,3)
		children = []
		while n - 1 and gate_num_children:
			children.append(gate_dataSource[len_gate-n+1])
			n = n - 1
			gate_num_children = gate_num_children - 1
		gate_dag[gate] = children
		#add logic
		gate_dag[gate].insert(0,random.choice(['&','|']))
	#print str(gate_dag)
	return gate_dag

def get_father_dataSource(gate_dag):
	copy_gate_dag = copy.deepcopy(gate_dag)
	father_dataSource = {}
	for gate in copy_gate_dag:
		copy_gate_dag[gate].remove(copy_gate_dag[gate][0])
		if len(copy_gate_dag[gate]) > 0:
			for element in copy_gate_dag[gate]:
				father = []
				father.append(gate)				
				father_dataSource[element] = father						
	#print str(father_dataSource)
	return father_dataSource

def found_ancestor(father_dataSource):
	for gate in father_dataSource:
		for element in father_dataSource[gate]:
			if element is not 'r1':
				for elementa in father_dataSource[element]:
					father_dataSource[gate].append(elementa)
				element = father_dataSource[element]
	#print str(father_dataSource)
	for ancestor in father_dataSource:
		father_dataSource[ancestor] = list(set(father_dataSource[ancestor]))		
	#print str(father_dataSource)
	return father_dataSource

#add events
def get_gate_event_dag(gate_dag,event_dataSource,len_event):
	gate_event_dag = copy.copy(gate_dag)
	n = len_event
	for gate in gate_dag:
		gate_num_children = random.randint(1,3)
		children = []
		while n and gate_num_children:
			children.append(event_dataSource[len_event-n])
			n = n - 1
			gate_num_children = gate_num_children - 1
		for child in children:
			gate_event_dag[gate].append(child)
	#print str(gate_event_dag)
	return gate_event_dag

#add repeated elements
def complete_tree(gate_event_dag,gate_dataSource,event_dataSource,ancestor):
	gate_children_dag = copy.copy(gate_event_dag)
	for gate in gate_event_dag:
		copy_event_dataSource = copy.copy(event_dataSource)
		while len(gate_children_dag[gate]) < 3:
			for element in gate_children_dag[gate]:
				if 'e' in element:
					copy_event_dataSource.remove(element)
			gate_children_dag[gate].append(random.choice(copy_event_dataSource))
	

	print gate_dataSource
	#print str(gate_children_dag)
	"""
	#repeated gates
	for gate in gate_children_dag:
		copy_gate_dataSource = copy.copy(gate_dataSource)
		repeated_gate_probability = random.random()
		if repeated_gate_probability > 0.7:		
			copy_gate_dataSource.remove(gate)
			#print str(copy_gate_dataSource)
			
			for element in gate_children_dag[gate]:
				if 'g' in element:
					copy_gate_dataSource.remove(element)	
			#print str(copy_gate_dataSource)
			
			if gate is not 'r1':
				for elements in ancestor[gate]:
					copy_gate_dataSource.remove(elements)
			#print str(copy_gate_dataSource)
			gate_children_dag[gate].append(random.choice(copy_gate_dataSource))
	"""
	#print str(gate_children_dag)
	return gate_children_dag

def generate_tree(ngate,nevent):
	gate_dataSource = generating_gate_dataSource(ngate)	
	event_dataSource = generating_event_dataSource(nevent)
	
	len_gate = len(gate_dataSource)
	len_event = len(event_dataSource)
	
	gate_dag = get_gate_dag(gate_dataSource,len_gate)
	father_dataSource = get_father_dataSource(gate_dag)
	ancestor = found_ancestor(father_dataSource)
	
	gate_event_dag = get_gate_event_dag(gate_dag,event_dataSource,len_event)
	
	gate_children_dag = complete_tree(gate_event_dag,gate_dataSource,event_dataSource,ancestor)
	

	print gate_children_dag
	return gate_children_dag


#=============================================================#
def fault_tree_level(gate_children_dag):
	begin_level = 0
	level = {}
	get_level(gate_children_dag,'r1',level, begin_level+1)

	#print str(level)
	return level

def get_level(gate_children_dag,root_name,level, next_level):
	#print root_name
	if next_level in level:
		level[next_level].append(root_name)
	else:
		level[next_level] = []
		level[next_level].append(root_name)

	children = []
	for each_child in gate_children_dag[root_name]:
		if 'g' in each_child:
			children.append(each_child)
		#print children
	#print gate_children_dag[root_name]
	#children = gate_children_dag[root_name][1:]
	for child in children:
		get_level(gate_children_dag,child,level,next_level+1)





def print_outfile(tree):
	for gate in tree:
		op = tree[gate][0]
		if gate is 'r1':
			print gate,'/*root*/ := (',
		else:
			print gate,' := (',
		times=0
		for children in tree[gate]:
			times=times+1
			if children is not '&' and children is not '|':
				if times is not 2:
					print op,children,
				else:
					print children,	
		
		print ')'


def enrich_tree(tree, gate_dataSource, level):


	print "tree in rich"+str(tree)
	for gate in tree:
		copy_gate_dataSource = copy.copy(gate_dataSource)
		#print "copy"+str(copy_gate_dataSource)
		target_node = random.choice(copy_gate_dataSource)
		repeated_gate_probability = random.random()
		source_node_level = 0
		target_node_level = 0

		for level_num in level:
			if target_node in level[level_num]:
				target_node_level = level_num
			if gate in level[level_num]:
				source_node_level = level_num
		#print str(target_node_level)+"   "+str(source_node_level)
		if target_node_level < source_node_level:
			continue
		if repeated_gate_probability > 0.7:		
			copy_gate_dataSource.remove(gate)
		#print str(copy_gate_dataSource)										
			for element in tree[gate]:														
				if 'g' in element:												
					copy_gate_dataSource.remove(element)	
				#print str(copy_gate_dataSource)
			if gate is not 'r1':
				for elements in ancestor[gate]:
					copy_gate_dataSource.remove(elements)	
			#print str(copy_gate_dataSource)
			#tree[gate].append(random.choice(copy_gate_dataSource))
			print "add "+str(target_node)+" to "+ str(gate)
			print str(target_node_level)+"   "+str(source_node_level)
			tree[gate].append(target_node)
	return tree
	"""
	#print str(gate_children_dag)
																						
	return gate_children_dag
	def generate_tree(ngate,nevent)
	gate_dataSource = generating_gate_dataSource(ngate)	
	event_dataSource = generating_event_dataSource(nevent)
	len_gate = len(gate_dataSource)
	len_event = len(event_dataSource)								
	gate_dag = get_gate_dag(gate_dataSource,len_gate)
	father_dataSource = get_father_dataSource(gate_dag)
	ancestor = found_ancestor(father_dataSource)
	gate_event_dag = get_gate_event_dag(gate_dag,event_dataSource,len_event)
	gate_children_dag = complete_tree(gate_event_dag,gate_dataSource,event_dataSource,ancestor)
	"""





if __name__ == "__main__":	

	ngate = 80
	nevent = 100
	
	gate_dataSource = generating_gate_dataSource(ngate)
	gate_dag = get_gate_dag(gate_dataSource,len(gate_dataSource))
	ancestor = found_ancestor(get_father_dataSource(gate_dag))
	tree = generate_tree(ngate,nevent)
	print tree
	#print "tree"
	level = fault_tree_level(tree)
	print level
	final_tree = enrich_tree(tree,gate_dataSource,level)
	print final_tree
	#print tree
	#print_outfile(tree)
	
	
	
	
	
	

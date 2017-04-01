"""
Copyright 2011 Wissarut Yuttachai, Pratkasem Vesarach, Poompat Saengudomlert
======================================================================
    This file is part of WDMPlanner.

    WDMPlanner is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WDMPlanner is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with WDMPlanner.  If not, see <http://www.gnu.org/licenses/>.
======================================================================
"""
#------------------------------------------------------------------------------
# Program: Dijkstra algorithm
# Description: Calculate the shortest path from a source node to all nodes
# Author: Pratkasem V.
# Reference: http://en.wikipedia.org/wiki/Dijkstra's_algorithm
# Version:	- 24/01/11	- First release
#			- 25/01/11	- Create the output ->"short_info"
#			- 28/01/11	- Add the connectivity checking -> "connect_search"
#           - 31/01/11  - Add the choice to choose "link_list" or "node_list"
#           - 11/02/11  - Add the source node availability checking to the
#                         "connect_search"
#------------------------------------------------------------------------------
# Parameters Description
#
# connect_mat: Connectivity matrix
# src_node: Source node
# des_node: Destination node
# list_cri: List criteria: '1': link_list, '2': node_list. Default is '1'
#------------------------------------------------------------------------------

def dijkstra(connect_mat, src_node, des_node, list_cri = 1):

	# The matrix below is for testing only
	# connect_mat = {1:{2:2,6:3},2:{1:2,6:5,3:3},3:{2:3,4:1,5:2},4:{3:1,5:4},5:{3:2,4:4,6:8},6:{1:3,2:5,5:8}}
	
	# Check whether the destination node can be connected or not.
	# Default is the Breadth-first search algorithm
	path_found_ind = connect_search(connect_mat, src_node, des_node, 1)

	if path_found_ind == 1: # Path is possible
	
		# Initiate the solution matrix
		dijkstra_sol_mat = {}
	
		# Initiate the distance and previous node
		for	i in connect_mat.keys():
			dijkstra_sol_mat.update({i:{'dist':float('inf'),'previous':0}})
	
		# Distance of the source node is zero
		dijkstra_sol_mat[src_node]['dist'] = 0

		# Initiate the uncheck set (i.e. nodes)
		uncheck_set = set(connect_mat.keys())
	
		# The main loop. The process keeps going the uncheck set is empty
		while len(uncheck_set) != 0:
			# Create the current distance matrix based on the uncheck set
			distance_temp = {}
			for i in uncheck_set:
				distance_temp.update({i:dijkstra_sol_mat[i]['dist']})
		
			# Determine the node to be updated
			update_node = []
			for j in distance_temp.keys():
				if distance_temp[j] == min(distance_temp.values()):
					update_node = j
		
			# Remove the updated node from the uncheck nodes set
			uncheck_set.remove(update_node)
	
			# Update the distance and the previous node	keys
			for k in connect_mat[update_node].keys():
				if k in uncheck_set:
					distance_update = dijkstra_sol_mat[update_node]['dist'] +\
								  connect_mat[update_node][k]
					if distance_update < dijkstra_sol_mat[k]['dist']:
						dijkstra_sol_mat[k]['dist'] = distance_update
						dijkstra_sol_mat[k]['previous'] = update_node

		# Create the list of nodes in the shortest path
		node_list = [des_node]
		src_found = 0
		while src_found != 1:
			node_list.append(dijkstra_sol_mat[node_list[-1]]['previous'])
			if node_list[-1] == src_node:
				src_found = 1
		# List starts from the source node
		node_list.reverse()

		# To give 'link_list' or 'node_list'		
		if list_cri == 1:
			link_list = node2link(node_list)
			short_info = {'link_list': link_list,\
						  'dist': dijkstra_sol_mat[des_node]['dist']}
		else:
			short_info = {'node_list': node_list,\
						  'dist': dijkstra_sol_mat[des_node]['dist']}
	
	# Path is not possible
	else:
		short_info = {'link_list':[],'dist':[]}

	# Return the short_info as an output
	return short_info

#------------------------------------------------------------------------------
# Program: Search algorithm
# Description: Check the connectivity between the source and the destination
#              node. There are two algorithm: Breadth-first search and Depth
#			   first search.
# Author: Pratkasem V.
# Version:	- 27/01/11	- First release
#------------------------------------------------------------------------------
# Parameters Description
#
# connect_mat: Connectivity matrix
# src_node: Source node
# des_node: Destination node
# search_cri: Search criteria. 1: Breadth-first, 2: Depth-first
#------------------------------------------------------------------------------ 
def connect_search(connect_mat, src_node, des_node, search_cri):

	# Initiate the connectivity indicator. '1': Path found '0': Path not found
	connect_ind = 0	

	# Initiate the close and open list
	open_list = []
	close_list = []

	# Add the source node to the open_list
	open_list.append(src_node)

    # Check whether source node presents in the connect_mat
	if src_node in connect_mat.keys():
		# Loop until the destination node is found of the open_list is empty
		while open_list:
		
			# Search for the nodes that are connected to the first node in the open
			# list. Then, remove the nodes that are already in open/close list.
			temp_node = connect_mat[open_list[0]].keys()
		
			for i in set(open_list)|set(close_list):
				if i in temp_node:
					temp_node.remove(i)

			# Remove the recently search node from the open_list and put it into
			# the close_list
			close_list.append(open_list[0])
			open_list.remove(open_list[0])

			# Add the temp_node to the open_list according to the search criteria
			if search_cri == 1:
				for i in temp_node: open_list.append(i)
			elif search_cri == 2:
				for i in temp_node: open_list.insert(0,i)
			else:
				print 'ERROR!!!'

			# Check whether the destination node is already in the open_list
			if des_node in open_list:
				connect_ind = 1; break

	return connect_ind


#------------------------------------------------------------------------------
# Program: Node to link conversion
# Description: Convert from a node list to a link list
# Author: Pratkasem V.
# Version:	- 31/01/11	- First release
#------------------------------------------------------------------------------
# Parameters Description
#
# node_list: list of nodes in a path
# link_list: list of link in a path
#------------------------------------------------------------------------------ 
def node2link(node_list):

	# Initiate link list
	link_list = []
	# Convert from a list of node to a list of link
	for i in range(len(node_list)-1):
		link_list.append([node_list[i], node_list[i+1]])

	return link_list

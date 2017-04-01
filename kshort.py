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
# Program: K-Shortest path algorithm
# Description: Calculate the k-shortest path (i.e. if any) from a source node
#			   to the destination node
# Author: Pratkasem V.
# Reference: "Finding the k shortest loopless paths in a network"
# Version:	- 31/01/11 - First release
#           - 07/02/11 - Fix the wrong list_cri selection
#                      - Add the k = 1 possibility checking
#------------------------------------------------------------------------------
# Parameters Description
#
# connect_mat: Connectivity matrix
# src_node: Source node
# des_node: Destination node
# k: number of path. Note: The program will return only possible k paths
# list_cri: List criteria. '1': link list format, '2': node list format.
#			Default is '1'
#------------------------------------------------------------------------------
import dijkstra
import copy

def kshort(connect_mat, src_node, des_node, k, list_cri = 1):
	
	# Create the k shortest path list (i.e. dictionary)
	kpath_list = {}

	# Determine the first shortest path k = 1
	k_1_path = dijkstra.dijkstra(connect_mat, src_node, des_node, 2)
	
	# If the first shortest path cannot be found, return the blank kpath_list
	if k_1_path['dist'] != []: 
		kpath_list.update({1:k_1_path})

		# Find the remaining k
		# Create the list of possible k shortest path
		possible_kpath_list = {}
	
		for i in range(2,k+1,1):
		
			# Check whether it is possible to find k = i. If not possible
			# terminate the loop and return the best found solution
			if i-1 in kpath_list.keys():
			
				# Determine k-1 node list (i.e. exclude the destination node)
				pre_k_node_list = kpath_list[i-1]['node_list'][:-1]
			
				# Loop j = 1, 2,..., Q(k-1)
				for j in range(len(pre_k_node_list)):
				
					# Determine the root of current loop
					root = pre_k_node_list[:j+1]
				
					# Initiate the list of links to be removed
					remove_link_list = []

					for q in kpath_list.keys():
	
						# Check whether the root is coincide with the subpath in
						# kpath_list
						if root == kpath_list[q]['node_list'][:j+1]:
						
							# Determine the link to be temporary removed
							remove_link = [root[-1], kpath_list[q]['node_list'][j+1]]
						
							# If the link is not already in the list, add it	
							if remove_link not in remove_link_list:
								remove_link_list.append(remove_link)
				
					# Determine the spur of current loop
				
					# Create temporary connect_mat
					temp_connect_mat = copy.deepcopy(connect_mat)
				
					# Remove links from the temp_connect_mat
					for q in remove_link_list:
						del(temp_connect_mat[q[0]][q[1]])
				
					# Remove nodes in the root from the temp_connect_mat (i.e. except
					# the last node).
					if len(root) > 1:
						for q in root[:-1]:
							del(temp_connect_mat[q])
							for z in temp_connect_mat.keys():
								if q in temp_connect_mat[z].keys():
									del(temp_connect_mat[z][q])
				
					# Determine the path from j to the destination node
					spur = dijkstra.dijkstra(temp_connect_mat, root[-1], des_node, 2)
					if spur['dist'] != []:	
						# Create temp_k_path: Combine root and spur
						temp_k_path = root + spur['node_list'][1:]

						# Determine the distance of the temp_k_path
						temp_k_dist = 0
						for q in range(len(temp_k_path)-1):
							temp_k_dist = temp_k_dist + connect_mat[temp_k_path[q]]\
									  	[temp_k_path[q+1]]	
				
						# If not already exists, add the temp_k_path to the
						# possible_kpath_list
						if str(temp_k_path) not in possible_kpath_list.keys():
							possible_kpath_list.update({str(temp_k_path):temp_k_dist})
			
				# Determine the current k shortest path
				for j in possible_kpath_list.keys():
					if possible_kpath_list[j] == min(possible_kpath_list.values()):
						kpath_list.update({i:{'node_list':eval(j),\
										  	  'dist':possible_kpath_list[j]}})
						del(possible_kpath_list[j])
						break
			else:
				break
	
		# Return in node_list format of link_list format
		if list_cri == 2:
			return kpath_list
	
		else:
			# Use the link list format
			kpath_list_link = {}
			for i in kpath_list.keys():
				kpath_list_link.update({i:{'dist':kpath_list[i]['dist'],\
				'link_list':dijkstra.node2link(kpath_list[i]['node_list'])}})
		
			return kpath_list_link
	else:
		return k_1_path

#connect_mat = {'a':{'b':2,'f':3},'b':{'a':2,'f':5,'c':3},'c':{'b':3,'d':1,'e':2},'d':{'c':1,'e':4},\
#              'e':{'c':2,'d':4,'f':8},'f':{'a':3,'b':5,'e':8}}
#print kshort(connect_mat, 'a', 'd', 3, 1)

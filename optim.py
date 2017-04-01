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
# Import the related module
from pulp import *
import kshort

def opt_wave(connect_mat, k_num, traffic_mat, wave_num, fiber_num, slot_num, obj_cri=1, traf_split=2):

    """
    Function:

    This function computes the minimum number of lightpaths to support
    all traffic demands. The network is based on the O-E-O network.

    Arguments:

    connect_mat: The connectivity matrix.
    k_num: The number of of required shortest paths.
    traffic_mat: The traffic demand matrix. The required bandwidth is
                 represented in number of traffic slot.
    wave_num: The maximum number of wavelength channels per fiber.
    fiber_num: The maximum number of fiber per physical link.
    slot_num: The number of traffic slots per wavelengths
    obj_cri: The objective function criterion. "1": Minimize the number of
             required wavelength channels. "2": Maximize the number of
             supported traffic demands. "3": Minimize the additional link
             capacity.
    traf_split: Traffic splitting indicator. "1": Traffic splitting is
                allowed. "2": No traffic slitting.
    
    Revision: 07.03.11

    Author: Pratkasem V.
    """
    
    # !!!These arguments are for function testing only!!!
    #connect_mat = {'s1':{'s2':2,'s6':3},'s2':{'s1':2,'s6':5,'s3':3},'s3':{'s2':3,'s4':1,'s5':2},'s4':{'s3':1,'s5':4},\
    #               's5':{'s3':2,'s4':4,'s6':8},'s6':{'s1':3,'s2':5,'s5':8}}
    #traffic_mat = {'s1':{'s3':15,'s4':10,'s5':2},'s2':{'s3':2,'s6':6},'s4':{'s1':3}}
    #k_num = 3
    #wave_num = 2
    #fiber_num = 1
    #slot_num = 4
    #obj_cri = 2
    #traf_split = 1

    #-------------------------------------------------------------------------
    #                     INITIATE THE RELATED ENTITIES
    #-------------------------------------------------------------------------
    
    # Create the set of shortest paths of all source-destination pairs
    # K_paths_set['(s,d)'][k_ind]['link_list'] -> List of links in path #k_ind
    # K_paths_set['(s,d)'][k_ind]['dist'] -> Distance of path #k_ind

    K_paths_set = {}
    for i in traffic_mat.keys():
        for j in traffic_mat[i].keys():
            K_paths_temp = kshort.kshort(connect_mat, i, j, k_num, 1)
            if isinstance(i, basestring) and isinstance(j, basestring):
                K_paths_set.update({'(' + i + ',' + j +')': K_paths_temp})
            elif isinstance(i, int) and isinstance(j, int):
                K_paths_set.update({str.replace(str((i,j)), ' ',''): K_paths_temp})
            else:
                print 'Please input consistance format'
    
    # Convert the 'link_list' into string
    for i in K_paths_set.keys():
        for j in K_paths_set[i].keys():
            for q in range(len(K_paths_set[i][j]['link_list'])):
                temp_q = K_paths_set[i][j]['link_list'][q]
                temp_q_str = '(' + str(temp_q[0]) + ',' + str(temp_q[1]) + ')'
                K_paths_set[i][j]['link_list'][q] = temp_q_str
   
    # Create the Link_paths_set. It is used to determine the (s,d) and k
    # indices of paths that use physical link (m,n)
    
    Link_paths_set = {}
    for i in K_paths_set.keys():
        for j in K_paths_set[i].keys():
            for q in K_paths_set[i][j]['link_list']:
                if q not in Link_paths_set.keys():
                    Link_paths_set.update({q:{}})
    
    # Insert the values into Link_paths_set
    for i in K_paths_set.keys():
        for j in K_paths_set[i].keys():
            for q in K_paths_set[i][j]['link_list']:
                if i not in Link_paths_set[q].keys():
                    Link_paths_set[q].update({i:[str(j)]})
                elif j not in Link_paths_set[q][i]:
                    Link_paths_set[q][i].append(str(j))

    # Generate the sets
    # S_set: Set of source-destination pairs with nonzero traffic
    # E_set: Set of directed physical links
    # K_set: Set of k index (i.e. shortest path indices)
	
    S_set = {}
    for i in traffic_mat.keys():
        for j in traffic_mat[i].keys():
            if isinstance(i, basestring) and isinstance(j, basestring):
                S_set.update({'(' + i + ',' + j + ')': traffic_mat[i][j]})
            elif isinstance(i, int) and isinstance(j, int):
                S_set.update({str.replace(str((i,j)), ' ',''):traffic_mat[i][j]})
            else:
                print 'Please input consistent format'

    E_set = []
    for i in connect_mat.keys():
        for j in connect_mat[i].keys():
            if isinstance(i, basestring) and isinstance(j, basestring):
                E_set.append('(' + i + ',' + j + ')')
            elif isinstance(i, int) and isinstance(j, int):
                E_set.append(str.replace(str((i,j)), ' ', ''))
            else:
                print 'Please input consistent format'

    K_set = [str(i) for i in range(1, k_num+1, 1)]

	# Generate dictionaries of the decision variables
    # b_(s,d)_k: The bandwidth allocated to route k for source-destination pair
    #            (s,d). They have discrete values
    # v_(s,d)_k: Indicator that indicates whether b_(s,d)_k is used or not.
    #            It is binary.
    # c_(m,n): The number of wavelength channels in physical link (m,n)
    # d_(m,n): The number of additional wavelength channels in physical link
    #          (m,n)

    
    b_vars = LpVariable.dicts('b', (S_set, K_set), lowBound = 0,\
             upBound = None, cat = 'Integer')
    
    v_vars = LpVariable.dicts('v', (S_set, K_set), lowBound = 0,\
             upBound = None, cat = 'Binary')

    c_vars = LpVariable.dicts('c', E_set, lowBound = 0,\
             upBound = None, cat = 'Integer')

    d_vars = LpVariable.dicts('d', E_set, lowBound = 0,\
             upBound = None, cat = 'Integer')
    #-------------------------------------------------------------------------
    #               CREATE THE PROBLEM AND THE OBJECTIVE FUNCTION
    #-------------------------------------------------------------------------

    # Create the 'prob' variable to contain the problem data
    # Add the objective function to the problem

    if obj_cri == 1: # Minimize resource
        prob = LpProblem("The lightpath minimization problem", LpMinimize)
        prob += lpSum([c_vars[i] for i in E_set])
    elif obj_cri == 2: # Maximize supported traffic
        prob = LpProblem("The supported bandwidth maximization problem",
                         LpMaximize)
        prob += lpSum([b_vars[i] for i in S_set])
    elif obj_cri == 3: # Minimize the additional resource
        prob = LpProblem("The additional resource minimization problem",
                         LpMinimize)
        prob += lpSum([d_vars[i] for i in E_set])
    else:
        print "Please input a correct objective function criterion!"

    #-------------------------------------------------------------------------
    #                      CONSTRAINT: TRAFFIC DEMAND
    #-------------------------------------------------------------------------

    if obj_cri == 1 or obj_cri == 3: # Minimize: resources/additional resources
        for i in S_set.keys():
            prob += lpSum([b_vars[i][q] for q in K_set]) == S_set[i],\
                    "traf_const" + i
    elif obj_cri == 2: # Maximize supported traffic
        for i in S_set.keys():
            prob += lpSum([b_vars[i][q] for q in K_set]) <= S_set[i],\
                    "traf_const" + i
    else:
        print "Please input the correct objective function criterion!" 

    #-------------------------------------------------------------------------
    #           CONSTRAINT: WAVELENGTH CHANNELS IN PHYSICAL LINKS
    #-------------------------------------------------------------------------
    for i in E_set:
        if i in Link_paths_set.keys():
            link = i.split(',')                   #revised on March 12, 2011
            node1 = link[0].split('(')[1]         #rev.
            node2 = link[1].split(')')[0]         #rev.
            if obj_cri == 1 or obj_cri == 2: # Min. resources/Max. Traf.  
                prob += lpSum([(1.0/slot_num[node1][node2]) * b_vars[j][q]\
                for j in Link_paths_set[i].keys()\
                for q in Link_paths_set[i][j]]) <= c_vars[i], "wave_chan" + i #rev.
            elif obj_cri == 3: # Minimize: additional resources
                prob += lpSum([(1.0/slot_num[node1][node2]) * b_vars[j][q]\
                for j in Link_paths_set[i].keys()\
                for q in Link_paths_set[i][j]]) <= c_vars[i] + d_vars[i],\
                "wave_chan" + i #rev.

    #-------------------------------------------------------------------------
    #                    CONSTRAINT: WAVELENGTH CAPACITY
    #-------------------------------------------------------------------------

    for i in E_set:
        link = i.split(',')                   #revised on March 12, 2011
        node1 = link[0].split('(')[1]         #rev.
        node2 = link[1].split(')')[0]         #rev.
        prob += c_vars[i] <= wave_num[node1][node2] * fiber_num[node1][node2], "wave_cap" + i

    #-------------------------------------------------------------------------
    #                   CONSTRAINT: NO TRAFFIC SPLITTING
    #-------------------------------------------------------------------------

    if traf_split == 2:
        for i in S_set:
            for j in K_set:
                prob += b_vars[i][j]*(1.0/S_set[i]) <= v_vars[i][j],\
                        "b_indicator_" + i + "_" + j

        for i in S_set:
            prob += lpSum(v_vars[i][j] for j in K_set) <= 1,\
                    "no_split_" + i  
    #-------------------------------------------------------------------------
    #                   CREATE LP FILE AND SOLVE THE PROBLEM
    #-------------------------------------------------------------------------

    prob.writeLP("optim_lp.lp")
    prob.solve(GLPK())

    #-------------------------------------------------------------------------
    #                     PRINT THE SOLUTION TO THE SCREEN
    #-------------------------------------------------------------------------
   
    # The optimization solver result 
    print "Status: ", LpStatus[prob.status]
    
    # The objective value
    if obj_cri == 1: # Minimize resource
        print "The total number of wavelength channels: ",\
              value(prob.objective)
    elif obj_cri == 2: # Maximize supported traffic
        print "The amount of supported traffic: ", value(prob.objective)
    elif obj_cri == 3: # Minimize additional resource
        print "The amount of additional wavelength channels: ",\
              value(prob.objective)
    else: 
        print "Please input a correct objective function criterion!"

    #-------------------------------------------------------------------------
    #                           CREATE THE OUTPUTS
    #-------------------------------------------------------------------------

    # path_allo_bw['(s,d)'][k]['link_list']: List of links in path k of
    # source-destination pair (s,d)
    # path_allo_bw['(s,d)'][k]['bandwidth']: Allocated bandwidth in path k of
    # source-destination pair (s,d)
    # wave_link['(m,n)']: Number of allocated wavelength in physical link
    # (m,n)
    # add_wave_link['(m,n)']: Number of additional wavelength in physical link
    # (m,n)

    paths_allo_bw = {}
    wave_link = {}
    add_wave_link = {}

    for v in prob.variables():
        if v.varValue != 0:
            #var_name = v.name.replace('_',' '); var_name = var_name.split()
            var_name = v.name.split('_',1) #revised. WISSARUT
            if var_name[0] == 'b':
                v_name = var_name[1].rsplit('_',1) #revised. WISSARUT
                var_name = [var_name[0],v_name[0].replace('_',' '),v_name[1]] #added
            if var_name[0] == 'b':
                k_temp = eval(var_name[2])
                link_list_temp = K_paths_set[var_name[1]][k_temp]['link_list']
                bw_temp = v.varValue
                if var_name[1] not in paths_allo_bw.keys():
                    paths_allo_bw.update({var_name[1]:{k_temp:{'link_list':\
                    link_list_temp, 'bandwidth':v.varValue}}})
                elif var_name[1] in paths_allo_bw.keys() and\
                     k_temp not in paths_allo_bw[var_name[1]].keys():
                     paths_allo_bw[var_name[1]].update({k_temp:{'link_list':\
                     link_list_temp, 'bandwidth':v.varValue}})
            elif var_name[0] == 'c':
                wave_link.update({var_name[1]:v.varValue})
            elif var_name[0] == 'd':
                add_wave_link.update({var_name[1]:v.varValue})

    return paths_allo_bw, wave_link, add_wave_link, value(prob.objective)
 
#-----------------------------------------------------------------------------
#                     FOR COMMAND PROMPT PROGRAM CALLING
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    opt_wave()

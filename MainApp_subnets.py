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
from __future__ import division
from Tkinter import *
from random import sample
import tkMessageBox, tkFileDialog, tkSimpleDialog
import pickle
import operator
# local functions
import kshort
import optim
import math
import random
from pulp import*
import itertools
from MenuBar import *
from StatusBar import *
from EditDialog import *
from InfoDialog import *
from ScrolledCanvas import *
from ScrolledFrame import *


class MainApp:
    # -----------------------------constructor------------------------
    def __init__(self, parent):
        self.myParent = parent
        self.myParent.geometry("1200x700")
        ### Topmost frame is called myContainer1
        self.myContainer1 = Frame(parent)  ###
        self.myContainer1.pack(side=LEFT, expand=NO, fill=BOTH)
        # control frame
        self.control_frame = Frame(self.myContainer1)  ###
        self.control_frame.pack(side=TOP, expand=NO)
        # padx=10, pady=5, ipadx=5, ipady=5
        # show frame
        self.show_frame = Frame(self.myContainer1)  ###
        self.show_frame.pack(side=TOP, expand=YES, fill=BOTH)
        # status frame
        self.status_frame = Frame(self.myContainer1)  ###
        self.status_frame.pack(side=BOTTOM, expand=YES, fill=X)
        # -------------------------------------------------
        self.prev_item = None
        self.sel_item = None
        self.prev_sel_item = None
        self.prev_sel_type = None
        self.prev_type = None
        self.sel_type = None
        self.prev_x = None
        self.prev_y = None
        self.node_list = {}
        self.edge_list = {}
        self.topo = {}
        self.node_pos = {}
        self.do = None
        self.status_mode = "Move node"
        self.paths = None
        self.top_info1 = None
        # ---------------- NEW VAR ----------------------
        self.edge_simp_list = {}
        self.graph = {}
        self.node_cor = {}
        self.first_node = None
        self.first_node_cor = None
        self.slope = {}
        self.set_border_nodes = []
        self.state = "Showing"
        # ---------------------------------------------------
        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = ''  # couldn't figure out how this works
        # options['filetypes'] = [('all files', '*'), ('text files', '.txt')]
        options['filetypes'] = [('all files', '*'), ('workspace files', '.wp')]
        # options['initialdir'] = 'C:\\'
        options['initialfile'] = ''
        options['parent'] = self.myParent
        options['title'] = 'Open File'
        # --------------------optimization parameters---------
        self.k_num = 2
        self.default_wave_num = 2
        self.default_slot_num = 4
        self.default_fiber_num = 1
        self.default_workcap_num = 100
        self.traffic_mat = None
        self.wave_num = {}
        self.slot_num = {}
        self.workcap_num ={}
        self.fiber_num = {}
        self.paths_allo_bw = None
        self.wave_link = None
        self.add_wave_link = None
        self.wave_link_use = {}
        self.draw_addwave_key = []
        self.add_legend_key = []
        self.obj_cri = 1  # 1=minimize resource,#2=maximize supported traffic,#3=Minimize the additional link capacity.
        self.obj_value = None
        self.trf_split = 0  # 1=splitted,#2=not splitted.
        self.var_showpath = 1  # added 25AUG2011 #path selection
        self.sdlist = {}  # source:destination
        self.source = []  # added 14AUG2011 #source sequence
        self.destination = []
        self.drawopt_link_key = []
        self.drawopt_node_key = []
        self.index = 0
        # ---------------- FRAME IN info_frame --------------
        self.frame_opt = None
        self.toolbar_opt = None
        self.radio_opt = None
        self.frame_link_info_topmost = None
        self.frame_link_info_top = None
        self.frame_link_info_bottom = None
        self.toolbar_link_edit = None
        self.toolbar_check_cycle = None
        self.frame_link_edit_top = None
        self.frame_link_edit_bottom = None
        self.top_opt1 = None
        self.top_opt2 = None
        self.info_canvas = None
        # ---------------shortest path parameters------------
        self.draw_path_key = []
        # ---------------------------------------------------
        self.defaultLineColor = "black"
        self.defaultNodeColor = "cyan"
        self.blue = "#0000FF"
        self.royalblue = "#4169E1"
        self.deepskyblue = "#00BFFF"
        # -------------------- MENU ------------------------#
        menu = MenuBar(self.myParent, self.callback_clear, self.callback_open, \
                       self.callback_close, self.callback_demo, self.callback_showtrf)
        # -------------------TOOLBAR------------------------#
        # create a toolbar
        self.toolbar = Frame(self.control_frame, borderwidth=2, relief=RIDGE)
        self.b1 = Button(self.toolbar, text="create node", width=10, command=self.callback_create_node, relief=GROOVE)
        self.b1.pack(side=LEFT, padx=2, pady=2)
        self.b2 = Button(self.toolbar, text="create edge", width=10, command=self.callback_create_edge, relief=GROOVE)
        self.b2.pack(side=LEFT, padx=2, pady=2)
        self.b3 = Button(self.toolbar, text="remove node/edge", width=16, command=self.callback_remove, relief=GROOVE)
        self.b3.pack(side=LEFT, padx=2, pady=2)
        self.b4 = Button(self.toolbar, text="edit", width=10, command=self.callback_edit, relief=GROOVE)
        self.b4.pack(side=LEFT, padx=2, pady=2)
        self.b5 = Button(self.toolbar, text="open", width=10, command=self.callback_open, relief=GROOVE)
        self.b5.pack(side=LEFT, padx=2, pady=2)
        self.b6 = Button(self.toolbar, text="save", width=10, command=self.callback_save, relief=GROOVE)
        self.b6.pack(side=LEFT, padx=2, pady=2)
        self.b7 = Button(self.toolbar, text="find border", width=10, command=self.callback_find_border, relief=GROOVE)
        self.b7.pack(side=LEFT, padx=2, pady=2)
        self.b8 = Button(self.toolbar, text="background", width=10, command=self.callback_background, relief=GROOVE)
        self.b8.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack(side=TOP, fill=X)
        # -----------------ALGORITHM BAR-------------------#
        # create a toolbar
        self.functionbar = Frame(self.control_frame, borderwidth=2, relief=RIDGE)
        self.f1 = Button(self.functionbar, text="shortest path", width=10, command=self.callback_shortestPath,
                         relief=GROOVE)
        self.f1.pack(side=LEFT, padx=2, pady=2)
        self.f2 = Button(self.functionbar, text="optimize", width=10, command=self.callback_opt, relief=GROOVE)
        self.f2.pack(side=LEFT, padx=2, pady=2)
        self.f3 = Button(self.functionbar, text="partitioning graph", width=10, command=self.callback_partitioning,
                         relief=GROOVE)
        self.f3.pack(side=LEFT, padx=2, pady=2)
        self.f4 = Button(self.functionbar, text="random nodes", width=10, command=self.callback_rand, relief=GROOVE)
        self.f4.pack(side=LEFT, padx=2, pady=2)
        self.f5 = Button(self.functionbar, text="ring protect", width=10, command=self.callback_ring_prot, relief=GROOVE)
        self.f5.pack(side=LEFT, padx=2, pady=2)
        self.functionbar.pack(side=TOP, fill=X)
        # ------------------TOPO----------------------------#
        self.topo_frame = Frame(self.show_frame, borderwidth=5, relief=RIDGE)
        self.topo_frame.pack(side=LEFT, expand=YES, fill=BOTH)
        # ------------------INFO----------------------------#
        self.info_frame = Frame(self.show_frame, borderwidth=5, relief=RIDGE)
        self.info_frame.pack(side=RIGHT, expand=YES, fill=BOTH)
        # ---------------------------------#
        self.info_frame_top = Frame(self.info_frame, borderwidth=1, relief=RIDGE)
        self.info_frame_top.pack(side=TOP, expand=YES, fill=BOTH)
        self.scrollframe_info_top = ScrolledFrame(self.info_frame_top, 350, 280)  # Scrolled top info frame WxH
        self.info_frame_bottom = Frame(self.info_frame, borderwidth=1, relief=RIDGE)
        self.info_frame_bottom.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.scrollframe_info_bottom = ScrolledFrame(self.info_frame_bottom, 350, 280)  # Scrolled bottom info frame
        self.scrollframe_info_top.updateScrollers()
        self.scrollframe_info_bottom.updateScrollers()
        # -------------------CANVAS------------------------#
        # create a canvas widget as a child to the root window
        self.canvas = Canvas(self.topo_frame, borderwidth=5, \
                             relief=RIDGE, scrollregion=(0, 0, 1000, 800), width=780, height=500)
        ScrolledCanvas(self.topo_frame, self.canvas)
        # bind a left-mouse click event
        # canvas.bind("<Button-1>", callback_press)
        self.canvas.bind("<Button-1>", self.callback_select)
        # bind a left-mouse release event
        self.canvas.bind("<ButtonRelease-1>", self.callback_release)
        # the pack method on this widget; make itself visible
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        # -------------------- STATUS BAR ------------------#
        self.status = StatusBar(self.status_frame)
        self.status.pack(side=BOTTOM, expand=NO, fill=X)
        self.status.set('welcome')
        # ------------------------------background-----------------------------
        self.background_img = PhotoImage(file='map_full_gray.gif')
        self.bg = self.canvas.create_image(500, 400, image=self.background_img, state = NORMAL)

    def callback_ring_prot(self):
        self.reset()
        #self.reset_frame_info_bottom()
        L = {}
        print 'this is ring technique'
        print 'edge',self.edge_list
        print 'node',self.node_list
        for e in self.edge_list.keys():
            n1= self.edge_list[e]['fromto'][0]
            n2= self.edge_list[e]['fromto'][1]
            #print 'workcap',n1,n2,self.workcap_num[n1][n2]
            L[(n1, n2)] = self.workcap_num['A' + str(n1)]['A' + str(n2)]
            L[(n2, n1)] = self.workcap_num['A' + str(n2)]['A' + str(n1)]
            # print 'workcap',n1,n2,':',self.workcap_num['A'+str(n1)]['A'+str(n2)]
            # print 'workcap',n2, n1, ':', self.workcap_num['A' + str(n2)]['A' + str(n1)]
        #print L
        NODE = []
        # loop with n taking L values to get full NODE one by one
        for n in L:
            n1 = n[0]
            n2 = n[1]
            if n1 not in NODE:
                NODE = NODE + [n1]
            if n2 not in NODE:
                NODE = NODE + [n2]
        No_Node = len(NODE)
        No_NodePair = int(No_Node * (No_Node - 1) / 2)
        S_DID = list(range(0, No_NodePair))
        print 'S_DID',S_DID

        Set_Links = []
        for l in L:
            Set_Links.append(l)
        Link_ID = range(0, len(Set_Links)/2)
        print 'Link_ID',Link_ID
        ##finding all candidate paths
        graph = {}
        graph = graph.fromkeys(NODE, [])
        print(graph)
        for n in L:
            n1 = n[0]
            n2 = n[1]
            A = graph[n1]
            A = A + [n2]
            A.sort()
            graph[n1] = A
            # print(graph)

        print 'graph', (graph)
        ##find all cycle
        ori_graph = graph
        print "Graph = ", ori_graph

        # -----------------------------------------------------------------------------------------------------------------------
        def find_repeated_cycle(graph, start, end, cycle, repeated_cycles):
            cycle = cycle + [start]
            if start == end:
                if len(cycle) >= 4:
                    repeated_cycles.append(cycle)
                    return repeated_cycles
                if len(cycle) == 1:
                    for node in graph[start]:
                        if node not in cycle:
                            find_repeated_cycle(graph, node, end, cycle, repeated_cycles)
                cycle.pop()
                return repeated_cycles
            for node in graph[start]:
                if node not in cycle:
                    find_repeated_cycle(graph, node, end, cycle, repeated_cycles)
                if node == end:
                    find_repeated_cycle(graph, node, end, cycle, repeated_cycles)
            return repeated_cycles

        # -----------------------------------------------------------------------------------------------------------------------

        def remove_cycles(vertex):
            A_filter = []
            A = find_repeated_cycle(ori_graph, vertex, vertex, [], [])
            for i in A:
                temp = 1
                if len(A_filter) == 0:
                    A_filter.append(i)
                for j in A_filter:
                    if len(i) == len(j) and len(list(set(i) & set(j))) == len(i) - 1:
                        A_filter = A_filter
                        temp = 0
                    if len(i) != len(j):
                        temp = temp
                if temp == 1:
                    A_filter.append(i)
            return A_filter

        # -----------------------------------------------------------------------------------------------------------------------
        def del_node(vertex, NODE):
            NODE.remove(vertex)
            del ori_graph[vertex]
            for key, item in ori_graph.items():
                if item.count(vertex) > 0:
                    for j in item:
                        if j == vertex:
                            item.remove(vertex)

        # -----------------------------------------------------------------------------------------------------------------------
        def final(graph, NODE):
            all_cycles = []
            graph_temp = []
            for src in NODE:
                all_cycles = all_cycles + remove_cycles(src)
                del_node(src, NODE)
                return all_cycles

        Cycles = []
        while len(ori_graph) > 2:
            Cycles = Cycles + final(ori_graph, NODE)
        print 'All cycles:', Cycles
        Cycle_ID = range(0, len(Cycles))

        Beta = {}
        cycle_links = {}
        for c in Cycle_ID:
            cycle_links[c]=[]
            for j in range(0, len(Cycles[c]) - 1):
                m = Cycles[c][j]
                n = Cycles[c][j + 1]
                cycle_links[c].append((m,n))
                cycle_links[c].append((n,m))
        #print cycle_links
        for c in Cycle_ID:
            for l in Link_ID:
                if Set_Links[l] in cycle_links[c]:
                    Beta[(c, l)] = 1
                else:
                    Beta[(c, l)] = 0
        total_wk_trf = 0
        for l in Link_ID:
            total_wk_trf = total_wk_trf + L[Set_Links[l]]
        #print 'beta',Beta
        prob = LpProblem('P-cycle', LpMinimize)
        S = LpVariable.dicts('S', Link_ID, 0, None, LpInteger)
        NC = LpVariable.dicts('NC', Cycle_ID, 0, None, LpInteger)
        # objective function
        # prob += lpSum(C[l]*S[l] for l in L)
        prob += lpSum(S[l] for l in Link_ID)
        # constraint 1
        for l in Link_ID:
            prob += S[l] - lpSum(Beta[(c,l)] * NC[c] for c in Cycle_ID) == 0
        # constraint 2
        for l in Link_ID:
            prob += lpSum(Beta[(c,l)]* NC[c] for c in Cycle_ID) >= L[Set_Links[l]]

        prob.writeLP("P-cycle.lp")
        prob.solve()
        print'Status:', LpStatus[prob.status]
        print'Optimal solution:', value(prob.objective)
        for l in Link_ID:
            print 'S', l, value(S[l])
        count_c = 0
        used_cycles = []
        for c in Cycle_ID:
            print ('NC', c, value(NC[c]))
            if value(NC[c]) != 0:
                count_c = count_c + 1
                used_cycles.append(c)

        ###############
        self.reset_frame_info_bottom()  # reset info frame
        self.frame_link_info_topmost = Frame(self.scrollframe_info_bottom)
        self.frame_link_info_topmost.pack(side=TOP, expand=YES, fill=BOTH)
        Label(self.frame_link_info_topmost,
              text="Working traffic: " + str(total_wk_trf)+"\n" + \
                   "Spare traffic: " + str(value(prob.objective))+"\n" + \
                   "# cycles used: " + str(count_c)+"/"+str(len(Cycle_ID))+"\n"+ \
                   str(used_cycles), fg="blue").grid(row=0)
        ################
        def callback_check_cycle():
            for key in self.edge_list:
                self.canvas.itemconfig(key, fill='black')
                self.canvas.itemconfig(self.edge_list[key]['distance'].keys()[0], state=HIDDEN)
                #self.canvas.itemconfig.(self.text, state = HIDDEN)
                self.canvas.delete('self.text')
            c = int(self.e3.get())
            color = "#" + ("%06x" % random.randint(0, 16777215))
            if c in Cycle_ID:
                if value(NC[c]) != 0:
                    for key in self.edge_list:
                        if self.edge_list[key]['fromto'] in cycle_links[c]:
                            self.canvas.itemconfig(key, fill=color)
                            node1 = self.edge_list[key]['fromto'][0]
                            node2 = self.edge_list[key]['fromto'][1]
                            coor1 = self.node_pos[node1]
                            coor2 = self.node_pos[node2]
                            midx1 = (coor1[0] + coor1[2]) / 2.0
                            midy1 = (coor1[1] + coor1[3]) / 2.0
                            midx2 = (coor2[0] + coor2[2]) / 2.0
                            midy2 = (coor2[1] + coor2[3]) / 2.0
                            self.text = self.canvas.create_text((midx1 + midx2) / 2.0 + 10,
                                                                    (midy1 + midy2) / 2.0 - 10,
                                                                    text=str(value(NC[c])), fill = color)  # create edge label = spare capacity
                            self.canvas.itemconfig(self.text, tag = 'self.text')


                else:
                    for key in self.edge_list:
                        if self.edge_list[key]['fromto'] in cycle_links[c]:
                            self.canvas.itemconfig(key, fill=color)
                            node1 = self.edge_list[key]['fromto'][0]
                            node2 = self.edge_list[key]['fromto'][1]
                            coor1 = self.node_pos[node1]
                            coor2 = self.node_pos[node2]
                            midx1 = (coor1[0] + coor1[2]) / 2.0
                            midy1 = (coor1[1] + coor1[3]) / 2.0
                            midx2 = (coor2[0] + coor2[2]) / 2.0
                            midy2 = (coor2[1] + coor2[3]) / 2.0
                            self.text = self.canvas.create_text((midx1 + midx2) / 2.0 + 10,
                                                                    (midy1 + midy2) / 2.0 - 10,
                                                                    text=str(value(NC[c])), fill = color)  # create edge label = spare capacity
                            self.canvas.itemconfig(self.text, tag = 'self.text')
                    tkMessageBox.showinfo("OK","Didnt use cycle: " + str(Cycle_ID[c]))
            else:
                tkMessageBox.showinfo("OK","Number of cycles can take only from " + str(Cycle_ID[0])+" to "+str(Cycle_ID[-1]))

        Label(self.frame_link_info_topmost, text = "Using cycle: ").grid(row=1)
        self.e3 = Entry(self.frame_link_info_topmost)
        self.e3.grid(row=1, column=1)
        self.toolbar_check_cycle = Frame(self.scrollframe_info_bottom, borderwidth=2, relief=RIDGE, background="tan")
        self.toolbar_check_cycle.pack(side=BOTTOM, expand=NO, fill=BOTH)
        b_check_cycle = Button(self.toolbar_check_cycle, text="check", width=6,
                                   command= callback_check_cycle)
        b_check_cycle.pack(side=TOP, padx=2, pady=2)
        self.canvas.itemconfig(self.sel_item, fill='#FF0000')
        self.scrollframe_info_bottom.updateScrollers()


    ####################################################################################
    def callback_rand(self):
        for self.sel_item in self.node_list.keys():
            self.canvas.delete(self.sel_item)
            name = self.node_list.pop(self.sel_item)['name'].keys()[0]  # remove from topology
            self.canvas.delete(name)  # delete node's name text
        for self.sel_item in self.edge_list.keys():
            self.canvas.delete(self.sel_item)
            link = self.edge_list.pop(self.sel_item)
            distance_id = link['distance'].keys()[0]
            self.canvas.delete(distance_id)

        self.prev_item = None
        self.sel_item = None
        self.prev_sel_item = None
        self.prev_sel_type = None
        self.prev_type = None
        self.sel_type = None
        self.prev_x = None
        self.prev_y = None
        self.node_list = {}
        self.edge_list = {}

        while len(self.node_list) < 10:
            self.click_x = random.randint(1, 1000)
            self.click_y = random.randint(1, 800)
            self.node = self.canvas.create_oval(self.click_x - 15, self.click_y - 15, self.click_x + 15,
                                            self.click_y + 15, fill="CYAN")
            self.text = self.canvas.create_text(self.click_x, self.click_y + 25, text='A' + str(self.node))
            self.canvas.itemconfig(self.node, tags=self.node)
            self.node_list[self.node] = {}
            self.node_list[self.node]['name'] = {}
            self.node_list[self.node]['name'][self.text] = 'A' + str(self.node)
            self.node_pos[self.node] = self.canvas.coords(self.node)
            self.status.set(self.status_mode + ":" + "node created")
        # for k in self.node_list.keys():
        #     x = (self.node_pos[k][0] + self.node_pos[k][2]) / 2.0
        #     y = (self.node_pos[k][1] + self.node_pos[k][3]) / 2.0
        #     self.node_cor[k] = [x, y]
        # while len(self.edge_list) < 2:
        #     node1= random.choice(self.node_cor.keys())
        #     node2= random.choice(self.node_cor.keys())
        #     if node1!=node2:
        #         curr_x =  self.node_cor[node1][0]# line position
        #         curr_y =  self.node_cor[node1][1]
        #         self.prev_x = self.node_cor[node2][0]
        #         self.prev_y = self.node_cor[node2][1]
        #         self.edge = self.canvas.create_line(self.prev_x, self.prev_y,
        #                                     curr_x, curr_y, fill=self.defaultLineColor, arrow=None,
        #                                     width=3)
        #         dist_text = '1.0'  # default distance
        #         self.text = self.canvas.create_text((self.prev_x + curr_x) / 2.0 + 15,  # text position
        #                                     (self.prev_y + curr_y) / 2.0 + 15, text=dist_text)
        #         self.edge_list[self.edge] = {}
        #         #self.edge_list[self.edge]['fromto'] = (self.prev_item, self.sel_item)
        #         self.edge_list[self.edge]['distance'] = {}
        #         self.edge_list[self.edge]['distance'][self.text] = dist_text

    def callback_background(self):
        if self.state == "Hidden":
            self.canvas.itemconfig(self.bg, state=NORMAL)
            self.state = "Showing"
        elif self.state == "Showing":
            self.canvas.itemconfig(self.bg,state = HIDDEN)
            self.state = "Hidden"
    ##############################################################################################
    def callback_partitioning(self):
        print 'set border nodes:', self.set_border_nodes
        border_links = []
        border_links.append((self.set_border_nodes[0], self.set_border_nodes[-1]))
        border_links.append((self.set_border_nodes[-1], self.set_border_nodes[0]))
        print border_links
        for i in range(0, len(self.set_border_nodes) - 1):
            n1 = self.set_border_nodes[i]
            n2 = self.set_border_nodes[i + 1]
            border_links.append((n1, n2))
            border_links.append((n2, n1))
        print 'border_links', border_links

        def find_path(graph, start, end, path=[], all_path=[]):
            path = path + [start]
            if start == end:
                all_path.append(path)
                return
            if start in graph.keys():
                for node in graph[start]:
                    if node not in path:
                        find_path(graph, node, end, path, all_path)
            return all_path

        Route_Table = {}
        B = {}
        for src in self.set_border_nodes:
            for dst in self.set_border_nodes:
                if src < dst:
                    B[(src, dst)] = []
                    all_path = []
                    A = find_path(self.graph, src, dst, [], all_path)
                    A.sort()
                    A.sort(key=len)
                    for a in A:
                        for n in self.set_border_nodes:
                            if n != src and n != dst:
                                if n in a:
                                    B[(src, dst)].append(a)
                    Route_Table[(src, dst)] = A
        C = {}
        shared_routes = []
        for src in self.set_border_nodes:
            for dst in self.set_border_nodes:
                if src < dst:
                    C[(src, dst)] = []
                    B[(src, dst)].sort()
                    B[(src, dst)] = list(B[(src, dst)] for B[(src, dst)], _ in itertools.groupby(B[(src, dst)]))
                    for i in Route_Table[(src, dst)]:
                        if i not in B[(src, dst)] and tuple(i) not in border_links:
                            C[(src, dst)].append(i)
                    for j in C[(src, dst)]:
                        shared_routes.append(j)
        print 'shared_routes', shared_routes
        print 'len shared_routes', len(shared_routes)
        edges_subnets = {}
        l = len(self.set_border_nodes)
        add_nodes={}
        border_set = {}
        for i in range(0, len(shared_routes)):
            j=0
            k=0
            pos_src = self.set_border_nodes.index(shared_routes[i][0])
            pos_dst = self.set_border_nodes.index(shared_routes[i][-1])
            add_nodes[i]={}
            add_nodes[i][self.set_border_nodes[pos_src]]=[]
            add_nodes[i][self.set_border_nodes[pos_dst]] = []
            while (pos_src+j)%l!= pos_dst:
                add_nodes[i][self.set_border_nodes[pos_src]] += [self.set_border_nodes[(pos_src+j)%l]]
                j += 1
            add_nodes[i][self.set_border_nodes[pos_src]].pop(0)
            while (pos_dst+k)%l != pos_src:
                add_nodes[i][self.set_border_nodes[pos_dst]].append(self.set_border_nodes[(pos_dst+k)%l])
                k += 1
            add_nodes[i][self.set_border_nodes[pos_dst]].pop(0)
            add_nodes[i][self.set_border_nodes[pos_src]].reverse()
            print 'add_nodes',add_nodes
            border_set[i] = {}
            border_set[i][0] = shared_routes[i] + add_nodes[i][self.set_border_nodes[pos_dst]] + [shared_routes[i][0]]
            border_set[i][1] = shared_routes[i] + add_nodes[i][self.set_border_nodes[pos_src]] + [shared_routes[i][0]]
        print border_set
        print "self.node_list",self.node_list
        #print 'self.node_pos',self.node_pos
        print 'self.node_cor',self.node_cor
        ##function finding intersection of 2 lines
        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0] * p2[1] - p2[0] * p1[1])
            return A, B, -C

        def intersection(L1, L2):
            D = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x, y
            else:
                return False

        for i in range(0, len(shared_routes)):
            for n in range(0, len(border_set[i][0])-1):
                node1 = border_set[i][0][n]
                node2 = border_set[i][0][n+1]
                ##find intersection between considering node horizental
                for node in self.node_list:
                    if node not in self.set_border_nodes and node not in shared_routes[i] :
                        ## create a hozirental line contain node:
                        ref_node_cor = [0,self.node_cor[node][1]]
                        L1 = line(ref_node_cor, self.node_cor[node])
                        L2 = line(self.node_cor[node1], self.node_cor[node2])
                        R = intersection(L1, L2)
                        if R:
                            print "Intersection detected:", R
                        dist1 = math.hypot(R[0] - self.node_cor[node1][0], R[1] - self.node_cor[node1][1])
                        dist2 = math.hypot(R[0] - self.node_cor[node2][0], R[1] - self.node_cor[node2][1])
                        dist = math.hypot(self.node_cor[node2][0] - self.node_cor[node1][0], self.node_cor[node2][1] - self.node_cor[node1][1])
                        if dist1 + dist2 == dist:
                            print "true"
                        else:
                            print "fail"







    def callback_find_border(self):
        self.reset()
        self.reset_frame_info()
        color = "#" + ("%06x" % random.randint(0, 16777215))
        set_border_nodes = []
        ##      print 'self.node_list', self.node_list
        ##      print 'self.node_pos', self.node_pos
        print 'self.edge_list',self.edge_list
        for k in self.node_list.keys():
            x = (self.node_pos[k][0] + self.node_pos[k][2]) / 2.0
            y = (self.node_pos[k][1] + self.node_pos[k][3]) / 2.0
            self.node_cor[k] = [x, y]
        ##      print 'self.node_cor', self.node_cor
        edge_ID = 0
        for l in self.edge_list.keys():
            self.edge_simp_list[edge_ID] = self.edge_list[l]['fromto']
            edge_ID = edge_ID + 1
        print 'self.edge_simp_list',self.edge_simp_list
        for k in self.node_list.keys():
            self.graph[k] = []
            for l in self.edge_simp_list.keys():
                if k in self.edge_simp_list[l]:
                    if k == self.edge_simp_list[l][0]:
                        neigh = self.edge_simp_list[l][1]
                    else:
                        neigh = self.edge_simp_list[l][0]
                    self.graph[k].append(neigh)
                    ##      print 'self.graph',self.graph
                    #### find the lowest node ##########
        self.first_node_cor = [0, 1000000]
        for k in self.node_list.keys():
            if self.first_node_cor[1] > self.node_cor[k][1]:
                self.first_node_cor = self.node_cor[k]
        self.first_node = list(self.node_cor.keys())[list(self.node_cor.values()).index(self.first_node_cor)]
        first_node_cor = self.first_node_cor
        ref_vec = [1, 0]
        min_angle = 181
        chosen_node = -1
        for n in self.graph[self.first_node]:
            # self.canvas.itemconfig(n,fill='yellow')
            tmp_node_cor = self.node_cor[n]
            B = [tmp_node_cor[0] - first_node_cor[0], tmp_node_cor[1] - first_node_cor[1]]
            ##         self.vect=self.canvas.create_text(self.node_cor[n][0],self.node_cor[n][1]+15,text='vect='+str(B))
            angle = math.acos((ref_vec[0] * B[0] + ref_vec[1] * B[1]) / math.hypot(B[0], B[1])) * 180 / math.pi
            ##         self.angle=self.canvas.create_text(self.node_cor[n][0],self.node_cor[n][1]+30,text='angle='+str(angle))
            if min_angle > angle:
                chosen_node = n
                min_angle = angle
        self.canvas.itemconfig(chosen_node, fill=color)
        set_border_nodes.append(chosen_node)
        #############################################################################################################################################################################
        #############################################################################################################################################################################
        # prev_chosen_node = self.first_node
        prev_chosen_node_cor = first_node_cor
        chosen_node_cor = self.node_cor[chosen_node]

        while chosen_node != self.first_node:
            best_cand_zone = 5
            best_cand_angle = 0
            new_chosen_node = -5
            #print 'while loop'
            ref_vec = [prev_chosen_node_cor[0] - chosen_node_cor[0], prev_chosen_node_cor[1] - chosen_node_cor[1]]
            ref_angle = math.atan(ref_vec[1] / ref_vec[0]) * 180 / math.pi
            gen = (n for n in self.graph[chosen_node] if n not in set_border_nodes)
            for n in gen:
                print 'n',n
                tmp_node_cor = self.node_cor[n]
                cand_vec = [tmp_node_cor[0] - chosen_node_cor[0], tmp_node_cor[1] - chosen_node_cor[1]]
                cand_angle = math.atan(cand_vec[1] / cand_vec[0]) * 180 / math.pi
                cand_angle = abs(cand_angle)
                if ref_vec[0]<0 and ref_vec[1]<0:
                    print 'quad 0'
                    if cand_vec[0] < 0 and cand_vec[1] < 0:
                        if cand_angle > ref_angle:
                            cand_zone = 0
                        else:
                            cand_zone = 4
                    elif cand_vec[0] > 0 and cand_vec[1] < 0:
                        cand_zone = 1
                    elif cand_vec[0] > 0 and cand_vec[1] > 0:
                        cand_zone = 2
                    elif cand_vec[0] < 0 and cand_vec[1] > 0:
                        cand_zone = 3
                    print 'cand_zone',cand_zone
                    if cand_zone < best_cand_zone:
                        new_chosen_node=n
                        best_cand_zone=cand_zone
                        best_cand_angle=cand_angle
                    elif cand_zone == best_cand_zone:
                        if cand_zone == 0:
                            print 'zone 0'
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 1:
                            print 'zone 1'
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 2:
                            print 'zone 2'
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 3:
                            print 'zone 3'
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 4:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                elif ref_vec[0]>0 and ref_vec[1]<0:
                    if cand_vec[0] > 0 and cand_vec[1] < 0:
                        if cand_angle < ref_angle:
                            cand_zone = 0
                        else:
                            cand_zone = 4
                    elif cand_vec[0] > 0 and cand_vec[1] > 0:
                        cand_zone = 1
                    elif cand_vec[0] < 0 and cand_vec[1] > 0:
                        cand_zone = 2
                    elif cand_vec[0] < 0 and cand_vec[1] < 0:
                        cand_zone = 3

                    if cand_zone < best_cand_zone:
                        new_chosen_node=n
                        best_cand_zone=cand_zone
                        best_cand_angle=cand_angle
                    elif cand_zone == best_cand_zone:
                        if cand_zone == 0:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 1:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 2:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 3:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 4:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                elif ref_vec[0]>0 and ref_vec[1]>0:
                    if cand_vec[0] > 0 and cand_vec[1] > 0:
                        if cand_angle > ref_angle:
                            cand_zone = 0
                        else:
                            cand_zone = 4
                    elif cand_vec[0] < 0 and cand_vec[1] > 0:
                        cand_zone = 1
                    elif cand_vec[0] < 0 and cand_vec[1] < 0:
                        cand_zone = 2
                    elif cand_vec[0] > 0 and cand_vec[1] < 0:
                        cand_zone = 3

                    if cand_zone < best_cand_zone:
                        new_chosen_node=n
                        best_cand_zone=cand_zone
                        best_cand_angle=cand_angle
                    elif cand_zone == best_cand_zone:
                        if cand_zone == 0:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 1:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 2:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 3:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 4:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                elif ref_vec[0]<0 and ref_vec[1]>0:
                    print 'ref 3'
                    if cand_vec[0] < 0 and cand_vec[1] > 0:
                        if cand_angle > ref_angle:
                            print 'cand 0'
                            cand_zone = 0
                        else:
                            print "cand 4"
                            cand_zone = 4
                    elif cand_vec[0] < 0 and cand_vec[1] < 0:
                        cand_zone = 1
                    elif cand_vec[0] > 0 and cand_vec[1] < 0:
                        cand_zone = 2
                    elif cand_vec[0] > 0 and cand_vec[1] > 0:
                        cand_zone = 3
                    print "best cand",best_cand_zone
                    if cand_zone < best_cand_zone:
                        new_chosen_node=n
                        best_cand_zone=cand_zone
                        best_cand_angle=cand_angle
                    elif cand_zone == best_cand_zone:
                        if cand_zone == 0:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 1:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 2:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 3:
                            if best_cand_angle > cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
                        if cand_zone == 4:
                            if best_cand_angle < cand_angle:
                                new_chosen_node=n
                                best_cand_zone=cand_zone
                                best_cand_angle=cand_angle
            prev_chosen_node_cor = self.node_cor[chosen_node]
            print 'chosen_node',chosen_node
            chosen_node = new_chosen_node
            print 'new_chosen_node',new_chosen_node
            chosen_node_cor = self.node_cor[chosen_node]
            self.canvas.itemconfig(new_chosen_node, fill=color)
            set_border_nodes.append(new_chosen_node)
            print 'set_border_nodes', set_border_nodes
            self.set_border_nodes = set_border_nodes

    def callback_clear(self):
        if self.node_list or self.edge_list or self.topo or self.node_pos:
            if tkMessageBox.askokcancel("Warning!",
                                        "Do you really want to clear workspace?\nAll items will be removed!!!"):
                # ----- reset canvas & button ----#
                self.canvas.delete(ALL)
                self.b1.configure(default=NORMAL)
                self.b2.configure(default=NORMAL)
                self.b3.configure(default=NORMAL)
                self.b4.configure(default=NORMAL)
                self.f1.configure(default=NORMAL)
                self.f2.configure(default=NORMAL)
                # -----  ----#
                self.prev_item = None
                self.sel_item = None
                self.prev_type = None
                self.sel_type = None
                self.prev_x = None
                self.prev_y = None
                self.node_list = {}
                self.edge_list = {}
                self.topo = {}
                self.node_pos = {}
                # ----- optimization ----#
                self.k_num = 2
                self.default_wave_num = 2
                self.default_slot_num = 4
                self.default_fiber_num = 1
                self.traffic_mat = None
                self.default_workcap_num = 100
                self.wave_num = {}
                self.slot_num = {}
                self.workcap_num = {}
                self.fiber_num = {}
                self.paths_allo_bw = None
                self.wave_link = None
                self.add_wave_link = None
                self.wave_link_use = {}
                self.draw_addwave_key = []
                self.add_legend_key = []
                self.obj_cri = 1  # 1=minimize resource,#2=maximize supported traffic,#3=Minimize the additional link capacity.
                self.obj_value = None
                self.trf_split = 0
                self.sdlist = {}
                self.drawopt_link_key = []
                self.drawopt_node_key = []
                self.index = 0
                # -----  ----#
                self.do = None
                self.status_mode = None
                self.paths = None
                # ----- reset info frame ----#
                self.reset_frame_info()
                return TRUE
            else:
                return FALSE
        else:
            return TRUE

    # ------------------------------close-----------------------------
    def callback_close(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.myParent.destroy()

    # ------------------------------open------------------------------
    def callback_open(self):
        if TRUE:
            # get filename
            self.status.set("OPEN FILE: opening...")
            self.file_opt['filetypes'] = [('all files', '*'), ('workspace files', '.wp')]
            self.file_opt['initialfile'] = 'workspace.wp'
            filename = tkFileDialog.askopenfilename(**self.file_opt)
            # open file
            if filename:
                f = open(filename, 'r')
                open_ok = 1
                try:
                    tmp_node_list = pickle.load(f)
                    tmp_edge_list = pickle.load(f)
                    tmp_topo = pickle.load(f)
                    tmp_node_pos = pickle.load(f)
                    tmp_wave_num = pickle.load(f)
                    tmp_slot_num = pickle.load(f)
                    tmp_fiber_num = pickle.load(f)
                    tmp_workcap_num = pickle.load(f)
                except:
                    tkMessageBox.showerror("File not accepted", "Error: " + str(sys.exc_info()[0]))
                    open_ok = 0
                f.close()
                if open_ok and self.callback_clear():
                    self.reset()
                    self.reset_frame_info()
                    self.topo = tmp_topo
                    self.wave_num = tmp_wave_num
                    self.slot_num = tmp_slot_num
                    self.fiber_num = tmp_fiber_num
                    self.workcap_num= tmp_workcap_num
                    # draw
                    if len(tmp_node_list):  # create node
                        match_node = {}
                        for inode in tmp_node_list.keys():
                            coor1 = tmp_node_pos[inode]
                            name = tmp_node_list[inode]['name'].values()[0]
                            self.node = self.canvas.create_oval(coor1[0], coor1[1], coor1[2],
                                                                coor1[3], fill="CYAN")
                            self.text = self.canvas.create_text((coor1[0] + coor1[2]) / 2.0,
                                                                ((coor1[1] + coor1[3]) / 2.0) + 25,
                                                                text=name)  # create node label
                            self.canvas.itemconfig(self.node, tags=self.node)
                            self.node_list[self.node] = {}
                            self.node_list[self.node]['name'] = {}
                            self.node_list[self.node]['name'][self.text] = name
                            self.node_pos[self.node] = self.canvas.coords(self.node)
                            match_node[inode] = self.node
                        for iedge in tmp_edge_list:  # create edge
                            node1 = tmp_edge_list[iedge]['fromto'][0]
                            node2 = tmp_edge_list[iedge]['fromto'][1]
                            inode = match_node[node1]
                            jnode = match_node[node2]
                            coor1 = self.node_pos[inode]
                            coor2 = self.node_pos[jnode]
                            midx1 = (coor1[0] + coor1[2]) / 2.0
                            midy1 = (coor1[1] + coor1[3]) / 2.0
                            midx2 = (coor2[0] + coor2[2]) / 2.0
                            midy2 = (coor2[1] + coor2[3]) / 2.0
                            distance = tmp_edge_list[iedge]['distance'].values()[0]
                            self.edge = self.canvas.create_line(midx1, midy1, midx2, midy2,
                                                                fill=self.defaultLineColor, arrow=None, width=3)
                            #### hidden distance, show working capacity
                            # self.text = self.canvas.create_text((midx1 + midx2) / 2.0 + 10,
                            #                                     (midy1 + midy2) / 2.0 - 10,
                            #                                     text=distance)  # create edge label
                            self.text = self.canvas.create_text((midx1 + midx2) / 2.0 + 10,
                                                                (midy1 + midy2) / 2.0 - 10,
                                                                 text=self.workcap_num['A' + str(node1)]['A' + str(node2)])  # create edge label
                            self.edge_list[self.edge] = {}
                            self.edge_list[self.edge]['fromto'] = (inode, jnode)
                            self.edge_list[self.edge]['distance'] = {}
                            self.edge_list[self.edge]['distance'][self.text] = float(distance)
                        self.status.set("OPEN FILE:" + filename + " loaded")
                        self.b1.configure(default=NORMAL, relief=GROOVE)
                        self.b2.configure(default=NORMAL, relief=GROOVE)
                        self.b3.configure(default=NORMAL, relief=GROOVE)
                        self.b4.configure(default=NORMAL, relief=GROOVE)
                        self.f1.configure(default=NORMAL, relief=GROOVE)
                        self.f2.configure(default=NORMAL, relief=GROOVE)
                        self.do = None

    # ------------------------------demo------------------------------
    def callback_demo(self):
        if TRUE:
            # get filename
            self.status.set("DEMO - COST239 network")
            filename = 'COST239.wp'
            # open file
            if filename:
                f = open(filename, 'r')
                open_ok = 1
                try:
                    tmp_node_list = pickle.load(f)
                    tmp_edge_list = pickle.load(f)
                    tmp_topo = pickle.load(f)
                    tmp_node_pos = pickle.load(f)
                    tmp_wave_num = pickle.load(f)
                    tmp_slot_num = pickle.load(f)
                    tmp_fiber_num = pickle.load(f)
                    tmp_workcap_num = pickle.load(f)
                except:
                    tkMessageBox.showerror("File not accepted", "Error: " + str(sys.exc_info()[0]))
                    open_ok = 0
                f.close()
                if open_ok and self.callback_clear():
                    self.reset()
                    self.reset_frame_info()
                    self.topo = tmp_topo
                    self.wave_num = tmp_wave_num
                    self.slot_num = tmp_slot_num
                    self.fiber_num = tmp_fiber_num
                    #self.workcap_num = tmp_workcap_num
                    # draw
                    if len(tmp_node_list):  # create node
                        match_node = {}
                        for inode in tmp_node_list.keys():
                            coor1 = tmp_node_pos[inode]
                            name = tmp_node_list[inode]['name'].values()[0]
                            self.node = self.canvas.create_oval(coor1[0], coor1[1], coor1[2],
                                                                coor1[3], fill="CYAN")
                            self.text = self.canvas.create_text((coor1[0] + coor1[2]) / 2.0,
                                                                ((coor1[1] + coor1[3]) / 2.0) + 25,
                                                                text=name)  # create node label
                            self.canvas.itemconfig(self.node, tags=self.node)
                            self.node_list[self.node] = {}
                            self.node_list[self.node]['name'] = {}
                            self.node_list[self.node]['name'][self.text] = name
                            self.node_pos[self.node] = self.canvas.coords(self.node)
                            match_node[inode] = self.node
                        for iedge in tmp_edge_list:  # create edge
                            node1 = tmp_edge_list[iedge]['fromto'][0]
                            node2 = tmp_edge_list[iedge]['fromto'][1]
                            inode = match_node[node1]
                            jnode = match_node[node2]
                            coor1 = self.node_pos[inode]
                            coor2 = self.node_pos[jnode]
                            midx1 = (coor1[0] + coor1[2]) / 2.0
                            midy1 = (coor1[1] + coor1[3]) / 2.0
                            midx2 = (coor2[0] + coor2[2]) / 2.0
                            midy2 = (coor2[1] + coor2[3]) / 2.0
                            distance = tmp_edge_list[iedge]['distance'].values()[0]
                            self.edge = self.canvas.create_line(midx1, midy1, midx2, midy2,
                                                                fill=self.defaultLineColor, arrow=None, width=3)
                            self.text = self.canvas.create_text((midx1 + midx2) / 2.0 + 10,
                                                                (midy1 + midy2) / 2.0 - 10,
                                                                text=distance)  # create edge label
                            self.edge_list[self.edge] = {}
                            self.edge_list[self.edge]['fromto'] = (inode, jnode)
                            self.edge_list[self.edge]['distance'] = {}
                            self.edge_list[self.edge]['distance'][self.text] = float(distance)
                        self.status.set("OPEN FILE:" + filename + " loaded")
                        self.b1.configure(default=NORMAL, relief=GROOVE)
                        self.b2.configure(default=NORMAL, relief=GROOVE)
                        self.b3.configure(default=NORMAL, relief=GROOVE)
                        self.b4.configure(default=NORMAL, relief=GROOVE)
                        self.f1.configure(default=NORMAL, relief=GROOVE)
                        self.f2.configure(default=NORMAL, relief=GROOVE)
                        self.do = None

    def callback_showtrf(self):
        if os.name == 'nt':
            os.system('notepad.exe ' + 'COST239_traffic.txt')  # open file by notepad
        elif os.name == 'posix':
            os.system('emacs ' + 'COST239_traffic.txt')  # open file by emacs
        self.reset()
        self.reset_frame_info()
        self.frame_link_info_top = Frame(self.scrollframe_info_top)
        self.frame_link_info_top.pack(side=TOP, expand=NO, fill=BOTH)
        Label(self.frame_link_info_top, text="Traffic file format::").grid(row=0)
        Label(self.frame_link_info_top, text="Source(comma)Destination(comma)Distance(comma)(newline)").grid(row=1,
                                                                                                             sticky=W)
        Label(self.frame_link_info_top, text="-------------------------------------------------------").grid(row=2,
                                                                                                             sticky=W)
        Label(self.frame_link_info_top, text="London,Praque,13,").grid(row=3, sticky=W)
        Label(self.frame_link_info_top, text="Paris,Copenhagen,12,").grid(row=4, sticky=W)
        Label(self.frame_link_info_top, text="Amsterdam,Milan,15,").grid(row=5, sticky=W)
        Label(self.frame_link_info_top, text="Praque,Paris,25,").grid(row=6, sticky=W)
        Label(self.frame_link_info_top, text="-------------------------------------------------------").grid(row=7,
                                                                                                             sticky=W)
        # update the scrollregion
        self.scrollframe_info_top.updateScrollers()

    # ------------------------------save------------------------------
    def callback_save(self):
        self.reset()
        self.reset_frame_info()
        self.file_opt = options = {}
        options['defaultextension'] = ''
        options['filetypes'] = [('all files', '*'), ('workspace files', '.wp')]
        # options['initialdir'] = 'C:\\'
        options['initialfile'] = 'workspace.wp'
        options['parent'] = self.myParent
        options['title'] = 'Save File'
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)  # get filename
        if filename:
            f = open(filename, 'w')
            pickle.dump(self.node_list, f)
            pickle.dump(self.edge_list, f)
            pickle.dump(self.topo, f)
            pickle.dump(self.node_pos, f)
            pickle.dump(self.wave_num, f)
            pickle.dump(self.slot_num, f)
            pickle.dump(self.fiber_num, f)
            pickle.dump(self.workcap_num, f)
            f.close()
            self.status.set("SAVE FILE: workspace saved")
        if self.paths:
            self.reset()

    # ------------------------remove node/edge------------------------
    def callback_remove(self):
        self.status_mode = "REMOVE NODE/EDGE"
        self.reset()
        if self.do != "remove":
            self.b1.configure(default=NORMAL, relief=GROOVE)
            self.b2.configure(default=NORMAL, relief=GROOVE)
            self.b3.configure(default=ACTIVE, relief=GROOVE)
            self.b4.configure(default=NORMAL, relief=GROOVE)
            self.f1.configure(default=NORMAL, relief=GROOVE)
            self.f2.configure(default=NORMAL, relief=GROOVE)
            self.do = "remove"
            self.status.set(self.status_mode + ":" + " click on nodes or edges to remove...")
        else:
            self.b3.configure(default=NORMAL, relief=GROOVE)
            self.do = None
            self.status.set(self.status_mode + ":" + " ...")
            self.status_mode = "Move node"
            self.status.set("...")

    # ------------------------edit node/edge------------------------
    def callback_edit(self):
        self.status_mode = "EDIT ATTRIBUTE"
        self.reset()
        self.reset_frame_info()
        if self.do != "edit":
            self.b1.configure(default=NORMAL, relief=GROOVE)
            self.b2.configure(default=NORMAL, relief=GROOVE)
            self.b3.configure(default=NORMAL, relief=GROOVE)
            self.b4.configure(default=ACTIVE, relief=GROOVE)
            self.f1.configure(default=NORMAL, relief=GROOVE)
            self.f2.configure(default=NORMAL, relief=GROOVE)
            self.do = "edit"
            self.status.set(self.status_mode + ":" + " click on nodes or edges to edit...")
        else:
            self.b4.configure(default=NORMAL, relief=GROOVE)
            self.do = None
            self.status.set(self.status_mode + ":" + " ...")
            self.status_mode = "Move node"
            self.status.set("...")

    # --------------------------create node---------------------------
    def callback_create_node(self):
        self.status_mode = "CREATE NODE"
        self.reset()
        self.reset_frame_info()
        if self.do != "create node":
            self.b1.configure(default=ACTIVE, relief=GROOVE)
            self.b2.configure(default=NORMAL, relief=GROOVE)
            self.b3.configure(default=NORMAL, relief=GROOVE)
            self.b4.configure(default=NORMAL, relief=GROOVE)
            self.f1.configure(default=NORMAL, relief=GROOVE)
            self.f2.configure(default=NORMAL, relief=GROOVE)
            self.do = "create node"
            self.status.set(self.status_mode + ":" + " create node...")
        else:
            self.b1.configure(default=NORMAL, relief=GROOVE)
            self.do = None
            self.status.set(self.status_mode + ":" + " ...")
            self.status_mode = "Move node"
            self.status.set("...")

    # --------------------------create edge---------------------------
    def callback_create_edge(self):
        self.status_mode = "CREATE EDGE"
        self.reset()
        self.reset_frame_info()
        if self.do != "create edge" and self.do != "select another node...":
            self.b1.configure(default=NORMAL, relief=GROOVE)
            self.b2.configure(default=ACTIVE, relief=GROOVE)
            self.b3.configure(default=NORMAL, relief=GROOVE)
            self.b4.configure(default=NORMAL, relief=GROOVE)
            self.f1.configure(default=NORMAL, relief=GROOVE)
            self.f2.configure(default=NORMAL, relief=GROOVE)
            self.do = "create edge"
            self.status.set(self.status_mode + ":" + " create edge...")
        else:
            self.b2.configure(default=NORMAL, relief=GROOVE)
            self.do = None
            self.status.set(self.status_mode + ":" + "...")
            self.status_mode = "Move node"
            self.status.set("...")

    # --------------------------shortest path------------------------
    def callback_shortestPath(self):
        self.status_mode = "SHORTEST PATH"
        self.reset()
        self.reset_frame_info()
        if self.do != "shortest path" and self.do != "select destination...":
            self.b1.configure(default=NORMAL, relief=GROOVE)
            self.b2.configure(default=NORMAL, relief=GROOVE)
            self.b3.configure(default=NORMAL, relief=GROOVE)
            self.b4.configure(default=NORMAL, relief=GROOVE)
            self.f1.configure(default=ACTIVE, relief=GROOVE)
            self.f2.configure(default=NORMAL, relief=GROOVE)
            self.do = "shortest path"
            self.status.set(self.status_mode + ":" + " select the source...")
        else:
            self.f1.configure(default=NORMAL, relief=GROOVE)
            self.do = None
            self.status.set(self.status_mode + ":" + " ...")
            self.status_mode = "Move node"
            self.status.set("...")

    # --------------------------optimize------------------------
    def callback_opt(self):
        self.status_mode = "OPTIMIZATION"
        self.reset()
        self.reset_frame_info()
        if self.do != "optimize":
            self.status.set(self.status_mode + ":" + " ...")
            # ----------------------------------------------------------
            # choose a traffic matrix file
            # get filename
            self.file_opt['initialfile'] = 'traffic_maxtrix'
            self.file_opt['filetypes'] = [('all files', '*'), ('matrix files', '.txt')]
            self.status.set(self.status_mode + ":" + " opening traffic info...")
            self.filename = tkFileDialog.askopenfilename(**self.file_opt)
            # open file and show
            if self.filename:
                self.b1.configure(default=NORMAL, relief=GROOVE)
                self.b2.configure(default=NORMAL, relief=GROOVE)
                self.b3.configure(default=NORMAL, relief=GROOVE)
                self.b4.configure(default=NORMAL, relief=GROOVE)
                self.f1.configure(default=NORMAL, relief=GROOVE)
                self.f2.configure(default=ACTIVE, relief=GROOVE)
                self.do = "optimize"
                self.reset()
                self.reset_frame_info()
                self.opt_show_top_frame(1)
            else:
                self.f2.configure(default=NORMAL, relief=GROOVE)
                # self.reset_frame_info() #reset info frame
                self.status.set("...")
                self.do = None
        else:
            self.f2.configure(default=NORMAL)
            self.reset_frame_info()  # reset info frame
            self.status.set("...")
            self.do = None
            if self.top_opt2:
                self.top_opt2.destroy()

    # ---------------------optimize/open matrix file-------------------
    def callback_opt_open(self):
        self.status_mode = "OPTIMIZATION"
        # ----------------------------------------------------------
        # choose a traffic matrix file
        # get filename
        self.file_opt['initialfile'] = 'traffic_matrix'
        self.file_opt['filetypes'] = [('all files', '*'), ('matrix files', '.txt')]
        self.status.set(self.status_mode + ":" + " opening traffic info...")
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        # open file and show
        if self.filename:
            self.reset()
            self.opt_show_top_frame(1)
        else:
            self.status.set(self.status_mode + ":" + " ...")

    # --------------------------optimize------------------------
    def callback_opt_optimize(self):
        self.reset()
        if self.drawopt_link_key:  # clear paths
            for ind_key in self.drawopt_link_key:
                for key in self.drawopt_link_key[ind_key]:
                    self.canvas.delete(key)
            self.drawopt_link_key = {}
        if self.top_opt2:
            self.top_opt2.destroy()
        self.obj_cri = self.var_objcri.get()
        self.trf_split = self.var_trafsplit.get()
        for i in range(1, len(self.e)):
            if self.is_integer(self.e[i].get()):
                self.traffic_mat[self.s[i].get()][self.d[i].get()] = int(self.e[i].get())
            else:
                self.e[i].delete(0, END)
                self.e[i].insert(0, self.traffic_mat[self.s[i].get()][self.d[i].get()])
        if self.obj_cri == 1:
            print "Minimize resource"
        elif self.obj_cri == 2:
            print "Maximize number of supported traffic units"
        elif self.obj_cri == 3:
            print "Minimize the additional link capacity"
        self.status.set(self.status_mode + ":" + " optimization - RUNNING...")
        if self.topo and self.traffic_mat:  # NOTE:  Need to check traffic matrix for consistency. (i.e., node name)
            (self.paths_allo_bw, self.wave_link, self.add_wave_link, self.obj_value) = optim.opt_wave(self.topo, \
                                                                                                      self.k_num,
                                                                                                      self.traffic_mat,
                                                                                                      self.wave_num,
                                                                                                      self.fiber_num,
                                                                                                      self.slot_num,
                                                                                                      self.workcap_num,
                                                                                                      self.obj_cri,
                                                                                                      2 - self.trf_split)
            print 'path = ', str(self.paths_allo_bw)
            print 'link = ', str(self.wave_link)
            print 'add wave = ', str(self.add_wave_link)
            self.reset_frame_info_bottom()  # reset info frame
            if self.paths_allo_bw and self.wave_link:
                self.draw_path_opt()
                self.status.set(self.status_mode + ":" + " optimization - done.")
                # --------------------------
                if self.obj_cri == 1:
                    self.opt_show_top_frame(2)
                    self.reset_frame_info_bottom()  # reset info frame
                    self.frame_link_info_topmost = Frame(self.scrollframe_info_bottom)
                    self.frame_link_info_topmost.pack(side=TOP, expand=YES, fill=BOTH)
                    Label(self.frame_link_info_topmost,
                          text="(Minimize resource)\n" + "Total number of utilized wavelength channels = " + \
                               str(self.obj_value), fg="blue").grid(row=0)
                if self.obj_cri == 2:
                    self.reset_frame_info_bottom()  # reset info frame
                    self.frame_link_info_topmost = Frame(self.scrollframe_info_bottom)
                    self.frame_link_info_topmost.pack(side=TOP, expand=YES, fill=BOTH)
                    Label(self.frame_link_info_topmost,
                          text="(Maximize supported traffic units)\n" + "Total number of supported traffic units = " + \
                               str(self.obj_value), fg="blue").grid(row=0)
            else:
                self.status.set(self.status_mode + ":" + " optimization - infeasible!")
                # open file and show
                self.opt_show_top_frame(3)
                if self.obj_cri == 1:
                    self.reset_frame_info_bottom()  # reset info frame
                    self.frame_link_info_topmost = Frame(self.scrollframe_info_bottom)
                    self.frame_link_info_topmost.pack(side=TOP, expand=YES, fill=BOTH)
                    Label(self.frame_link_info_topmost, text="INFEASIBLE", fg="red").grid(row=0)
                tkMessageBox.showinfo("Optimization Window", "Infeasible!")  # show info
            if self.add_wave_link:
                # ------------------- ADDITONAL WAVELENGTH WINDOW ----------------------------#
                if self.top_opt2:
                    self.top_opt2.destroy()
                self.top_opt2 = Toplevel()
                self.frame_add_wave = Frame(self.top_opt2)
                self.scrollframe_top_opt = ScrolledFrame(self.frame_add_wave, 370,
                                                         200)  # Scrolled additional wav needed
                self.top_opt2.title('Additional Wavelengths Needed')
                i = 0
                Label(self.scrollframe_top_opt, text="").grid(row=i, column=0)
                Label(self.scrollframe_top_opt, text="").grid(row=i, column=2)
                Label(self.scrollframe_top_opt, text="additional wavelengths needed").grid(row=i, column=3)
                Label(self.scrollframe_top_opt, text="     ").grid(row=i, column=4)
                Label(self.scrollframe_top_opt, text="     ").grid(row=i, column=4)
                for link in self.add_wave_link:
                    i += 1
                    ilink = link.split(',')
                    node1 = ilink[0].split('(')[1]
                    node2 = ilink[1].split(')')[0]
                    Label(self.scrollframe_top_opt, text=node1).grid(row=i, column=0)
                    Label(self.scrollframe_top_opt, text="-").grid(row=i, column=1)
                    Label(self.scrollframe_top_opt, text=node2).grid(row=i, column=2)
                    Label(self.scrollframe_top_opt, text=self.add_wave_link[link]).grid(row=i, column=3)
                self.frame_add_wave.pack()
                self.status.set(self.status_mode + ":" + " optimization - done.")
                for edge in self.edge_list:
                    self.canvas.itemconfig(self.edge_list[edge]['distance'].keys()[0], state=HIDDEN)
                # update the scrollregion
                self.scrollframe_top_opt.updateScrollers()
        else:
            self.status.set(self.status_mode + ":" + " optimization - insufficient input!")
        # update the scrollregion
        self.scrollframe_info_top.updateScrollers()
        self.scrollframe_info_bottom.updateScrollers()

    # --------------------------click---------------------------------
    def callback_select(self, event):
        self.canvas = event.widget
        self.click_x = self.canvas.canvasx(event.x)
        self.click_y = self.canvas.canvasy(event.y)
        # self.sel_item = self.canvas.find_closest(x, y)
        oval_list = [item for item in self.canvas.find_overlapping(self.click_x - 5, self.click_y - 5, self.click_x + 5,
                                                                   self.click_y + 5) if
                     self.canvas.type(item) == "oval"]
        line_list = [item for item in self.canvas.find_overlapping(self.click_x - 5, self.click_y - 5, self.click_x + 5,
                                                                   self.click_y + 5) if
                     self.canvas.type(item) == "line"]
        if len(oval_list):
            self.sel_item = oval_list[0]
            self.sel_coor = self.canvas.coords(self.sel_item)
            self.sel_type = self.canvas.type(self.sel_item)
        elif len(line_list):
            self.sel_item = line_list[0]
            self.sel_coor = self.canvas.coords(self.sel_item)
            self.sel_type = self.canvas.type(self.sel_item)
        else:
            self.sel_item = None
            self.sel_coor = None
            self.sel_type = None
        # print "clicked at", x, y
        if self.do:
            print 'action = ', self.do
        else:
            print 'action = Move node'
            # print 'selected item = ',self.sel_item , "@", self.sel_coor
            # print 'selected type = ',self.sel_type
            # if not self.sel_item:
            # if self.do == "edit":
            # self.sel_item = self.prev_item
        if self.sel_item and self.sel_type == "oval":
            if self.do == None:  # move node
                self.do = "Move node"
                self.canvas.itemconfig(self.sel_item, fill="red")
                self.status_mode = "MOVE"
            elif self.do == "edit":  # edit node
                self.status.set(self.status_mode + ":" + "edit node")
                self.canvas.itemconfig(self.sel_item, fill="red")
                name_id = self.node_list[self.sel_item]['name'].keys()[0]
                # should disable main window
                prev_name = self.node_list[self.sel_item]['name'][name_id]
                d = EditDialog(self.myParent, "Node Attributes", ['Name'], [prev_name], self.sel_type)
                if d.result:
                    curr_name = d.result[0]
                    if curr_name != prev_name:
                        self.node_list[self.sel_item]['name'][name_id] = curr_name  # node_list
                        self.topo[curr_name] = {}  # topology
                        self.wave_num[curr_name] = {}
                        self.slot_num[curr_name] = {}
                        self.fiber_num[curr_name] = {}
                        self.workcap_num[curr_name] = {}
                        if prev_name in self.topo:
                            for member in self.topo[prev_name]:
                                self.topo[curr_name][member] = self.topo[prev_name][member]
                                self.wave_num[curr_name][member] = self.wave_num[prev_name][member]
                                self.slot_num[curr_name][member] = self.slot_num[prev_name][member]
                                self.fiber_num[curr_name][member] = self.fiber_num[prev_name][member]
                                self.workcap_num[curr_name][member] = self.workcap_num[prev_name][member]
                            self.topo.pop(prev_name)  # remove FROM node
                            self.wave_num.pop(prev_name)
                            self.slot_num.pop(prev_name)
                            self.fiber_num.pop(prev_name)
                            self.workcap_num.pop(prev_name)
                        for node in self.topo:
                            if self.topo[node].has_key(prev_name):
                                self.topo[node][curr_name] = self.topo[node][prev_name]
                                self.wave_num[node][curr_name] = self.wave_num[node][prev_name]
                                self.slot_num[node][curr_name] = self.slot_num[node][prev_name]
                                self.fiber_num[node][curr_name] = self.fiber_num[node][prev_name]
                                self.workcap_num[node][curr_name] = self.workcap_num[node][prev_name]
                                self.topo[node].pop(prev_name)  # remove TO node
                                self.wave_num[node].pop(prev_name)
                                self.slot_num[node].pop(prev_name)
                                self.fiber_num[node].pop(prev_name)
                                self.workcap_num[node].pop(prev_name)
                        self.canvas.itemconfig(name_id, text=curr_name)  # text
                self.canvas.itemconfig(self.sel_item, fill="CYAN")
            elif self.do == "remove":  # remove node
                self.canvas.itemconfig(self.sel_item, fill="red")
                self.do = "removed"
                # create edge or finding shortest path (click on the first node)
            elif self.do == "create edge" or self.do == "shortest path" or self.do == "optimize":
                nodename_select = self.node_list[self.sel_item]['name'].values()[0]
                if self.do == "create edge":
                    self.do = "select another node..."
                elif self.do == "shortest path":
                    self.reset()
                    self.do = "select destination..."
                elif self.do == "optimize":  # added 5/26/2011 - revised 6/13/2011 use elif
                    if self.sdlist.has_key(nodename_select) and self.paths_allo_bw and 0:  # 0=not utilized yet
                        self.do = "select destination node..."
                        if self.drawopt_link_key_press:
                            for key in self.drawopt_link_key_press:
                                self.canvas.delete(key)
                            self.drawopt_link_key_press = []
                        if self.drawopt_node_key_press:
                            for key in self.drawopt_node_key_press:
                                self.canvas.itemconfig(key, fill=self.defaultNodeColor)
                            self.drawopt_node_key_press = []
                    else:
                        return
                else:
                    self.status.set(
                        self.status_mode + ": " + nodename_select + " is not a source node in the traffic file.")
                    return
                if self.do != "optimize":
                    self.canvas.itemconfig(self.sel_item, fill="red")
                self.prev_item = self.sel_item
                self.prev_type = self.sel_type
                self.prev_x = (self.sel_coor[0] + self.sel_coor[2]) / 2.0
                self.prev_y = (self.sel_coor[1] + self.sel_coor[3]) / 2.0
                # print "first click, item ", self.sel_item, " @ ", self.prev_x, ",", self.prev_y
                self.status.set(self.status_mode + ":" + self.do)
                return
            elif self.do == "select another node...":  # create edge (click on the second node)
                self.canvas.itemconfig(self.sel_item, fill="red")
                if self.prev_item == self.sel_item:
                    self.status.set(self.status_mode + ":" + "no edge created")
                else:  # create edge
                    if not self.topo.has_key(self.node_list[self.sel_item]['name'].values()[0]):
                        self.topo[self.node_list[self.sel_item]['name'].values()[0]] = {}  # create line
                        create_line = True
                    else:  # future work - create multiple fibers on a link
                        if self.topo[self.node_list[self.sel_item]['name'].values()[0]].has_key(
                                self.node_list[self.prev_item]['name'].values()[0]):
                            self.status.set(self.status_mode + ":" + "already created")
                            create_line = False
                        else:
                            create_line = True
                    if create_line:  # CREATE LINE /EDGE
                        curr_x = (self.sel_coor[0] + self.sel_coor[2]) / 2.0  # line position
                        curr_y = (self.sel_coor[1] + self.sel_coor[3]) / 2.0
                        self.edge = self.canvas.create_line(self.prev_x, self.prev_y,
                                                            curr_x, curr_y, fill=self.defaultLineColor, arrow=None,
                                                            width=3)
                        dist_text = '1.0'  # default distance
                        #hidden distance, show working capacity
                        default_wkcap = '100'
                        # self.text = self.canvas.create_text((self.prev_x + curr_x) / 2.0 + 15,  # text position
                        #                                     (self.prev_y + curr_y) / 2.0 + 15, text=dist_text)
                        self.text = self.canvas.create_text((self.prev_x + curr_x) / 2.0 + 15,  # text position
                                                            (self.prev_y + curr_y) / 2.0 + 15, text=default_wkcap)
                        self.edge_list[self.edge] = {}
                        self.edge_list[self.edge]['fromto'] = (self.prev_item, self.sel_item)
                        self.edge_list[self.edge]['distance'] = {}
                        self.edge_list[self.edge]['distance'][self.text] = dist_text
                        print (self.prev_item, self.sel_item)
                        print self.edge_list

                        # UPDATE TOPOLOGY
                        name1 = self.node_list[self.prev_item]['name'].values()[0]
                        name2 = self.node_list[self.sel_item]['name'].values()[0]
                        if not self.topo.has_key(name1):
                            self.topo[name1] = {}
                        self.topo[name1][name2] = 1.0  # from_to
                        if not self.topo.has_key(name2):
                            self.topo[name2] = {}
                        self.topo[name2][name1] = 1.0  # to_from
                        if not self.wave_num.has_key(name1):
                            self.wave_num[name1] = {}
                        self.wave_num[name1][name2] = self.default_wave_num
                        if not self.wave_num.has_key(name2):
                            self.wave_num[name2] = {}
                        self.wave_num[name2][name1] = self.default_wave_num
                        if not self.slot_num.has_key(name1):
                            self.slot_num[name1] = {}
                        self.slot_num[name1][name2] = self.default_slot_num
                        if not self.slot_num.has_key(name2):
                            self.slot_num[name2] = {}
                        self.slot_num[name2][name1] = self.default_slot_num
                        if not self.workcap_num.has_key(name1):
                            self.workcap_num[name1] = {}
                        self.workcap_num[name1][name2] = self.default_workcap_num
                        if not self.workcap_num.has_key(name2):
                            self.workcap_num[name2] = {}
                        self.workcap_num[name2][name1] = self.default_workcap_num
                        if not self.fiber_num.has_key(name1):
                            self.fiber_num[name1] = {}
                        self.fiber_num[name1][name2] = self.default_fiber_num
                        if not self.fiber_num.has_key(name2):
                            self.fiber_num[name2] = {}
                        self.fiber_num[name2][name1] = self.default_fiber_num
                        print "line created ", self.prev_x, self.prev_y, (self.sel_coor[0]
                                                                          + self.sel_coor[2]) / 2.0, (self.sel_coor[1] +
                                                                                                      self.sel_coor[
                                                                                                          3]) / 2.0
                        self.status.set(self.status_mode + ":" + "edge created")
                        self.sel_item = self.edge  # FOR EDITING EDGE ATTRIBUTE
                        self.edit_edge()
                self.do = "edge created"
            elif self.do == "select destination...":
                self.canvas.itemconfig(self.sel_item, fill="red")
                if self.prev_item == self.sel_item:  # SAME NODE
                    self.reset()
                    self.paths = None
                    self.status.set(self.status_mode + ":" + "same node")
                else:  # SHORTEST PATHS
                    self.paths = kshort.kshort(self.topo, self.node_list[self.prev_item]['name'].values()[0],
                                               self.node_list[self.sel_item]['name'].values()[0], 3)
                    # print "path  = " + str(self.paths)
                    self.draw_path()
                self.do = "dijkstra done"
            elif self.do == "select destination node..." and 0:  # 0 - not utilized yet
                src = self.node_list[self.prev_item]['name'].values()[0]
                dst = self.node_list[self.sel_item]['name'].values()[0]
                if self.prev_item == self.sel_item:  # SAME NODE
                    self.canvas.itemconfig(self.sel_item, fill=self.defaultNodeColor)
                    self.paths = None
                    self.status.set(self.status_mode + ":" + "same node")
                elif dst in self.sdlist[src]:  # SHORTEST PATH in Optimization
                    self.drawopt_node_key_press = [self.prev_item, self.sel_item]
                    if self.paths_allo_bw:
                        self.canvas.itemconfig(self.sel_item, fill="red")
                        sd = '(' + src + ',' + dst + ')'
                        self.paths = self.paths_allo_bw[sd]
                        format_path = []
                        for ipath in self.paths:
                            for ilink in self.paths[ipath]['link_list']:
                                node1 = ilink.split(',')[0].split('(')[1]
                                node2 = ilink.split(',')[1].split(')')[0]
                                format_path.append([node1, node2])
                        self.paths[ipath]['link_list'] = format_path
                        # print '>>>>>>>>>>>: ', self.paths
                        # else:
                        # self.paths = kshort.kshort(self.topo,src,dst,1) #XXXXXXXXXXXXXXXX
                        # print '<<<<<<<<<<<" ', self.paths
                        # print "path  = " + str(self.paths)
                        self.draw_path_optshow()
                        self.status.set(self.status_mode + ": " + "shortest path is drawn.")
                else:
                    self.status.set(self.status_mode + ": " + dst + " is not a destination of " + src + ".")
                    self.do == "select destination node..."
                    self.canvas.itemconfig(self.sel_item, fill=self.defaultNodeColor)
                    return
                self.do = "optimize"
        elif self.sel_item and self.sel_type == "line":
            if self.do == None:  # line info
                self.show_info()
            if self.do == "optimize":  # line info
                # reset info frame
                self.reset_opt_info()
                self.frame_link_info_top = Frame(self.scrollframe_info_bottom)
                self.frame_link_info_top.pack(side=TOP, expand=NO, fill=BOTH)
                self.frame_link_info_bottom = Frame(self.scrollframe_info_bottom)
                self.frame_link_info_bottom.pack(side=BOTTOM, expand=NO, fill=BOTH)
                # ---------------------------------------------------------------#
                self.show_common()
                # ---------------------------------------------------------------#
            if self.do == "remove":  # remove edge
                self.canvas.itemconfig(self.sel_item, fill="red")
                self.do = "removed"
            elif self.do == "edit":  # edit edge
                self.prev_item = self.sel_item
                self.edit_edge()
        elif self.do == "create node":  # create node
            self.node = self.canvas.create_oval(self.click_x - 15, self.click_y - 15, self.click_x + 15,
                                                self.click_y + 15, fill="CYAN")
            self.text = self.canvas.create_text(self.click_x, self.click_y + 25, text='A' + str(self.node))
            print self.text
            self.canvas.itemconfig(self.node, tags=self.node)
            self.node_list[self.node] = {}
            self.node_list[self.node]['name'] = {}
            self.node_list[self.node]['name'][self.text] = 'A' + str(self.node)
            self.node_pos[self.node] = self.canvas.coords(self.node)
            self.status.set(self.status_mode + ":" + "node created")
            print self.node_list
            print self.node_pos
            print self.canvas.coords(self.node)
            # for k in range(1,len(self.node_list)):
            for k in self.node_list.keys():
                print self.canvas.coords(k)
                print self.node_pos[k]

    # ------------------------- release ---------------------------------
    def callback_release(self, event):
        self.canvas = event.widget
        self.rel_x = self.canvas.canvasx(event.x)
        self.rel_y = self.canvas.canvasy(event.y)
        # print "released at", x, y
        # self.status.set("released at %d %d",event.x, event.y)
        if self.do:
            print 'action = ', self.do
        else:
            print 'action = Move node'
        if self.do == "removed":
            if self.sel_type == "oval":  # remove node
                if tkMessageBox.askokcancel("Remove node",
                                            "Do you really want to remove selected node?"):
                    edge_remove = []
                    for key in self.edge_list:
                        if self.sel_item in self.edge_list[key]['fromto']:
                            self.canvas.delete(key)  # delete line
                            edge_remove.append(key)
                    for key in edge_remove:
                        link = self.edge_list.pop(key)
                        fromto = link['fromto']
                        distance_id = link['distance'].keys()[0]
                        name1 = self.node_list[fromto[0]]['name'].values()[0]
                        name2 = self.node_list[fromto[1]]['name'].values()[0]
                        if self.topo[name1].has_key(name2):
                            self.topo[name1].pop(name2)
                            self.topo[name2].pop(name1)
                            self.wave_num[name1].pop(name2)
                            self.wave_num[name2].pop(name1)
                            self.slot_num[name1].pop(name2)
                            self.slot_num[name2].pop(name1)
                            self.workcap_num[name1].pop(name2)
                            self.workcap_num[name2].pop(name1)
                            self.fiber_num[name1].pop(name2)
                            self.fiber_num[name2].pop(name1)
                        self.canvas.delete(distance_id)  # delete distance text
                        if not len(self.topo[name1]):
                            self.topo.pop(name1)
                        if not len(self.topo[name2]):
                            self.topo.pop(name2)
                        if not len(self.wave_num[name1]):
                            self.wave_num.pop(name1)
                        if not len(self.wave_num[name2]):
                            self.wave_num.pop(name2)
                        if not len(self.slot_num[name1]):
                            self.slot_num.pop(name1)
                        if not len(self.slot_num[name2]):
                            self.slot_num.pop(name2)
                        if not len(self.workcap_num[name1]):
                            self.workcap_num.pop(name1)
                        if not len(self.workcap_num[name2]):
                            self.workcap_num.pop(name2)
                        if not len(self.fiber_num[name1]):
                            self.fiber_num.pop(name1)
                        if not len(self.fiber_num[name2]):
                            self.fiber_num.pop(name2)
                    self.canvas.delete(self.sel_item)  # delete oval
                    name = self.node_list.pop(self.sel_item)['name'].keys()[0]  # remove from topology
                    self.canvas.delete(name)  # delete node's name text
                    self.node_pos.pop(self.sel_item)  # delete node's position
                    self.status.set(self.status_mode + ":" + "node %d removed", self.sel_item)
                else:
                    self.canvas.itemconfig(self.sel_item, fill="CYAN")
            elif self.sel_type == "line":  # remove edge
                if tkMessageBox.askokcancel("Remove edge",
                                            "Do you really want to remove selected edge?"):
                    link = self.edge_list.pop(self.sel_item)
                    fromto = link['fromto']
                    distance = link['distance'].keys()[0]
                    name1 = self.node_list[fromto[0]]['name'].values()[0]
                    name2 = self.node_list[fromto[1]]['name'].values()[0]
                    self.topo[name1].pop(name2)
                    self.topo[name2].pop(name1)
                    self.wave_num[name1].pop(name2)
                    self.wave_num[name2].pop(name1)
                    self.slot_num[name1].pop(name2)
                    self.slot_num[name2].pop(name1)
                    self.workcap_num[name1].pop(name2)
                    self.workcap_num[name2].pop(name1)
                    self.fiber_num[name1].pop(name2)
                    self.fiber_num[name2].pop(name1)
                    self.canvas.delete(distance)  # delete distance text
                    if not len(self.topo[name1]):
                        self.topo.pop(name1)
                    if not len(self.topo[name2]):
                        self.topo.pop(name2)
                    if not len(self.wave_num[name1]):
                        self.wave_num.pop(name1)
                    if not len(self.wave_num[name2]):
                        self.wave_num.pop(name2)
                    if not len(self.slot_num[name1]):
                        self.slot_num.pop(name1)
                    if not len(self.slot_num[name2]):
                        self.slot_num.pop(name2)
                    if not len(self.workcap_num[name1]):
                        self.workcap_num.pop(name1)
                    if not len(self.workcap_num[name2]):
                        self.workcap_num.pop(name2)
                    if not len(self.fiber_num[name1]):
                        self.fiber_num.pop(name1)
                    if not len(self.fiber_num[name2]):
                        self.fiber_num.pop(name2)
                    self.canvas.delete(self.sel_item)  # delete line
                    self.status.set(self.status_mode + ":" + "edge %d removed", self.sel_item)
                else:
                    self.canvas.itemconfig(self.sel_item, fill=self.defaultLineColor)
            self.do = "remove"  # next remove
        elif self.do == "edge created" and self.sel_type == "oval":  # edge is created
            if self.canvas.type(self.sel_item) == "oval":
                self.canvas.itemconfig(self.sel_item, fill="CYAN")
            self.canvas.itemconfig(self.prev_item, fill="CYAN")
            self.do = "create edge"  # next create edge
        elif self.do == "dijkstra done" and self.sel_type == "oval":  # dijkstra done
            self.canvas.itemconfig(self.sel_item, fill="CYAN")
            self.canvas.itemconfig(self.prev_item, fill="CYAN")
            if self.paths:
                if not self.paths.has_key('link_list'):
                    # for ipath in self.paths:
                    self.status.set(self.status_mode + ":" + 'shortest path = ' + str(self.paths[1]['link_list']) +
                                    '::' + str(self.paths[1]['dist']) + "   select the source...")
                else:
                    self.status.set(self.status_mode + ":" + "select the source...")
            else:
                self.status.set(self.status_mode + ":" + "select the source...")
            self.do = "shortest path"  # next shortest path
        elif self.do == "Move node" and self.sel_type == "oval":  # move node
            if self.rel_x != self.click_x or self.rel_y != self.click_y:
                self.canvas.coords(self.sel_item, self.rel_x - 15, self.rel_y - 15, self.rel_x + 15, self.rel_y + 15)
                self.canvas.coords(self.node_list[self.sel_item]['name'].keys()[0], self.rel_x, self.rel_y + 25)
                self.node_pos[self.sel_item] = self.canvas.coords(self.sel_item)
                for key in self.edge_list:
                    if self.sel_item in self.edge_list[key]['fromto']:
                        coor1 = self.canvas.coords(self.edge_list[key]['fromto'][0])
                        coor2 = self.canvas.coords(self.edge_list[key]['fromto'][1])
                        midx1 = (coor1[0] + coor1[2]) / 2.0
                        midy1 = (coor1[1] + coor1[3]) / 2.0
                        midx2 = (coor2[0] + coor2[2]) / 2.0
                        midy2 = (coor2[1] + coor2[3]) / 2.0
                        self.canvas.coords(key, midx1, midy1, midx2, midy2)  # move line
                        distance_id = self.edge_list[key]['distance'].keys()[0]
                        if midx2 - midx1 != 0:  # text position
                            if (midy2 - midy1) / (midx2 - midx1) >= 0:
                                self.canvas.coords(distance_id, (midx1 + midx2) / 2.0 - 15,
                                                   (midy1 + midy2) / 2.0 + 15)  # move name
                            else:
                                self.canvas.coords(distance_id, (midx1 + midx2) / 2.0 + 15,
                                                   (midy1 + midy2) / 2.0 + 15)  # move name
                        else:
                            self.canvas.coords(distance_id, (midx1 + midx2) / 2.0 + 15,
                                               (midy1 + midy2) / 2.0)  # move name
                print "move ", self.sel_item, " to ", self.canvas.coords(self.sel_item)
                self.status.set(self.status_mode + ":" + "item %d moved", self.sel_item)
            else:
                tkMessageBox.showinfo("OK", self.node_list[self.sel_item]['name'].values()[0])  # show info
            self.canvas.itemconfig(self.sel_item, fill="CYAN")
            self.move_node = None
            self.do = None  # next move node

        print "------------------", self.status_mode, "------------------"
        """
        print "node list:", self.node_list
        print ">>>><<<<"

        print "edge list:", self.edge_list
        print ">>>><<<<"

        print "topology:", self.topo
        print ">>>><<<<"
        """
        """
        print "traffic matrix: ", self.traffic_mat
        print ">>>><<<<"
        print "node position:", self.node_pos

        print ">>>><<<<"
        print "wavelength number:", self.wave_num
        print ">>>><<<<"
        print "slot number:", self.slot_num
        print ">>>><<<<"
        print "fiber number:", self.fiber_num
        """
        if self.add_wave_link:
            print "add wave no.:", self.add_wave_link
            print ">>>><<<<"
        if self.paths_allo_bw:
            print "allocated bandwidth:", self.paths_allo_bw
            print ">>>><<<<"

    # ------------------------- plot trace -------------------------------#
    def draw_path(self):  # SHORTEST PATH
        self.reset()
        self.reset_frame_info()
        if not self.paths.has_key('link_list'):
            color = ['red', 'yellow', 'green', 'blue', 'magenta'][0:len(self.paths.keys())]
            size = [11, 7, 3]
            print 'draw_path color = ', color
            for ipath in self.paths:
                for [node1, node2] in self.paths[ipath]['link_list']:
                    for key in self.edge_list:
                        key1 = self.edge_list[key]['fromto'][0]
                        key2 = self.edge_list[key]['fromto'][1]
                        if node1 in self.node_list[key1]['name'].values() and \
                                        node2 in self.node_list[key2]['name'].values() or \
                                                node1 in self.node_list[key2]['name'].values() and \
                                                node2 in self.node_list[key1]['name'].values():
                            self.canvas.itemconfig(key, fill=color[ipath - 1])  # key start from 1
                            self.draw_path_key.append(self.canvas.create_line(self.canvas.coords(key), \
                                                                              fill=color[ipath - 1], arrow=None,
                                                                              width=size[ipath - 1]))
        self.info_canvas = Canvas(self.scrollframe_info_top, borderwidth=2, relief=RIDGE)

        text = self.info_canvas.create_text(100 + 100, 20, text=self.paths[1]['link_list'][0][0] + \
                                                                " to " + self.paths[1]['link_list'][
                                                                    len(self.paths[1]['link_list']) - 1][1])
        text = self.info_canvas.create_text(30 + 0, 50, text='The shortest path is ', anchor='w')
        ind_txt = 0
        for hop in self.paths[1]['link_list']:
            if ind_txt == 0:
                path = "\"" + hop[0] + "--" + hop[1]
                ind_txt += 1
            else:
                path += "--" + hop[1]
        path += "\" : " + str(self.paths[1]['dist']) + " km"
        text = self.info_canvas.create_text(30 + 0, 70, text=path, anchor='w')

        for i in range(len(color)):
            if i == 0:
                text1 = self.info_canvas.create_text(50, 100 + i * 20, text=str(i + 1) + "st path :")
            elif i == 1:
                text1 = self.info_canvas.create_text(50, 100 + i * 20, text=str(i + 1) + "nd path :")
            elif i == 2:
                text1 = self.info_canvas.create_text(50, 100 + i * 20, text=str(i + 1) + "rd path :")
            else:
                text1 = self.info_canvas.create_text(50, 100 + i * 20, text=str(i + 1) + "th path :")
            edge = self.info_canvas.create_line(93, 103 + i * 20,
                                                200, 103 + i * 20, fill=color[i], arrow=None, width=size[i])
            text2 = self.info_canvas.create_text(200 + 40, 100 + i * 20,
                                                 text=": " + str(self.paths[i + 1]['dist']) + " km")

        self.info_canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        # update the scrollregion
        self.scrollframe_info_top.updateScrollers()

    # --------------------------------------------------------------------#
    def draw_path_optshow(self):  # SHORTEST PATH for optimization
        self.reset_frame_info_bottom()  # reset info frame
        self.info_canvas = Canvas(self.scrollframe_info_bottom, borderwidth=2, relief=RIDGE)
        if self.drawopt_link_key:
            self.drawopt_link_key[self.index] = []
        else:
            self.drawopt_link_key = {}
            self.drawopt_link_key[self.index] = []
        if not self.paths.has_key('link_list'):
            color = ['dark orange', 'dark green']
            size = [8, 5]
            print 'color = ', color
            print self.paths
            icolor = 0
            for ipath in self.paths:
                format_path = []
                bandwidth = self.paths[ipath]['bandwidth']  # added 8/25/2011
                edge = self.info_canvas.create_line(20, 103 + icolor * 20,
                                                    90, 103 + icolor * 20, fill=color[icolor], arrow=None,
                                                    width=size[icolor])
                print 'create line'
                text = self.info_canvas.create_text(130 + 40, 100 + icolor * 20,
                                                    text="Allocated bandwidth (unit):  " + str(bandwidth))
                for [node1, node2] in self.paths[ipath]['link_list']:
                    for key in self.edge_list:
                        key1 = self.edge_list[key]['fromto'][0]
                        key2 = self.edge_list[key]['fromto'][1]
                        if node1 in self.node_list[key1]['name'].values() and \
                                        node2 in self.node_list[key2]['name'].values() or \
                                                node1 in self.node_list[key2]['name'].values() and \
                                                node2 in self.node_list[key1]['name'].values():
                            print '>>>>>>>>link = ', node1, node2
                            # self.canvas.itemconfig(key,fill=color[0]) #key start from 1
                            self.drawopt_link_key[self.index].append(self.canvas.create_line(self.canvas.coords(key), \
                                                                                             fill=color[icolor],
                                                                                             arrow=None,
                                                                                             width=size[icolor]))
                    format_path.append('(' + node1 + ',' + node2 + ')')
                self.paths[ipath]['link_list'] = format_path
                icolor += 1
            self.info_canvas.pack(side=LEFT, expand=YES, fill=BOTH)
            # update the scrollregion
            self.scrollframe_info_bottom.updateScrollers()
            print self.paths

    # --------------------------------------------------------------------#
    def draw_path_opt(self):  # OPTIMIZATION
        max_use = max(self.wave_link.values())
        min_use = min(self.wave_link.values())
        for link in self.wave_link:
            link1 = link.split('(')
            link1 = link1[1].split(')')
            link1 = link1[0].split(',')
            for key in self.edge_list:
                text_key = self.edge_list[key]['distance'].keys()[0]
                self.canvas.itemconfig(text_key, state=HIDDEN)
                node1 = self.node_list[self.edge_list[key]['fromto'][0]]['name'].values()
                node2 = self.node_list[self.edge_list[key]['fromto'][1]]['name'].values()
                if not self.wave_link_use.has_key(node1[0]):
                    self.wave_link_use[node1[0]] = {}
                if not self.wave_link_use.has_key(node2[0]):
                    self.wave_link_use[node2[0]] = {}
                if not self.wave_link_use[node1[0]].has_key(node2[0]):
                    self.wave_link_use[node1[0]][node2[0]] = 0
                if not self.wave_link_use[node2[0]].has_key(node1[0]):
                    self.wave_link_use[node2[0]][node1[0]] = 0
                if link1[0] in node1 and link1[1] in node2 or link1[0] in node2 and link1[1] in node1:
                    if link1[0] in node1 and link1[1] in node2:
                        self.wave_link_use[node1[0]][node2[0]] = self.wave_link[link]
                        pct = 100.0 * self.wave_link_use[node1[0]][node2[0]] / self.wave_num[node1[0]][node2[0]]
                    elif link1[0] in node2 and link1[1] in node1:
                        self.wave_link_use[node2[0]][node1[0]] = self.wave_link[link]
                        pct = 100.0 * self.wave_link_use[node2[0]][node1[0]] / self.wave_num[node2[0]][node1[0]]
                    if pct >= 0.0 and pct <= 25.0:
                        self.canvas.itemconfig(key, fill='black')  # 0-25%
                    elif pct > 25.0 and pct <= 50.0:
                        self.canvas.itemconfig(key, fill='blue')  # 26-50%
                    elif pct > 51.0 and pct <= 75.0:
                        self.canvas.itemconfig(key, fill='magenta')  # 51-75%
                    elif pct > 75.0 and pct <= 100.0:
                        self.canvas.itemconfig(key, fill='red')  # 76-100%
                        # else:
                        # self.canvas.itemconfig(key,fill=self.royalblue)
                        # if link1[0] in node1 and link1[1] in node2:
                        #   self.wave_link_use[node1[0]][node2[0]] = self.wave_link[link]
                        # if link1[0] in node2 and link1[1] in node1:
                        #   self.wave_link_use[node2[0]][node1[0]] = self.wave_link[link]
        text_key_add = []
        for link in self.add_wave_link:  # SHOWING ADDITIONAL WAVELENGTH NEEDED
            link1 = link.split('(')
            link1 = link1[1].split(')')
            link1 = link1[0].split(',')
            for key in self.edge_list:
                text_key = self.edge_list[key]['distance'].keys()[0]
                node1 = self.node_list[self.edge_list[key]['fromto'][0]]['name'].values()
                node2 = self.node_list[self.edge_list[key]['fromto'][1]]['name'].values()
                if (link1[0] in node1 and link1[1] in node2) or (link1[0] in node2 and link1[1] in node1):
                    if text_key in text_key_add:
                        [coorx, corry] = self.canvas.coords(text_key)
                        self.draw_addwave_key.append(self.canvas.create_text([coorx + 10, corry], \
                                                                             text=" , " + str(self.add_wave_link[link]),
                                                                             fill="red"))
                    else:
                        self.draw_addwave_key.append(self.canvas.create_text(self.canvas.coords(text_key), \
                                                                             text=str(self.add_wave_link[link]),
                                                                             fill="red"))
                    text_key_add.append(text_key)
        if self.draw_addwave_key:
            self.draw_addwave_key.append(self.canvas.create_text([400, 25], \
                                                                 text="ADDITIONAL WAVELENGTHS NEEDED", fill="red"))
        self.add_legend()
        # self.top_opt2.focus
        print "wave_link_use --->", self.wave_link_use

    # --------------------------------------------------------------------#
    def show_path_opt(self):  # added 8/25/2011
        delete_key = []
        if self.drawopt_link_key:  # clear paths
            for ind_key in self.drawopt_link_key:
                delete_key.append(ind_key)
                for key in self.drawopt_link_key[ind_key]:
                    self.canvas.delete(key)
        ind = self.var_showpath.get()
        print 'draw...............  ', self.source[ind], '-', self.destination[ind]
        src = self.source[ind]
        dst = self.destination[ind]
        self.index = ind
        for inode in self.node_list:
            if self.node_list[inode]['name'] == src:
                self.prev_item = inode
            if self.node_list[inode]['name'] == dst:
                self.sel_item = inode
        if self.paths_allo_bw:
            sd = '(' + src + ',' + dst + ')'
            self.paths = self.paths_allo_bw[sd]
            print 'spilt = ', self.var_trafsplit.get()
            for ipath in self.paths:
                format_path = []
                for ilink in self.paths[ipath]['link_list']:
                    node1 = ilink.split(',')[0].split('(')[1]
                    node2 = ilink.split(',')[1].split(')')[0]
                    format_path.append([node1, node2])
                self.paths[ipath]['link_list'] = format_path
            self.draw_path_optshow()
            self.status.set(self.status_mode + ": " + "path is drawn.")
        print 'draw path(s) = ', self.drawopt_link_key

    # --------------------------------------------------------------------#
    def add_legend(self):  # LEGEND
        icolor = ['black', 'blue', 'magenta', 'red']
        isize = [3, 3, 3, 3]
        self.add_legend_key.append(self.canvas.create_text([700, 25], \
                                                           text="WAVELENGTH UTILIZATION", fill="red"))
        itext = ['0-25%', '26-50%', '51-75%', '76-100%']
        for i in range(len(icolor)):
            edge = self.canvas.create_line(700, 55 + i * 20, 725, 55 + i * 20, fill=icolor[i], arrow=None,
                                           width=isize[i])
            text = self.canvas.create_text(700 + 50, 55 + i * 20, text=itext[i])
            self.add_legend_key.append(edge)
            self.add_legend_key.append(text)

    # --------------------------------------------------------------------#
    def reset(self):  # RESET TOPOLOGY
        if self.node_list:  # reset all nodes
            for inode in self.node_list:
                self.canvas.itemconfig(inode, fill=self.defaultNodeColor)
        if self.edge_list:  # reset all edges
            for ilink in self.edge_list:
                self.canvas.itemconfig(ilink, fill=self.defaultLineColor, width=3)  # Line
                self.canvas.itemconfig(self.edge_list[ilink]['distance'].keys()[0], \
                                       fill=self.defaultLineColor, state=NORMAL)  # Text on Line
        if self.draw_path_key:  # delete colored lines - SHORTEST PATH
            for key in self.draw_path_key:
                self.canvas.delete(key)
        if self.draw_addwave_key:
            for key in self.draw_addwave_key:
                self.canvas.delete(key)
        if self.add_legend_key:
            for key in self.add_legend_key:
                self.canvas.delete(key)
        self.draw_path_key = []
        self.wave_link_use = {}
        self.draw_addwave_key = []
        self.add_legend_key = []
        self.trf_split = 0
        self.canvas.delete('self.text')
        # ----- optimization ----#
        delete_key = []
        if self.drawopt_link_key:  # clear paths
            for ind_key in self.drawopt_link_key:
                delete_key.append(ind_key)
                for key in self.drawopt_link_key[ind_key]:
                    self.canvas.delete(key)
        self.drawopt_link_key = None
        self.paths_allo_bw = None
        self.wave_link = None
        self.add_wave_link = None

    # --------------------------------------------------------------------#
    def reset_frame_info_top(self):  # RESET INFORMATION FRAME (TOP)
        if self.frame_opt:
            self.frame_opt.destroy()
        if self.radio_opt:
            self.radio_opt.destroy()
        if self.toolbar_opt:
            self.toolbar_opt.destroy()
        if self.frame_link_info_top:
            self.frame_link_info_top.destroy()
        if self.frame_link_info_bottom:
            self.frame_link_info_bottom.destroy()
        if self.frame_link_edit_top:
            self.frame_link_edit_top.destroy()
        if self.frame_link_edit_bottom:
            self.frame_link_edit_bottom.destroy()
        if self.toolbar_link_edit:
            self.toolbar_link_edit.destroy()
        if self.info_canvas:
            self.info_canvas.destroy()

    def reset_frame_info_bottom(self):  # RESET INFORMATION FRAME (BOTTOM)
        if self.frame_link_info_topmost:
            self.frame_link_info_topmost.destroy()
        if self.frame_link_info_top:
            self.frame_link_info_top.destroy()
        if self.frame_link_info_bottom:
            self.frame_link_info_bottom.destroy()
        if self.info_canvas:
            self.info_canvas.destroy()
        if self.toolbar_check_cycle:
            self.toolbar_check_cycle.destroy()
        #if self.

    def reset_frame_info(self):  # RESET INFORMATION FRAME (ALL)
        self.reset_frame_info_top()
        self.reset_frame_info_bottom()

    def reset_opt_info(self):  # RESET INFORMATION FRAME (For optimization)
        if self.frame_link_info_top:
            self.frame_link_info_top.destroy()
        if self.frame_link_info_bottom:
            self.frame_link_info_bottom.destroy()

    # --------------------------------------------------------------------#
    def callback_update_link(self):
        # UPDATE TOPOLOGY
        key = self.edge_list[self.sel_item]['distance'].keys()[0]
        node1 = self.edge_list[self.sel_item]['fromto'][0]
        node2 = self.edge_list[self.sel_item]['fromto'][1]
        name1 = self.node_list[node1]['name'].values()[0]
        name2 = self.node_list[node2]['name'].values()[0]
        change = True
        if self.is_numeric(self.e1[0].get()):
            self.canvas.itemconfig(key, text=self.e1[0].get())
            self.edge_list[self.sel_item]['distance'][key] = float(self.e1[0].get())
            self.topo[name1][name2] = float(self.e1[0].get())
            self.topo[name2][name1] = float(self.e1[0].get())
        else:
            change = False
        if self.is_numeric(self.e1[3].get()):
            self.wave_num[name1][name2] = int(float(self.e1[3].get()))
        else:
            change = False
        if self.is_numeric(self.e2[2].get()):
            self.wave_num[name2][name1] = int(float(self.e2[2].get()))
        else:
            change = False
        if self.is_numeric(self.e1[4].get()):
            self.slot_num[name1][name2] = int(float(self.e1[4].get()))
        else:
            change = False
        if self.is_numeric(self.e2[3].get()):
            self.slot_num[name2][name1] = int(float(self.e2[3].get()))
        else:
            change = False
        if self.is_numeric(self.e1[5].get()):
            self.canvas.itemconfig(key, text=self.e1[5].get())
            self.workcap_num[name1][name2] = int(float(self.e1[5].get()))
        else:
            change = False
        if self.is_numeric(self.e2[4].get()):
            self.canvas.itemconfig(key, text=self.e2[4].get())
            self.workcap_num[name2][name1] = int(float(self.e2[4].get()))
        else:
            change = False
        if self.is_numeric(self.e1[2].get()):
            self.fiber_num[name1][name2] = int(float(self.e1[2].get()))
        else:
            change = False
        if self.is_numeric(self.e2[1].get()):
            self.fiber_num[name2][name1] = int(float(self.e2[1].get()))
        else:
            change = False
        if change:
            tkMessageBox.showinfo("OK", "information on link between " + name1 + " and " + name2 + " has been changed.")
            # --------------------------------------------------------------------#

    def callback_edittrf(self):
        if os.name == 'nt':
            os.system('notepad.exe ' + self.filename)  # open file by notepad
        elif os.name == 'posix':
            os.system('emacs ' + self.filename)  # open file by emacs
        self.opt_show_top_frame(1)

    # --------------------------------------------------------------------#
    def edit_edge(self):
        if self.status_mode == 'EDIT ATTRIBUTE':
            self.status.set(self.status_mode + ":" + "edit edge's attribute")
        else:
            self.status.set(self.status_mode + ":" + "edit edge's attribute or select a node")
        self.canvas.itemconfig(self.sel_item, fill="red")
        distance_id = self.edge_list[self.sel_item]['distance'].keys()[0]
        node1 = self.edge_list[self.sel_item]['fromto'][0]
        node2 = self.edge_list[self.sel_item]['fromto'][1]
        name1 = self.node_list[node1]['name'].values()[0]
        name2 = self.node_list[node2]['name'].values()[0]
        self.reset_frame_info()  # reset info frame
        self.reset()
        self.frame_link_edit_top = Frame(self.scrollframe_info_top)
        self.frame_link_edit_bottom = Frame(self.scrollframe_info_top)
        self.toolbar_link_edit = Frame(self.scrollframe_info_top, borderwidth=2, relief=RIDGE, background="tan")
        self.frame_link_edit_top.pack(side=TOP, expand=NO, fill=BOTH)
        self.frame_link_edit_bottom.pack(side=TOP, expand=NO, fill=BOTH)
        self.toolbar_link_edit.pack(side=BOTTOM, expand=NO, fill=BOTH)
        # --------------------#
        self.e1 = []
        self.labelText = ["distance (km)", name1 + "-" + name2, "No. of fibers", "capacity (wavelengths/fiber)", \
                          "capacity (slots/fiber)","working capacity"]
        distance = self.edge_list[self.sel_item]['distance'][distance_id]
        self.dialogText = [distance, distance]
        self.dialogText.append(self.fiber_num[name1][name2])
        self.dialogText.append(self.wave_num[name1][name2])
        self.dialogText.append(self.slot_num[name1][name2])
        self.dialogText.append(self.workcap_num[name1][name2])

        for i in range(len(self.labelText)):
            Label(self.frame_link_edit_top, text=self.labelText[i]).grid(row=i)
            self.e1.append(None)
            if i != 1:
                self.e1[i] = Entry(self.frame_link_edit_top)
                self.e1[i].insert(0, self.dialogText[i])
                self.e1[i].grid(row=i, column=1)
        # --------------------#
        self.e2 = []
        self.labelText = [name2 + "-" + name1, "No. of fibers", "capacity (wavelengths/fiber)", \
                          "capacity (slots/fiber)","working capacity"]
        self.dialogText = [distance]
        self.dialogText.append(self.fiber_num[name2][name1])
        self.dialogText.append(self.wave_num[name2][name1])
        self.dialogText.append(self.slot_num[name2][name1])
        self.dialogText.append(self.workcap_num[name2][name1])
        for i in range(len(self.labelText)):
            Label(self.frame_link_edit_bottom, text=self.labelText[i]).grid(row=i)
            self.e2.append(None)
            if i > 0:
                self.e2[i] = Entry(self.frame_link_edit_bottom)
                self.e2[i].insert(0, self.dialogText[i])
                self.e2[i].grid(row=i, column=1)
        # ------------------#
        self.b1_link_edit = Button(self.toolbar_link_edit, text="update", width=6,
                                   command=self.callback_update_link)
        self.b1_link_edit.pack(side=TOP, padx=2, pady=2)
        self.canvas.itemconfig(self.sel_item, fill='#FF0000')
        # update the scrollregion
        self.scrollframe_info_top.updateScrollers()

    # --------------------------------------------------------------------#
    def show_info(self):
        self.reset_frame_info()  # reset info frame
        self.reset()
        self.frame_link_info_top = Frame(self.scrollframe_info_top)
        self.frame_link_info_top.pack(side=TOP, expand=NO, fill=BOTH)
        self.frame_link_info_bottom = Frame(self.scrollframe_info_top)
        self.frame_link_info_bottom.pack(side=BOTTOM, expand=NO, fill=BOTH)
        # -----------------#
        self.show_common()
        self.canvas.itemconfig(self.sel_item, fill='#FF0000')
        # --------------------------------------------------------------------#

    def show_common(self):
        self.status.set(self.status_mode + " show info")
        # prev_color=self.canvas.itemcget(self.sel_item,"fill")
        distance_id = self.edge_list[self.sel_item]['distance'].keys()[0]
        node1 = self.edge_list[self.sel_item]['fromto'][0]
        node2 = self.edge_list[self.sel_item]['fromto'][1]
        name1 = self.node_list[node1]['name'].values()[0]
        name2 = self.node_list[node2]['name'].values()[0]
        if self.do == "optimize":
            self.labelText = ["distance (km)", name1 + "-" + name2, "Wavelength Utilization",
                              "Additional Wavelengths Needed"]

            distance = self.edge_list[self.sel_item]['distance'][distance_id]
            self.dialogText = [distance, distance]
            if self.wave_link_use:
                if not self.wave_link_use[name1][name2]:
                    self.dialogText.append('-')
                else:
                    self.dialogText.append(
                        str(100.0 * self.wave_link_use[name1][name2] / self.wave_num[name1][name2]) + '%')
            else:
                self.dialogText.append('-')
            if self.add_wave_link:
                if '(' + name1 + ',' + name2 + ')' in self.add_wave_link:
                    self.dialogText.append(self.add_wave_link['(' + name1 + ',' + name2 + ')'])
                else:
                    self.dialogText.append('-')
            else:
                self.dialogText.append('-')
            vpath = '(' + name1 + ',' + name2 + ')'
            """
            if self.paths_allo_bw:
               for sd in self.paths_allo_bw:
                  if self.paths_allo_bw[sd].has_key(1):
                     if vpath in self.paths_allo_bw[sd][1]['link_list']:
                        spath = self.paths_allo_bw[sd][1]['link_list']
                        print '1-shortest path draw = ', spath
            self.dialogText.append('-')
            """
            i = 0
            for nName in self.labelText:
                if i == 1:
                    Label(self.frame_link_info_top, text="-----------------------------").grid(row=i)
                    i += 1
                    Label(self.frame_link_info_top, text=nName).grid(row=i)
                else:
                    Label(self.frame_link_info_top, text=nName).grid(row=i)
                    Label(self.frame_link_info_top, text=" : ").grid(row=i, column=1)
                    Label(self.frame_link_info_top, text=self.dialogText[self.labelText.index(nName)]).grid(row=i,
                                                                                                            column=2)
                i += 1
            self.labelText = [name2 + "-" + name1, "Wavelength Utilization", "Additional Wavelengths Needed"]
            self.dialogText = [distance]
            if self.wave_link_use:
                if not self.wave_link_use[name2][name1]:
                    self.dialogText.append('-')
                else:
                    self.dialogText.append(
                        str(100.0 * self.wave_link_use[name2][name1] / self.wave_num[name2][name1]) + '%')
            else:
                self.dialogText.append('-')
            if self.add_wave_link:
                if '(' + name2 + ',' + name1 + ')' in self.add_wave_link:
                    self.dialogText.append(self.add_wave_link['(' + name2 + ',' + name1 + ')'])
                else:
                    self.dialogText.append('-')
            else:
                self.dialogText.append('-')
            Label(self.frame_link_info_bottom, text="--------------------------").grid(row=0)
            i = 1
            for nName in self.labelText:
                if i > 1:
                    Label(self.frame_link_info_bottom, text=nName).grid(row=i)
                    Label(self.frame_link_info_bottom, text=" : ").grid(row=i, column=1)
                    Label(self.frame_link_info_bottom, text=self.dialogText[self.labelText.index(nName)]).grid(row=i,
                                                                                                               column=2)
                else:
                    Label(self.frame_link_info_bottom, text=nName).grid(row=i, column=0)
                i += 1
        # END OPTIMIZATION
        else:
            self.labelText = ["distance (km)", name1 + "-" + name2, "No. of fibers", "capacity (wavelengths/fiber)", \
                              "capacity (slots/wavelength)", "Wavelength Utilization","working capacity"]
            distance = self.edge_list[self.sel_item]['distance'][distance_id]
            self.dialogText = [distance, distance]
            self.dialogText.append(self.fiber_num[name1][name2])
            self.dialogText.append(self.wave_num[name1][name2])
            self.dialogText.append(self.slot_num[name1][name2])
            self.dialogText.append(self.workcap_num[name1][name2])
            if self.wave_link_use:
                if not self.wave_link_use[name1][name2]:
                    self.dialogText.append('-')
                else:
                    self.dialogText.append(
                        str(100.0 * self.wave_link_use[name1][name2] / self.wave_num[name1][name2]) + '%')
            else:
                self.dialogText.append('-')
            i = 0
            for nName in self.labelText:
                if i == 1:
                    Label(self.frame_link_info_top, text="-----------------------------").grid(row=i)
                    i += 1
                    Label(self.frame_link_info_top, text=nName).grid(row=i)
                else:
                    Label(self.frame_link_info_top, text=nName).grid(row=i)
                    Label(self.frame_link_info_top, text=" : ").grid(row=i, column=1)
                    Label(self.frame_link_info_top, text=self.dialogText[self.labelText.index(nName)]).grid(row=i,
                                                                                                            column=2)
                i += 1
            self.labelText = [name2 + "-" + name1, "No. of fibers", "capacity (wavelengths/fiber)", \
                              "capacity (slots/fiber)", "Wavelength Utilization","working capacity"]
            self.dialogText = [distance]
            self.dialogText.append(self.fiber_num[name2][name1])
            self.dialogText.append(self.wave_num[name2][name1])
            self.dialogText.append(self.slot_num[name2][name1])
            self.dialogText.append(self.workcap_num[name1][name2])
            if self.wave_link_use:
                if not self.wave_link_use[name2][name1]:
                    self.dialogText.append('-')
                else:
                    self.dialogText.append(
                        str(100.0 * self.wave_link_use[name2][name1] / self.wave_num[name2][name1]) + '%')
            else:
                self.dialogText.append('-')
            Label(self.frame_link_info_bottom, text="--------------------------").grid(row=0)

            i = 1
            for nName in self.labelText:
                if i > 1:
                    Label(self.frame_link_info_bottom, text=nName).grid(row=i)
                    Label(self.frame_link_info_bottom, text=" : ").grid(row=i, column=1)
                    Label(self.frame_link_info_bottom, text=self.dialogText[self.labelText.index(nName)]).grid(row=i,
                                                                                                               column=2)
                else:
                    Label(self.frame_link_info_bottom, text=nName).grid(row=i, column=0)
                i += 1
        # update the scrollregion
        self.scrollframe_info_top.updateScrollers()
        self.scrollframe_info_bottom.updateScrollers()

    # ===========================================================================================#
    # choice 1: initial; show 2 radiobuttons, read data from file
    #        2: show 2 radiobuttons, existing data
    #        3: show 3 radiobuttons, exisiing data
    def opt_show_top_frame(self, choice):
        radio_choice = choice
        self.sdlist = {}
        if choice < 2:
            radio_choice = 2
        if self.filename:
            print "------------------------ optimize -----------------------"
            # ------------------- OPTIMIZATION WINDOW ----------------------------#
            self.reset_frame_info()  # reset info frame
            # self.frame_opt = Frame(self.info_frame_top)
            # self.radio_opt = Frame(self.info_frame_top)
            # self.toolbar_opt = Frame(self.info_frame_top,borderwidth=2,relief=RIDGE,background="tan")
            self.frame_opt = Frame(self.scrollframe_info_top)
            self.radio_opt = Frame(self.scrollframe_info_top)
            self.toolbar_opt = Frame(self.scrollframe_info_top, borderwidth=2, relief=RIDGE)

            self.b1_opt = Button(self.toolbar_opt, text="run", width=6, command=self.callback_opt_optimize,
                                 relief=GROOVE)
            self.b1_opt.pack(side=LEFT, padx=2, pady=2)
            self.b2_opt = Button(self.toolbar_opt, text="open", width=6, command=self.callback_opt_open, relief=GROOVE)
            self.b2_opt.pack(side=LEFT, padx=2, pady=2)
            self.b2_opt = Button(self.toolbar_opt, text="edit traffic file", width=10, command=self.callback_edittrf,
                                 relief=GROOVE)
            self.b2_opt.pack(side=LEFT, padx=2, pady=2)

            choice_opt = [('Minimize number of utilized wavelength channels', 1),
                          ('Maximize number of supported traffic units', 2), \
                          ('Minimize the additional wavelength channels', 3)]
            # choice_split = [('Allow traffic splitting',1), ('No traffic splitting',2)]
            self.var_objcri = IntVar()  # objective selection variable
            for text, value in choice_opt:
                if value <= radio_choice:
                    Radiobutton(self.radio_opt, text=text, value=value, \
                                variable=self.var_objcri, state=NORMAL).pack(anchor=W)
                else:
                    Radiobutton(self.radio_opt, text=text, value=value, \
                                variable=self.var_objcri, state=DISABLED).pack(anchor=W)
            self.var_objcri.set(1)  # set - objective selection variable
            self.var_trafsplit = IntVar()  # traffic splitting selection variable
            self.var_trafsplit.set(self.trf_split)  # set - traffic splitting selection variable
            Checkbutton(self.radio_opt, text="Traffic splitting allowed", variable=self.var_trafsplit).pack()

            self.var_showpath = IntVar()  # added 25AUG2011 #used path selection variable
            Label(self.frame_opt, text="source").grid(row=0, column=0)
            Label(self.frame_opt, text="destination").grid(row=0, column=2)
            Label(self.frame_opt, text="show path").grid(row=0, column=3)
            Label(self.frame_opt, text="traffic (unit)").grid(row=0, column=4)
            self.e = []
            self.s = []
            self.d = []
            self.e.append(None)
            self.s.append(None)
            self.d.append(None)
            name_list = self.topo.keys()
            err_count = 0
            if choice < 2:
                self.traffic_mat = {}
            i = 0
            f = open(self.filename, 'r')
            for line in f:
                sline = line.split(',')
                format_err = 0
                if len(sline) == 4:
                    i += 1
                    self.s.append(None)
                    self.d.append(None)
                    self.e.append(None)
                    self.s[i] = StringVar()
                    self.d[i] = StringVar()
                    self.s[i].set(sline[0])
                    self.d[i].set(sline[1])
                    if self.s[i].get() in name_list and self.d[i].get() in name_list:
                        Label(self.frame_opt, textvariable=self.s[i]).grid(row=i, column=0)  # source
                        Label(self.frame_opt, text="-").grid(row=i, column=1)
                        Label(self.frame_opt, textvariable=self.d[i]).grid(row=i, column=2)  # destination
                        self.source.append(self.s[i].get())
                        self.destination.append(self.d[i].get())
                        Radiobutton(self.frame_opt, text='', value=i - 1, \
                                    variable=self.var_showpath, state=NORMAL, command=self.show_path_opt).grid(row=i,
                                                                                                               column=3)  # added 8/25/2011
                        self.e[i] = Entry(self.frame_opt)  # distance
                        if choice < 2:
                            self.e[i].insert(0, sline[2])  # TRAFFIC
                            if not self.traffic_mat.has_key(sline[0]):
                                self.traffic_mat[sline[0]] = {}
                            self.traffic_mat[sline[0]][sline[1]] = int(sline[2])
                        else:
                            self.e[i].insert(0, self.traffic_mat[sline[0]][sline[1]])  # TRAFFIC
                        self.e[i].grid(row=i, column=4)  # edited 14AUG2011
                        if self.sdlist.has_key(self.s[i].get()):  # added 5/26/2011
                            self.sdlist[self.s[i].get()].append(self.d[i].get())
                        else:
                            self.sdlist[self.s[i].get()] = []
                            self.sdlist[self.s[i].get()].append(self.d[i].get())
                    else:
                        err_count += 1
                        i -= 1
                        self.s.pop(len(self.s) - 1)
                        self.d.pop(len(self.d) - 1)
                        self.e.pop(len(self.e) - 1)
                elif len(sline) > 1:
                    format_err = 1
            if format_err:
                tkMessageBox.showwarning("Error detected!!!", "Please check traffic file's format.")  # show info
            if err_count:
                tkMessageBox.showwarning("Error detected!!!",
                                         "Discard " + str(err_count) + " demand(s)\check nodes' name")  # show info
            # print 'sd_list:::::>', self.sdlist
            f.close()
            self.toolbar_opt.pack()
            self.radio_opt.pack()
            self.frame_opt.pack()
            # update the scrollregion
            self.scrollframe_info_top.updateScrollers()
            self.status.set(self.status_mode + ":" + " traffic loaded...")
            print self.traffic_mat

    def is_integer(self, x):
        try:
            int(x)
        except ValueError:
            tkMessageBox.showerror("Error detected!!!", "Only integer for traffic matrix")  # show info
            return False
        else:
            return True

    def is_numeric(self, x):
        try:
            float(x)
        except ValueError:
            tkMessageBox.showerror("Error detected!!!", "Only number allowed")  # show info
            return False
        else:
            return True

#creating the grid space
        # jump_space = 20
        # stored_node_coor = []
        # grid_num_x = range(2,500/jump_space+1)
        # grid_num_y = range(2,300/jump_space+1)
        #step 1: scatter from designed number of nodes
        # while len(self.node_list) < self.node_num:
        #     rand_grid_x = random.choice(grid_num_x)
        #     rand_grid_y = random.choice(grid_num_y)
        #     self.click_x = rand_grid_x*jump_space
        #     self.click_y = rand_grid_y*jump_space
        #     if (self.click_x,self.click_y) not in stored_node_coor:
        #         stored_node_coor.append((self.click_x,self.click_y))
        #         self.node = self.canvas.create_oval(self.click_x - 7, self.click_y - 7, self.click_x + 7,
        #                                             self.click_y + 7, fill="CYAN")
        #         self.text = self.canvas.create_text(self.click_x, self.click_y + 12, text=str(self.node))
        #         self.canvas.itemconfig(self.node, tags=self.node)
        #         self.node_list[self.node] = {}
        #         self.node_list[self.node]['name'] = {}
        #         self.node_list[self.node]['name'][self.text] = 'A' + str(self.node)
        #         self.node_pos[self.node] = self.canvas.coords(self.node)
        #         self.status.set(self.status_mode + ":" + "node created")
        #         node_degree[self.node] = 0
        # candidate_nodes = self.node_list.keys()
        # topo = {}
        # for i in candidate_nodes:
        #     topo[i] = []
        # L = 19 # locality < 20 (unit)
        # target_dist = {0: 0, 1: 0, 2: 22.5, 3: 43.1, 4: 16.1, 5: 11.8, 6: 5.4, 7: 1.1}
        # current_dist = {0: len(self.node_list), 1:0, 2: 0, 3:0, 4:0, 5:0, 6:0, 7:0}
        # target_dist_upper = {}
        # total_link = 0
        # for i in target_dist.keys():
        #     target_dist_upper[i] = math.ceil(len(candidate_nodes)*target_dist[i]/100)
        #     #target_dist_lower[i] = math.floor(len(candidate_nodes)*target_dist[i]/100)
        #     total_link = total_link + i*target_dist_upper[i]
        # print "total link", total_link
        # #step 2: do round-robin
        # #for curr_node in self.node_list.keys():
        # index = -1
        # list_node = []
        # for i in self.node_list.keys():
        #     list_node.append(i)
        # while len(self.edge_list) < total_link:
        #     index += 1
        #     index = index % len(self.node_list.keys())
        #     curr_node = list_node[index]
        #     prev_x = (self.node_pos[curr_node][0] + self.node_pos[curr_node][2]) / 2.0
        #     prev_y = (self.node_pos[curr_node][1] + self.node_pos[curr_node][3]) / 2.0
        #     print "curr node coor", (prev_x, prev_y)
        #     rand_angle = random.randrange(0,360)
        #     #find that end_point
        #     if rand_angle >= 0 and rand_angle <= 180:
        #         end_point_x = prev_x + L*math.cos(rand_angle)
        #         end_point_y = prev_y + L*math.sin(rand_angle)
        #     if rand_angle >180 and rand_angle <=360:
        #         end_point_x = prev_x - L * math.cos(rand_angle)
        #         end_point_y = prev_y + L * math.sin(rand_angle)
        #     # self.edge = self.canvas.create_line(prev_x, prev_y,
        #     #                                     end_point_x, end_point_y, fill="red",
        #     #                                     arrow=LAST,
        #     #                                     width=1)
        #     # round end point to list of predefined nodes
        #     distance = {}
        #     for cand_neib in self.node_list.keys():
        #         cand_x = (self.node_pos[cand_neib][0] + self.node_pos[cand_neib][2]) / 2.0
        #         cand_y = (self.node_pos[cand_neib][1] + self.node_pos[cand_neib][3]) / 2.0
        #         if cand_neib != curr_node:
        #             if cand_neib not in topo[curr_node]:
        #                 distance[cand_neib]  = math.hypot((end_point_x - cand_x), (end_point_y - cand_y))
        #     # sort to find the closest node on grid
        #     sorted_distance = sorted(distance.items(), key=operator.itemgetter(1))
        #     print sorted_distance
        #     neib_node = sorted_distance[0][0]
        #     # choosen_x = (self.node_pos[neib_node][0] + self.node_pos[neib_node][2]) / 2.0
        #     # choosen_y = (self.node_pos[neib_node][1] + self.node_pos[neib_node][3]) / 2.0
        #     # self.edge = self.canvas.create_line(prev_x, prev_y,
        #     #     choosen_x, choosen_y, fill=self.defaultLineColor,
        #     #     arrow=None,
        #     #     width=1)
        #     # topo[curr_node].append(neib_node)
        #     # topo[neib_node].append(curr_node)
        #     # self.edge_list[self.edge] = {}
        #     # self.edge_list[self.edge]['fromto'] = (curr_node, neib_node)
        #     # self.edge_list[self.edge]['distance'] = {}
        #     # self.edge_list[self.edge]['distance'][self.text] = float('0')
        #
        #
        #     print "node_degree", node_degree
        #     print "current_dist", current_dist
        #     print "target upper", target_dist_upper
        #     update_current_dist = {}
        #     for deg in target_dist.keys():
        #         update_current_dist[deg] = current_dist[deg]
        #     update_current_dist[node_degree[curr_node]] -= 1
        #     update_current_dist[node_degree[curr_node]+1] += 1
        #     update_current_dist[node_degree[neib_node]] -= 1
        #     update_current_dist[node_degree[neib_node]+1] += 1
        #     exceed_target = NO
        #     for deg in target_dist.keys():
        #         if deg>= 2:
        #             if update_current_dist[deg] > target_dist_upper[deg]:
        #                 exceed_target = YES
        #     if exceed_target == NO:
        #         choosen_x = (self.node_pos[neib_node][0] + self.node_pos[neib_node][2]) / 2.0
        #         choosen_y = (self.node_pos[neib_node][1] + self.node_pos[neib_node][3]) / 2.0
        #         self.edge = self.canvas.create_line(prev_x, prev_y,
        #                                             choosen_x, choosen_y, fill=self.defaultLineColor,
        #                                             arrow=None,
        #                                             width=1)
        #         node_degree[curr_node] += 1
        #         node_degree[neib_node] += 1
        #         topo[curr_node].append(neib_node)
        #         topo[neib_node].append(curr_node)
        #         self.edge_list[self.edge] = {}
        #         self.edge_list[self.edge]['fromto'] = (curr_node, neib_node)
        #         self.edge_list[self.edge]['distance'] = {}
        #         self.edge_list[self.edge]['distance'][self.text] = float('0')
        #         for deg in target_dist.keys():
        #             current_dist[deg] = update_current_dist[deg]


# while len(self.node_list) < self.node_num:
        #     self.click_x = random.randint(20, 780)
        #     self.click_y = random.randint(20, 500)
        #     self.node = self.canvas.create_oval(self.click_x - 15, self.click_y - 15, self.click_x + 15,
        #                                     self.click_y + 15, fill="CYAN")
        #     self.text = self.canvas.create_text(self.click_x, self.click_y + 12, text = str(self.node))
        #     self.canvas.itemconfig(self.node, tags=self.node)
        #     self.node_list[self.node] = {}
        #     self.node_list[self.node]['name'] = {}
        #     self.node_list[self.node]['name'][self.text] = 'A' + str(self.node)
        #     self.node_pos[self.node] = self.canvas.coords(self.node)
        #     self.status.set(self.status_mode + ":" + "node created")
        #     node_degree[self.node]=0
        # candidate_nodes = self.node_list.keys()

# backup files for the above files 
import numpy as np
import math
import heapq
import pygame ,sys
from queue import PriorityQueue
import cv2
import os

map_width = 1200
map_height = 500
WHITE = (255,255,255)
PADDING_COLOR = (120, 120, 120)
RANDOM_COLOR=(130,120,230)
GRAY = (80,80,80)

########## DEFINING A NODE CLASS TO STORE NODES AS OBJECTS ###############

class Node:
    def __init__(self, x, y, cost, parent_id):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent_id = parent_id
    
    def __lt__(self, other):
        return self.cost < other.cost

############ CONFIGURATION SPACE CONSTRUCTION WITH OBSTACLES ############

def Configuration_space(width, height):
    
    # Generating Obstacle Space
    obs_space = np.full((height, width),0)
    
    for y in range(0, height) :
        for x in range(0, width):
            
            rect_1_1_buffer = (x + 5) - 100  
            rect_1_2_buffer = (y + 5) - 100
            rect_1_3_buffer = (x - 5) - 175
            rect_1_3_bffer = (y - 5) - 500    

            rect_2_1_buffer = (x + 5) - 275  
            rect_2_2_buffer = (y + 5) - 0  
            rect_2_3_buffer = (x - 5) - 350
            rect_2_4_buffer = (y - 5) - 400 
            
            # Hexagon Obstacle
            hexagon_6_b = (y + 5) +  0.58*(x + 5) - 475.098
            hexagon_5_b = (y + 5) - 0.58*(x - 5) + 275.002
            hexagon_4_b = (x - 6.5) - 779.9
            hexagon_3_b = (y - 5) + 0.58*(x - 5) - 775.002
            hexaagon_2_b = (y - 5) - 0.58*(x + 5) - 24.92
            hexagon_1_b = (x + 6.5) - 520.1
            
            # Block Obstacle
            temp1_b = (x + 5) - 900
            temp2_b = (x + 5) - 1020
            temp3_b = (x - 5) - 1100
            temp4_b = (y + 5) - 50
            temp5_b = (y - 5) - 125
            temp6_b = (y + 5) - 375
            temp7_b = (y - 5) - 450
           
            if((temp1_b>0 and temp2_b<0 and temp4_b>0 and temp5_b<0) or(temp2_b>0 and temp3_b<0 and temp4_b>0 and temp7_b<0) or (temp6_b>0 and temp7_b<0 and temp1_b>0 and temp2_b<0) or (rect_1_1_buffer>0 and rect_1_2_buffer>0 and rect_1_3_buffer<0 and rect_1_3_bffer<0) or (rect_2_1_buffer>0 and rect_2_3_buffer<0 and rect_2_4_buffer<0 and rect_2_2_buffer>0) or (hexagon_6_b>0 and hexagon_5_b>0 and hexagon_4_b<0 and hexagon_3_b<0 and hexaagon_2_b<0 and hexagon_1_b>0)):
                obs_space[y, x] = 1
             
             
            
            winidow_1 = (y) - 5
            window_2 = (y) - 495
            window_3 = (x) - 5
            window_4 = (x) - 1195 

           
            rect_2_1 = (x) - 275  
            rect_2_2 = (y) - 0
            rect_2_4 = (x) - 350
            rect_2_3 = (y) - 400 
           
            rect_11 = (x) - 100  
            rect_12 = (y) - 100
            rect_13 = (x) - 175
            rect_14 = (y) - 500
            
            # Hexagon Obstacle
            h6 = (y) + 0.58*(x) - 475.098
            h5 = (y) - 0.58*(x) + 275.002
            h4 = (x) - 779.9
            h3 = (y) + 0.58*(x) - 775.002
            h2 = (y) - 0.58*(x) - 24.92
            h1 = (x) - 520.1 
            
            # Block Obstacle
            t1 = (x) - 900
            t2 = (x) - 1020
            t3 = (x) - 1100
            t4 = (y) - 50
            t5 = (y) - 125
            t6 = (y) - 375
            t7 = (y) - 450

            # Setting the line constrain to obatain the obstacle space with buffer
            if((h6>0 and h5>0 and h4<0 and h3<0 and h2<0 and h1>0) or (rect_11>0 and rect_12>0 and rect_13<0 and rect_14<0 ) or (rect_2_1>0  and rect_2_3<0 and rect_2_4<0 and rect_2_2>0) or (t1>0 and t2<0 and t4>0 and t5<0) or (t2>0 and t3<0 and t4>0 and t7<0) or (t6>0 and t7<0 and t1>0 and t2<0) or (winidow_1<0) or (window_2>0) or (window_3<0) or (window_4>0)):
                obs_space[y, x] = 2


####### DEFINING THE BOUNDARIES FOR CONFIGURATION SPACE ########

    for i in range(1200):
        obs_space[0][i] = 1
    for i in range(1200):
        obs_space[499][i] = 1
        
    for i in range(500):
        obs_space[i][1] = 1
        
    for i in range(500):
        obs_space[i][1199] = 1
       
    return obs_space

############## CHECK IF THE GIVEN MOVE IS VALID OR NOT ###############

def Validity(x, y, obs_space):
    # Check if coordinates are within the boundaries of the obstacle space and if the cell is occupied by an obstacle (value 1 or 2)
    if x < 0 or x >= map_width or y < 0 or y >= map_height or obs_space[y][x] == 1 or obs_space[y][x] == 2:
        return False
    
    return obs_space[y, x] == 0

############## CHECK IF THE GOAL NODE IS REACHED ###############

def Check_goal(present, goal):
    return math.isclose(present.x, goal.x) and math.isclose(present.y, goal.y)

############# GENERATE UNIQUE KEY ##############

def key(node):
    return 3333 * node.x + 113 * node.y 

############# GENERATE CHILD NODES ##############

def up(x, y, cost):
    return x, y - 1, cost + 1

def down(x, y, cost ):
    return x, y + 1, cost + 1

def left(x, y, cost):
    return x - 1, y, cost + 1

def right(x, y, cost):
    return x + 1, y, cost + 1

def bottom_left(x, y, cost):
    return x - 1, y + 1, cost + 1.4

def bottom_right(x, y, cost):
    return x + 1, y + 1, cost + 1.4

def up_left(x, y, cost):
    return x - 1, y - 1, cost + 1.4

def up_right(x, y, cost):
    return x + 1, y - 1, cost + 1.4

#######################3

#######################################################

def dijkstra(start, goal, obs_space):
    target_Node, start_node = goal, start
    moves = [up, down, left, right, bottom_left, bottom_right, up_left, up_right]
    unexplored_nodes, explored_nodes = {key(start_node): start_node}, set()
    priority_queue, all_nodes = PriorityQueue(), []

    priority_queue.put(start_node)

    while not priority_queue.empty():
        present_node = priority_queue.get()
        all_nodes.append([present_node.x, present_node.y])

        if Check_goal(present_node, target_Node):
            target_Node.parent_id, target_Node.cost = present_node.parent_id, present_node.cost
            print("Goal Node found")
            return all_nodes, 1

        if present_node in explored_nodes:
            continue
        else:
            explored_nodes.add(present_node)

        for move in moves:
            x, y, cost = move(present_node.x, present_node.y, present_node.cost)
            new_node = Node(x, y, cost, present_node)
            new_node_id = key(new_node)

            if not Validity(new_node.x, new_node.y, obs_space) or (new_node in explored_nodes or new_node_id in unexplored_nodes):
                continue

            if new_node_id in unexplored_nodes:
                if new_node.cost < unexplored_nodes[new_node_id].cost:
                    unexplored_nodes[new_node_id].cost, unexplored_nodes[new_node_id].parent = new_node.cost, new_node.parent
                    priority_queue.put(unexplored_nodes[new_node_id])
            else:
                unexplored_nodes[new_node_id] = new_node
                priority_queue.put(new_node)

    return all_nodes, 0
######### IMPLEMENTING DIJKSTRA ALGORITHM ##############

######### IMPLEMENTING DIJKSTRA ALGORITHM ##############


########### BACKTRACK AND GENERATE SHORTEST PATH ############

def Backtrack(target_Node):  
    x_way = []
    y_way = []
    x_way.append(target_Node.x)
    y_way.append(target_Node.y)

    parent_node = target_Node.parent_id
    total_cost = target_Node.cost
    while parent_node != -1:
        x_way.append(parent_node.x)
        y_way.append(parent_node.y)
        parent_node = parent_node.parent_id
        
    x_way.reverse()
    y_way.reverse()
    
    return x_way, y_way, total_cost

######### CALLING ALL MY FUNCTIONS TO IMPLEMENT DIJKSTRA ALGORITHM ON A POINT ROBOT ###########
def draw_map(screen, obs_space):
    for y in range(map_height):
        for x in range(map_width):
            if obs_space[y, x] == 1:
                pygame.draw.rect(screen, GRAY, (x, map_height - y - 1, 1, 1))
            elif obs_space[y, x] == 2:
                pygame.draw.rect(screen, PADDING_COLOR, (x, map_height - y - 1, 1, 1))
            

def draw_explored_nodes(screen, all_nodes, explored_color, frame_num):
    for node in all_nodes:
        pygame.draw.circle(screen, explored_color, (node[0], map_height - node[1] - 1), 1)
        if frame_num % 200 == 0:
            pygame.image.save(screen, os.path.join(frame_folder, f'frame_{frame_num:04d}.png'))
        frame_num += 1
        pygame.display.flip()
    return frame_num

def draw_shortest_path(screen, x_way, y_way, frame_num):
    for i in range(len(x_way) - 1):
        pygame.draw.line(screen, (0, 255, 255), (x_way[i], map_height - y_way[i] - 1),
                         (x_way[i + 1], map_height - y_way[i + 1] - 1), 2)
        pygame.image.save(screen, os.path.join(frame_folder, f'frame_{frame_num:04d}.png'))
        frame_num +=1
        pygame.display.flip()

# def draw_current_node(screen, current_node):
#     pygame.draw.circle(screen, (0, 0, 0), (current_node[0], map_height - current_node[1] - 1), 2)


###########

if __name__ == '__main__':
    

    pygame.init()
    screen = pygame.display.set_mode((map_width, map_height))
    obs_space = Configuration_space(map_width, map_height)
    pygame.display.set_caption("Algorithm Visualization Window")
    clock = pygame.time.Clock()

    # start_pointt = int(input("Enter the Number (x, y) :")).split(" ")
    # end_point = int(input("Enter the Number (x, y) :")).split(" ")
    # x_start_point =  int(input("Enter the start Number (x) :"))

    # y_start_point = int(input("Enter the start Number (y) :"))

    # x_end_point = int(input("Enter the end Number (x) :"))

    # y_end_point = int(input("Enter the end Number (y) :"))
    # Sample testCase
    x_start_point, y_start_point = 10, 10
    x_end_point, y_end_point = 190, 250
    
    start_node = Node(x_start_point, y_start_point - 1, 0, -1)
    target_Node = Node(x_end_point, y_end_point - 1, 0, -1)

    frame_num = 0
    new_frame_num = 0

    frame_folder = 'frames'
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    all_nodes, found_goal = dijkstra(start_node, target_Node, obs_space)

    print(found_goal)
    if found_goal:
        running = True
        x_way, y_way, total_cost = Backtrack(target_Node)
        print("total cost: ", total_cost)
        current_index = 0
        frame_count = 0

        screen.fill(WHITE)
        explored_color = (60, 150, 60)

        draw_map(screen, obs_space)
        new_frame_num = draw_explored_nodes(screen, all_nodes, explored_color, frame_num)
        draw_shortest_path(screen, x_way, y_way, new_frame_num)
        print("Total frames generated", new_frame_num)
    
        clock.tick(120)
        current_index += 1

        while current_index == target_Node:
            print("Exiting Loop")
            break
            

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break 


            # if current_index >= len(all_nodes):
            #     running = False
        else:
            print("Ending the program")
    pygame.quit()
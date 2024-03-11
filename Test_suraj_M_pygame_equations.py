
# backup files for the above files 
import numpy as np
import math
import heapq
import pygame ,sys
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

def is_point_inside_rectangle(x, y, vertices):
    x_min = min(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0])
    x_max = max(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0])
    y_min = min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])
    y_max = max(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])
    return x_min <= x <= x_max and y_min <= y <= y_max

def is_point_inside_hexagon(x, y , center_x, center_y, side_length):
    cx, cy = center_x, center_y
    vertices = []
    angle_deg = 60
    angle_rad = math.radians(angle_deg)
    for i in range(6):
        px = cx + side_length * math.cos(angle_rad * i + math.radians(30))
        py = cy + side_length * math.sin(angle_rad * i + math.radians(30))
        vertices.append((px, py))
    odd_nodes = False
    j = 5
    for i in range(6):
        if (vertices[i][1] < y and vertices[j][1] >= y) or (vertices[j][1] < y and vertices[i][1] >= y):
            if (vertices[i][0] + (y - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) * (vertices[j][0] - vertices[i][0])) < x:
                odd_nodes = not odd_nodes
        j = i
    return odd_nodes

def is_point_inside_block(point, vertices):
    odd_nodes = False
    j = len(vertices) - 1
    for i in range(len(vertices)):
        if (vertices[i][1] < point[1] and vertices[j][1] >= point[1]) or (vertices[j][1] < point[1] and vertices[i][1] >= point[1]):
            if (vertices[i][0] + (point[1] - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) * (vertices[j][0] - vertices[i][0])) < point[0]:
                odd_nodes = not odd_nodes
        j = i
    return odd_nodes

def Configuration_space(width, height):
    
    # Generating Obstacle Space
    obs_space = np.full((height, width),0)
    
    for y in range(0, height) :
        for x in range(0, width):
            
            # Plotting Buffer Space for the Obstacles using Half Plane Equations
            
            # Rectangle 1 Obastacle
            r11_buffer = (x + 5) - 100  
            r12_buffer = (y + 5) - 100
            r13_buffer = (x - 5) - 175
            r14_buffer = (y - 5) - 500    # No need to define lower most line at boundry
            
            # Rectangle 2 Obastacle
            r21_buffer = (x + 5) - 275  
            r22_buffer = (y + 5) - 0  # No need to define lower most line at boundry
            r23_buffer = (x - 5) - 350
            r24_buffer = (y - 5) - 400 
            
            # Hexagon Obstacle
            h6_buffer = (y + 5) +  0.58*(x + 5) - 475.098
            h5_buffer = (y + 5) - 0.58*(x - 5) + 275.002
            h4_buffer = (x - 6.5) - 779.9
            h3_buffer = (y - 5) + 0.58*(x - 5) - 775.002
            h2_buffer = (y - 5) - 0.58*(x + 5) - 24.92
            h1_buffer = (x + 6.5) - 520.1
            
            # Block Obstacle
            t1_buffer = (x + 5) - 900
            t2_buffer = (x + 5) - 1020
            t3_buffer = (x - 5) - 1100
            t4_buffer = (y + 5) - 50
            t5_buffer = (y - 5) - 125
            t6_buffer = (y + 5) - 375
            t7_buffer = (y - 5) - 450
            
            # Setting the line constrain to obatain the obstacle space with buffer
            if((t1_buffer>0 and t2_buffer<0 and t4_buffer>0 and t5_buffer<0) or(t2_buffer>0 and t3_buffer<0 and t4_buffer>0 and t7_buffer<0) or (t6_buffer>0 and t7_buffer<0 and t1_buffer>0 and t2_buffer<0) or (r11_buffer>0 and r12_buffer>0 and r13_buffer<0 and r14_buffer<0) or (r21_buffer>0 and r23_buffer<0 and r24_buffer<0 and r22_buffer>0) or (h6_buffer>0 and h5_buffer>0 and h4_buffer<0 and h3_buffer<0 and h2_buffer<0 and h1_buffer>0)):
                obs_space[y, x] = 1
             
             
            # Plotting Actual Object Space Half Plane Equations
            
            # Wall Obstacles
            w1 = (y) - 5
            w2 = (y) - 495
            w3 = (x) - 5
            w4 = (x) - 1195 

            # Rectangle 2 Obastacle
            r21 = (x) - 275  
            r22 = (y) - 0
            r24 = (x) - 350
            r23 = (y) - 400 
            
            # Rectangle 1 Obastacle
            r11 = (x) - 100  
            r12 = (y) - 100
            r13 = (x) - 175
            r14 = (y) - 500
            
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
            if((h6>0 and h5>0 and h4<0 and h3<0 and h2<0 and h1>0) or (r11>0 and r12>0 and r13<0 and r14<0 ) or (r21>0  and r23<0 and r24<0 and r22>0) or (t1>0 and t2<0 and t4>0 and t5<0) or (t2>0 and t3<0 and t4>0 and t7<0) or (t6>0 and t7<0 and t1>0 and t2<0) or (w1<0) or (w2>0) or (w3<0) or (w4>0)):
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




def up(x, y, cost, goal_x, goal_y):
    return x, y - 1, cost + 1, goal_x, goal_y

def down(x, y, cost, goal_x, goal_y):
    return x, y + 1, cost + 1, goal_x, goal_y

def left(x, y, cost, goal_x, goal_y):
    return x - 1, y, cost + 1, goal_x, goal_y

def right(x, y, cost, goal_x, goal_y):
    return x + 1, y, cost + 1, goal_x, goal_y

def bottom_left(x, y, cost, goal_x, goal_y):
    return x - 1, y + 1, cost + 1.4, goal_x, goal_y

def bottom_right(x, y, cost, goal_x, goal_y):
    return x + 1, y + 1, cost + 1.4, goal_x, goal_y

def up_left(x, y, cost, goal_x, goal_y):
    return x - 1, y - 1, cost + 1.4, goal_x, goal_y

def up_right(x, y, cost, goal_x, goal_y):
    return x + 1, y - 1, cost + 1.4, goal_x, goal_y

#######################3

#######################################################
######### IMPLEMENTING DIJKSTRA ALGORITHM ##############


def dijkstra(start, goal, obs_space):
    if Check_goal(start, goal):
        return None, 1

    goal_node = goal
    start_node = start

    moves = [up, down, left, right, bottom_left, bottom_right, up_left, up_right]
    unexplored_nodes = {}
    start_key = key(start_node)
    unexplored_nodes[start_key] = start_node

    explored_nodes = set()
    priority_list = [(start_node.cost, start_node)]
    
    all_nodes = []

    while priority_list:
        present_node_cost, present_node = heapq.heappop(priority_list)

        all_nodes.append([present_node.x, present_node.y])

        if present_node == goal_node:
            goal_node.parent_id = present_node.parent_id
            goal_node.cost = present_node.cost
            print("Goal Node found")
            return all_nodes, 1

        if present_node in explored_nodes:
            continue
        else:
            explored_nodes.add(present_node)

        for move in moves:
            x, y, cost, goal_x, goal_y = move(present_node.x, present_node.y, present_node.cost, goal_node.x, goal_node.y)
            new_node = Node(x, y, cost, present_node)
            new_node_id = key(new_node)

            if not Validity(new_node.x, new_node.y, obs_space) or (new_node in explored_nodes or new_node_id in unexplored_nodes):
                continue

            if new_node_id in unexplored_nodes:
                if new_node.cost < unexplored_nodes[new_node_id].cost:
                    unexplored_nodes[new_node_id].cost = new_node.cost
                    unexplored_nodes[new_node_id].parent_id = new_node.parent_id
                    priority_list.remove((unexplored_nodes[new_node_id].cost, unexplored_nodes[new_node_id]))
                    heapq.heappush(priority_list, (new_node.cost, unexplored_nodes[new_node_id]))
            else:
                unexplored_nodes[new_node_id] = new_node
                heapq.heappush(priority_list, (new_node.cost, new_node))
            
    return all_nodes, 0
######### IMPLEMENTING DIJKSTRA ALGORITHM ##############


########### BACKTRACK AND GENERATE SHORTEST PATH ############

def Backtrack(goal_node):  
    x_path = []
    y_path = []
    x_path.append(goal_node.x)
    y_path.append(goal_node.y)

    parent_node = goal_node.parent_id
    while parent_node != -1:
        x_path.append(parent_node.x)
        y_path.append(parent_node.y)
        parent_node = parent_node.parent_id
        
    x_path.reverse()
    y_path.reverse()
    
    return x_path, y_path

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

def draw_shortest_path(screen, x_path, y_path, frame_num):
    for i in range(len(x_path) - 1):
        pygame.draw.line(screen, (0, 255, 255), (x_path[i], map_height - y_path[i] - 1),
                         (x_path[i + 1], map_height - y_path[i + 1] - 1), 2)
        pygame.image.save(screen, os.path.join(frame_folder, f'frame_{frame_num:04d}.png'))
        frame_num +=1
        pygame.display.flip()

# def draw_current_node(screen, current_node):
#     pygame.draw.circle(screen, (0, 0, 0), (current_node[0], map_height - current_node[1] - 1), 2)


###########

if __name__ == '__main__':
    obs_space = Configuration_space(map_width, map_height)

    pygame.init()
    screen = pygame.display.set_mode((map_width, map_height))
    pygame.display.set_caption("Dijkstra Algorithm")
    clock = pygame.time.Clock()

    s_x, s_y = 5, 5
    e_x, e_y = 1140, 450
    start_node = Node(s_x, s_y - 1, 0, -1)
    goal_node = Node(e_x, e_y - 1, 0, -1)
    # start_node = Node(s_x, s_y, 0, -1)
    # goal_node = Node(e_x, e_y, 0, -1)
    frame_num = 0

    frame_folder = 'frames'
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    all_nodes, found_goal = dijkstra(start_node, goal_node, obs_space)
    print(found_goal)
    if found_goal:
        running = True
        current_index = 0

        frame_count = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(WHITE)
            explored_color = (150, 200, 60)

            draw_map(screen, obs_space)
            new_frame_num = draw_explored_nodes(screen, all_nodes, explored_color, frame_num)
            print(new_frame_num)
            # if current_index < len(all_nodes):
            #     draw_shortest_path(screen, [all_nodes[i][0] for i in range(current_index)],
            #                        [all_nodes[i][1] for i in range(current_index)])
                # draw_current_node(screen, all_nodes[current_index])
                

            # if found_goal:
            x_path, y_path = Backtrack(goal_node)
            draw_shortest_path(screen, x_path, y_path, new_frame_num)

            
            clock.tick(120)
            current_index += 1

            if current_index >= len(all_nodes):
                running = False
        else:
            print("Ma chuda")
    pygame.quit()
#  This files contains code for project 2
# under development 

# Verion: 0.1 (Final, Test)  
# Date: 9th March
# Sources: Stackoverflow, Github, ChatGpt

import pygame, sys
from pygame.locals import *
import math
import pygame.gfxdraw


map_width = 500
map_height = 1200

def main():
    pygame.init()
    DISPLAY=pygame.display.set_mode((map_height,map_width))
    WHITE=(255,255,255)
    GRAY = (80,80,80)
    
    polygon_sides = 6
    polygon_length = 150
    polygon_bloat = 5
    PADDING_COLOR = (120,120,120)
    padding = 5
    DISPLAY.fill(WHITE)

    # pygame.draw.rect(DISPLAY, [red, blue, green], [left, top, width, height], filled)
    


    pygame.draw.rect(DISPLAY, GRAY, (100-padding, -50-padding, 75+2*padding, 400+2*padding))  # Leftmost rectangle with padding
    pygame.draw.rect(DISPLAY, GRAY, (275-padding, 100-padding, 75+2*padding, 400+2*padding))  # rightmost rectangle 
    
    pygame.draw.rect(DISPLAY,PADDING_COLOR,(100,-50,75,400)) # Leftmost rectangle 
    pygame.draw.rect(DISPLAY,PADDING_COLOR,(275,100,75,400))  # rightmost rectangle 

    # pygame.draw.rect(DISPLAY,GRAY,(275,100,75,400))
    # pygame.draw.polygon(DISPLAY, GRAY,150 ,[(125, 125 ), (50, 50), (50,75)])


    # Calculate the vertices of the polygon
    polygon_vertices = []
    
    # pygame.draw.circle(DISPLAY, GRAY, (y,x), 150, 1)
    for i in range(polygon_sides):
        angle = math.radians(i * (360 / polygon_sides) + 90)
        # angle = i * (2 * math.pi / polygon_sides)
        x = 650 + ((polygon_length + polygon_bloat) - padding ) * math.cos(angle)
        y = 250 + ((polygon_length + polygon_bloat) - padding) * math.sin(angle)
        polygon_vertices.append((x, y))

    # print(polygon_vertices)
    pygame.draw.polygon(DISPLAY, PADDING_COLOR, polygon_vertices,0)
    pygame.draw.polygon(DISPLAY, GRAY, polygon_vertices, 5)
    
    # Rightmost rectangle with padding
    
    # pygame.draw.rect(DISPLAY,PADDING_COLOR,(100,-50,75,400)) # Leftmost rectangle 
    # pygame.draw.rect(DISPLAY,PADDING_COLOR,(275,100,75,400)) # rightmost rectangle
    # U Shaped right hand rectangle
    # # pygame.draw.rect(DISPLAY, [red, blue, green], [left, top, width, height], filled)
    # pygame.draw.rect(DISPLAY, GRAY, (1020, 50, 80, 400))   # Right vertical part of U
    # pygame.draw.rect(DISPLAY, GRAY, (900, 50, 200, 75))  # TOP vertical part of U
    # pygame.draw.rect(DISPLAY, GRAY, (900, 375, 200, 75))  # Bottom Horizontal part of U rect

# Polygon: 
    # Draw the polygon on the map
    
    
#  U shaped rectangle
    pygame.draw.rect(DISPLAY, GRAY, (1020-padding, 50-padding, 80+2*padding, 400+2*padding))   # Right vertical part of U with padding
    pygame.draw.rect(DISPLAY, GRAY, (900-padding, 50-padding, 200+2*padding, 75+2*padding))  # Top vertical part of U with padding
    pygame.draw.rect(DISPLAY, GRAY, (900-padding, 375-padding, 200+2*padding, 75+2*padding))  # Bottom Horizontal part of U rect with padding
    
#   Padding for U shaped Rectangle 
    pygame.draw.rect(DISPLAY, PADDING_COLOR, (1020, 50, 80, 400))   # Right vertical part of U without padding
    pygame.draw.rect(DISPLAY, PADDING_COLOR, (900, 50, 200, 75))  # Top vertical part of U without padding
    pygame.draw.rect(DISPLAY, PADDING_COLOR, (900, 375, 200, 75))  # Bottom Horizontal part of U rect without padding

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()
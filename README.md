# Pathfinding Algorithm Visualization

This repository contains a Python implementation of the Dijkstra pathfinding algorithm with obstacle space visualization. The algorithm is applied to a point robot navigating through a 2D environment with obstacles.

## Overview

The code consists of the following components:

1. **Node Class**: Defines a node in the configuration space, storing information such as coordinates, cost, and parent ID.

2. **Configuration Space Construction**: Generates an obstacle space with predefined obstacles, including rectangles, hexagons, and blocks.

3. **Validity Check**: Determines if a given move is valid by checking boundaries and obstacle occupancy.

4. **Goal Check**: Verifies if the goal node is reached.

5. **Dijkstra Algorithm Implementation**: Applies Dijkstra's algorithm to find the shortest path from the start node to the goal node.

6. **Visualization**: Utilizes Pygame to visualize the obstacle space, explored nodes, and the shortest path.

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone
   ```

## Install dependencies

```bash
    pip install numpy pygame opencv-python


```

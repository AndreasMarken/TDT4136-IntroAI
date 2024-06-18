from queue import PriorityQueue

class Node:
    def __init__(self, position, cellValue=0):
        self.position = position # [x, y] position of the node
        self.cellValue = cellValue # The cost of moving to this node
        self.g = float('inf')
        self.f = float('inf') # g + h, initialized to inf because we are looking for the smallest f
        self.cameFrom = None # Used to reconstruct the path

    def __lt__(self, other): # Compare method used for the priority queue
        return self.f < other.f

def createNodes(map_obj): # Create a dictionary of nodes from the map object. Return the dict with a tuple of the position as the key
    nodes = {}
    for i in range(map_obj.int_map.shape[0]):
        for j in range(map_obj.int_map.shape[1]):
            if map_obj.get_cell_value([i, j]) > 0:
                nodes[(i, j)] = Node([i, j], cellValue=map_obj.get_cell_value([i, j]))
    return nodes

def heuristic_manhattan(curr, goalNode): # Manhattan distance heuristic function
    return abs(curr.position[0] - goalNode.position[0]) + abs(curr.position[1] - goalNode.position[1])

def heuristic_euclidean(curr, goalNode): # Euclidean distance heuristic function
    return ((curr.position[0] - goalNode.position[0])**2 + (curr.position[1] - goalNode.position[1])**2)**0.5

def isPossibleMove(map_obj, position): # A possible move is withing the bounds of the map and the cell value is greater than 0. This is the way the map is built up. I use greater than 0, since i fill the reconstructed path with 0s.
    x, y = position
    return (
        0 <= x < map_obj.int_map.shape[0] and # Within the x coordinates
        0 <= y < map_obj.int_map.shape[1] and # Within the y coordinates
        map_obj.get_cell_value(position) > 0 # The cell value is greater than 0
    )

def getNeighbors(map_obj, curr): # Get a list of neighbor positions that are possbile moves using the isPossibleMove function. Could instead create edges from the nodes, and create a more graph esk solution, but this works fine.
    neighbors = []
    for dir in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
        neighbor = [curr.position[0] + dir[0], curr.position[1] + dir[1]]
        if isPossibleMove(map_obj, neighbor):
            neighbors.append(neighbor) 
    return neighbors

def aStarSearch(map): # A* search algorithm
    nodes = createNodes(map) # Dictionary of nodes
    startNode = nodes[tuple(map.get_start_pos())] # Get the start node
    startNode.g = 0 # The cost of moving to the start node is 0
    goalNode = nodes[tuple(map.get_goal_pos())] # Get the goal node
    
    frontier = PriorityQueue() # So we dont have to sort a list each iteration
    frontier.put(startNode, 0) # Put the start node in the frontier

    
    while not frontier.empty():
        currentNode = frontier.get()

        for neighbor in getNeighbors(map, currentNode):
            neighborNode = nodes[tuple(neighbor)] # Get the node from the neighbor position
            cost = currentNode.g + neighborNode.cellValue # The cost of moving to the neighbor node is the cost of moving to the current node + the cell value of the neighbor node

            if cost < neighborNode.g: # If the cost is less than the cost of moving to the neighbor node, update the neighbor node. Better solution found
                neighborNode.g = cost
                neighborNode.f = cost + heuristic_manhattan(neighborNode, goalNode) # The heuristic function can either be euclidean distance or manhattan distance. From my testing, the results are the same, except on task 2, where from only visual, i think euclidian is better.
                frontier.put(neighborNode, neighborNode.f) # Put the neighbor node in the frontier
                neighborNode.cameFrom = currentNode.position # Update the cameFrom attribute of the neighbor node

    # Reconstruct the path
    path = [] 
    current = goalNode.position # Start at the goal node since we use the cameFrom attribute in the Node class.
    if goalNode.cameFrom is None:
        return None # No path found
    current = nodes[tuple(current)].cameFrom # Skip the goal node, such that its color doesnt change.

    cost = 0

    while current != startNode.position: # Loop throug all the nodes we came from, until we reach the start node
        path.append(current) 
        map.set_cell_value(current, 0) # Set the cell value to 0, so we can see the path on the map
        current = nodes[tuple(current)].cameFrom # Update current to the node we came from
        cost += nodes[tuple(current)].cellValue

    print("Cost: %d" % cost)
    return path # Return the path
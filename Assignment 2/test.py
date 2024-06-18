from queue import PriorityQueue
import Map

class Node:
    def __init__(self, position, cellValue=0):
        self.position = position
        self.cellValue = cellValue
        self.g = float('inf')
        self.f = float('inf')
        self.cameFrom = None
        self.neighbors = []  # List of connected nodes

    def __lt__(self, other):
        return self.f < other.f

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost

def createGraph(map_obj):
    nodes = {}
    edges = []

    for i in range(map_obj.int_map.shape[0]):
        for j in range(map_obj.int_map.shape[1]):
            if map_obj.get_cell_value([i, j]) > 0:
                node = Node([i, j], cellValue=map_obj.get_cell_value([i, j]))
                nodes[(i, j)] = node

    # Create edges based on neighboring nodes
    for node in nodes.values():
        for dir in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            neighbor_pos = [node.position[0] + dir[0], node.position[1] + dir[1]]
            if tuple(neighbor_pos) in nodes:
                neighbor_node = nodes[tuple(neighbor_pos)]
                edge_cost = node.cellValue + neighbor_node.cellValue
                edge = Edge(node, neighbor_node, edge_cost)
                edges.append(edge)
                node.add_neighbor(neighbor_node)
                neighbor_node.add_neighbor(node)

    return nodes, edges

def heuristic_manhattan(curr, goalNode):
    return abs(curr.position[0] - goalNode.position[0]) + abs(curr.position[1] - goalNode.position[1])

def heuristic_euclidean(curr, goalNode):
    return ((curr.position[0] - goalNode.position[0])**2 + (curr.position[1] - goalNode.position[1])**2)**0.5

def aStarSearch(graph, start_pos, goal_pos):
    nodes, edges = graph
    startNode = nodes[tuple(start_pos)]
    goalNode = nodes[tuple(goal_pos)]

    frontier = PriorityQueue()  # So we don't have to sort a list each iteration
    frontier.put(startNode, 0)
    startNode.g = 0

    while not frontier.empty():
        currentNode = frontier.get()

        if currentNode == goalNode:
            # Reconstruct and return the path.
            path = []
            current = goalNode.position
            while current != startNode.position:
                path.append(current)
                current = nodes[tuple(current)].cameFrom
            return path[::-1]  # Reverse the path to start from the start node.

        for neighbor_node in currentNode.neighbors:
            edge_cost = None
            for edge in edges:
                if (edge.node1 == currentNode and edge.node2 == neighbor_node) or \
                   (edge.node2 == currentNode and edge.node1 == neighbor_node):
                    edge_cost = edge.cost
                    break

            if edge_cost is not None:
                cost = currentNode.g + edge_cost

                if cost < neighbor_node.g:
                    neighbor_node.g = cost
                    neighbor_node.f = cost + heuristic_euclidean(neighbor_node, goalNode)
                    frontier.put(neighbor_node, neighbor_node.f)
                    neighbor_node.cameFrom = currentNode.position

    return None  # No path found

map_obj = Map.Map_Obj(task=2)
path = aStarSearch(createGraph(map_obj), map_obj.get_start_pos(), map_obj.get_goal_pos())

for node in path:
    map_obj.set_cell_value(node, 5)

map_obj.show_map()
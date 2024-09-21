class Node:
    def __init__(self, name, capacity, dist):
        self.name = name
        self.capacity = capacity
        self.dist = dist
        self.ants = 0

class Ant:
    def __init__(self, number, lieu):
        self.number = number
        self.lieu = lieu

    def move(self, nodes_list):
        current_node = nodes_list[self.lieu]
        possible_moves = [node for node in nodes_list if abs(node.dist - current_node.dist) == 1 and node.ants < node.capacity]
        if possible_moves:
            next_node = min(possible_moves, key=lambda x: x.dist) 
            current_node.ants -= 1
            next_node.ants += 1
            self.lieu = nodes_list.index(next_node)
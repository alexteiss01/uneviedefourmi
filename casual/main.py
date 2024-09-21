import matplotlib.pyplot as plt
import networkx as nx
from ants import Ant
from ants import Node



def charger_nodes():
    nodes_list = []
    with open("infograph.txt") as file:
        for line in file:
            name, capacity, dist = line.strip().split(",")
            node = Node(name, int(capacity), int(dist))
            nodes_list.append(node)
    return nodes_list

nodes_list = charger_nodes()

# Initialisation des fourmis
ants_list = [Ant(i, 0) for i in range(10)]
nodes_list[0].ants = len(ants_list)

def move_ants(ants_list, nodes_list):
    for ant in ants_list:
        ant.move(nodes_list)

def all_ants_in_sd(nodes_list):
    sd_node = next(node for node in nodes_list if node.name == 'Sd')
    return sd_node.ants == len(ants_list)

# Simulation des étapes
step = 0
while not all_ants_in_sd(nodes_list):
    move_ants(ants_list, nodes_list)
    step += 1
    print(f"Étape {step}:")
    for node in nodes_list:
        print(f"Node {node.name} - Fourmis: {node.ants}")
(print("Les fourmis ont atteint le dortoir en seulement", step, "étapes !"))

# Représentation graphique du réseau
G = nx.Graph()

for node in nodes_list:
    G.add_node(node.name, capacity=node.capacity, dist=node.dist)

for node in nodes_list:
    if node.dist == 1:
        G.add_edge('Sd', node.name)
    for other_node in nodes_list:
        if abs(node.dist - other_node.dist) == 1:
            G.add_edge(node.name, other_node.name)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10)

plt.title("Représentation graphique du réseau")
plt.show()


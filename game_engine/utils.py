import re
import networkx as nx
import networkx.algorithms.isomorphism as iso
import time
from tqdm import tqdm
import pickle, gzip

from matplotlib import pyplot as plt
from networkx import dfs_preorder_nodes

time1 = time.time()
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ+"


def build_gaddag(dictionary):
    print("Generating Gaddag")
    gaddag = nx.DiGraph()
    gaddag.add_node(0, final=False)
    gaddag.add_node(1, final=True)
    extended_dictionary = []
    for word in tqdm(dictionary):
        for start_letter_index in range(len(word)-1):
            extended_dictionary.append(word[start_letter_index:0:-1]+word[0]+"+"+word[start_letter_index+1:])
        extended_dictionary.append(word[::-1])
    extended_dictionary.sort(key=len, reverse=True)
    length_dict = len(extended_dictionary)
    word_number = 0
    for word in extended_dictionary:
        if word_number % 10000 == 0:
            print("Word", word_number, "of", length_dict, "words")
            print("Time : ", time.time() - time1)
        word_number += 1
        last_node_index = 0
        for i, letter in enumerate(word):
            next_node_index = get_successor_with_letter(gaddag, last_node_index, alphabet.index(letter))
            if next_node_index == -1:
                if i == len(word)-1:
                    if gaddag.has_edge(last_node_index, 1):
                        gaddag[last_node_index][1]['letter'].update({alphabet.index(letter)})
                    else:
                        gaddag.add_edge(last_node_index, 1, letter={alphabet.index(letter)})
                else:
                    gaddag.add_edge(last_node_index, gaddag.number_of_nodes(), letter={alphabet.index(letter)})
                    last_node_index = gaddag.number_of_nodes()-1
                    nx.set_node_attributes(gaddag, {last_node_index: {'final': False}})
            else:
                last_node_index = next_node_index

        nx.set_node_attributes(gaddag, {last_node_index: {'final': True}})
    print("Done generating gaddag")
    return gaddag


def is_indistinguishable(graph, node1, node2):

    if nx.get_node_attributes(graph, "final")[node1] != nx.get_node_attributes(graph, "final")[node2]:
        return False

    subtree_node1 = graph.subgraph(nx.descendants_at_distance(graph, node1, 1) | {node1})
    subtree_node2 = graph.subgraph(nx.descendants_at_distance(graph, node2, 1) | {node2})
    def is_same_edge_letters(data1, data2):
        return data1.get("letter") == data2.get("letter")
    node_match = iso.numerical_node_match("final", False)
    return iso.is_isomorphic(subtree_node1, subtree_node2, node_match=node_match, edge_match=is_same_edge_letters)


def get_successor_with_letter(graph, node, letter):
    for successor in graph.successors(node):
        if letter in graph.edges[node, successor]['letter']:
            return successor
    return -1


ods = []
with (open("../data/ODS9.txt", "r") as file):
    for line in file:
        ods.append(line.strip())


my_gaddag = build_gaddag(ods)
print(my_gaddag.number_of_nodes())


"""
my_dictionary = ["MAN", "TAN", "BAN", "BA"]
my_gaddag = build_gaddag(my_dictionary)
print(my_gaddag.number_of_nodes())
"""

"""
pos = nx.spring_layout(my_gaddag)
nx.draw(my_gaddag, pos=pos, with_labels=True)
nx.draw_networkx_edge_labels(my_gaddag, pos=pos)
plt.show()
"""


with gzip.open("../data/gaddag.pkl.gz", "wb") as f:
    pickle.dump(my_gaddag, f, protocol=pickle.HIGHEST_PROTOCOL)


print(f"Time : {time.time()-time1}")




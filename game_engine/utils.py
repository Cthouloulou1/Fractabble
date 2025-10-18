import networkx as nx
import time
from tqdm import tqdm
import pickle, gzip

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

    for word in tqdm(extended_dictionary):
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

with gzip.open("../data/gaddag.pkl.gz", "wb") as f:
    pickle.dump(my_gaddag, f, protocol=pickle.HIGHEST_PROTOCOL)


print(f"Time : {time.time()-time1}")




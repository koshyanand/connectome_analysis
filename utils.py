import igraph as ig
import pandas as pd
import numpy as np
import networkx as nx

description = "regionDescriptions_short.txt"
human = "./data/human/"
chimp = "./data/chimpanzee/"
data_root = "data/"

def check_if_equal(mat1, mat2):
    count = 0
    for i in range(len(mat1)):
        
        for j in range(len(mat1[0])):
            
            if mat1[i][j] != mat2[i][j]:
                count += 1
    print(f"Total number of different edges : {count}")
    return count

def create_adj_matrix(path, dim):
    adj_matrix = [[0 for x in range(dim)] for y in range(dim)] 
    
    f = open(path, "r")
    i = 0;
    for row in f:
        values = row.split("\t")
        
        for j, val in enumerate(values):
            if val == "1":
                adj_matrix[i][j] = 1
        i += 1
    return adj_matrix

def create_degree_dict(graph):
    degree_list = list(graph.degree())
    degree_dict = {}
    for i in range(len(degree_list)):
        degree_dict[graph.vs[i]["label"].item()] = degree_list[i]
    return degree_dict

def get_file(path):
    f = open(path, "r")
    i = 0;
    output = []
    return np.array(f.read().strip().split("\n")) 
    
def get_labels():   
    return get_file(chimp + description), get_file(human + description)
    
def load_graph():

    chimp_adj_matrix = create_adj_matrix(chimp + "chimpanzee_60.txt", 72)
    human_adj_matrix = create_adj_matrix(human + "human_60.txt", 72)

    check_if_equal(chimp_adj_matrix, human_adj_matrix)

    chimp_graph = ig.Graph.Adjacency(chimp_adj_matrix)
    human_graph = ig.Graph.Adjacency(human_adj_matrix)

    df_chimp_header = get_file(chimp + description)                
    df_human_header = get_file(human + description)  
    chimp_graph.vs['label'] = np.array(df_chimp_header)
    human_graph.vs['label'] = np.array(df_human_header)

    return chimp_graph, human_graph

def load_nx_graph():

    chimp_adj_matrix = create_adj_matrix(chimp + "chimpanzee_60.txt", 72)
    human_adj_matrix = create_adj_matrix(human + "human_60.txt", 72)

    check_if_equal(chimp_adj_matrix, human_adj_matrix)
    
    chimp_graph = nx.from_numpy_matrix(np.array(chimp_adj_matrix), create_using=nx.DiGraph())
    human_graph = nx.from_numpy_matrix(np.array(human_adj_matrix), create_using=nx.DiGraph())
    return chimp_graph, human_graph

def get_max_flow(graph):
    max_flow = []
    for i, sourceVertex in enumerate(graph.vs):

        for j, targetVertex in enumerate(graph.vs):
            if i == j:
                continue
            max_flow.append((graph.maxflow(i, j).value, i, j))
    max_flow.sort(reverse = True)
    
    return max_flow

def convert_to_nx_graph(graph):
    return nx.from_numpy_matrix(np.array(graph.get_adjacency().data), create_using=nx.DiGraph())
    
def generate_randomized_graph(graph, versions, to_nx = False):
    random_g_list = []
    for i in range(versions):
        new_g = graph.copy()
        new_g.rewire(n=1000, mode='simple')
        if to_nx:
            random_g_list.append(convert_to_nx_graph(new_g))
        else:
            random_g_list.append(new_g)
    
    return random_g_list

def create_array(dic):
    out = []
    for i in range(72):
        out.append(dic[i])
    return out
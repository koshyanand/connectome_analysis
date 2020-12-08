import igraph as ig
import pandas as pd
import numpy as np

def check_if_equal(mat1, mat2):
    count = 0
    for i in range(len(mat1)):
        
        for j in range(len(mat1[0])):
            
            if mat1[i][j] != mat2[i][j]:
                count += 1
    print(f"Total number of different edges : {count}")
    return count

# path : Path of text file containing adj matrix
# dim : Dimention of the adj matrix
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
    

def load_graph():
    data_root = "data/"
    description = "regionDescriptions_short.txt"
    human = "./data/human/"
    chimp = "./data/chimpanzee/"

    chimp_adj_matrix = create_adj_matrix(chimp + "chimpanzee_60.txt", 72)
    human_adj_matrix = create_adj_matrix(human + "human_60.txt", 72)

    check_if_equal(chimp_adj_matrix, human_adj_matrix)

    chimp_graph = ig.Graph.Adjacency(chimp_adj_matrix)
    human_graph = ig.Graph.Adjacency(human_adj_matrix)

    df_chimp_header = pd.read_csv(chimp + description, sep='\t')               
    df_human_header = pd.read_csv(human + description, sep='\t')
    chimp_graph.vs['label'] = df_chimp_header.to_numpy()
    human_graph.vs['label'] = df_human_header.to_numpy()

    return chimp_graph, human_graph

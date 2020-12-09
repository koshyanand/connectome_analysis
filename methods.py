import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig
import networkx as nx
from utils import get_max_flow,load_nx_graph, load_graph, create_array
import math
from networkx.algorithms import closeness_centrality
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
human = "./data/human/"
chimp = "./data/chimpanzee/"
description = "regionDescriptions_short.txt"
import csv

def get_label(isChimp):
    if isChimp:
        filename = chimp + description
    else:
        filename = chimp + description
    f = open(filename, "r")
    return np.array(f.read().strip().split("\n")) 

def get_tuple(values, arg_sorted_values, isChimp):
    labels = get_label(isChimp)
    print(f"Lables : {len(labels)}")
    out = []
    for i in range(len(arg_sorted_values)):
        index = arg_sorted_values[i]
        out.append((labels[index], round(values[index], 4)))
    return out
        
def get_centrality(graph, method, topk=None):
    
    if method == "edge_betweeness_centrality":
        output = nx.edge_betweenness_centrality(graph)
    elif method == "betweenness_centrality":
        output = nx.betweenness_centrality(graph)
    elif method == "closeness_centrality":
        output = nx.closeness_centrality(graph)
    elif method == "eigenvector_centrality":
        output = nx.eigenvector_centrality(graph)
    elif method == "in_degree_centrality":
        output = nx.in_degree_centrality(graph)
    elif method == "out_degree_centrality":
        output = nx.out_degree_centrality(graph)
    elif method == "pagerank":
        output = pagerank(graph)
    else:
        return
    print(len(output))
    output = np.array(create_array(output))
    mean = round(np.mean(output), 4)
    if topk:
        arg_sorted_results = np.argsort(output)[::-1][:topk]
    else:
        arg_sorted_results = np.argsort(output)[::-1]
        
    return output, arg_sorted_results, mean
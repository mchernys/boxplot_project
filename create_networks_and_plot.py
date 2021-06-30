import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import networkx as nx
import sys

#protein_links_file="9606.protein.links.v11.0.txt.gz"
#protein_domains_file="proteins_w_domains.txt"
#boxplot_file="protein_domains_vs_string_degree.png"
protein_links_file = sys.argv[1]
protein_domains_file = sys.argv[2]
boxplot_file = "protein_domains_vs_string_degree.png"

network_data_frame = pd.read_csv(protein_links_file, sep=' ')
network = nx.from_pandas_edgelist(network_data_frame, source = "protein1", target = "protein2", edge_attr= "combined_score")
original_num_edges = network.number_of_edges()

sig_combined_score = 500
selected_edges = [(u,v) for u,v,e in network.edges(data=True) if e['combined_score'] >= sig_combined_score]
network = network.edge_subgraph(selected_edges)
new_num_edges = network.number_of_edges()

sig_node_degree = 100
greater_degree_nodes = [n for n in network.nodes() if network.degree[n] > sig_node_degree]
lesser_degree_nodes = [n for n in network.nodes() if network.degree[n] <= sig_node_degree]
greater_degree_network = network.subgraph(greater_degree_nodes)
lesser_degree_network = network.subgraph(lesser_degree_nodes)

prot_domains_per_id_df = pd.read_csv(protein_domains_file, sep = '\t')
prot_domains_per_id_df = prot_domains_per_id_df.loc[~prot_domains_per_id_df["Pfam ID"].isnull(),:]

ctr_dict = dict()
for prot_stable_id, df in prot_domains_per_id_df.groupby(by = "Protein stable ID"):
    ctr_dict[prot_stable_id] = len(df['Pfam ID'].unique())
greater_degree_domains = [ctr_dict[n.split(".")[1]] for n in greater_degree_network.nodes() if n.split(".")[1] in ctr_dict]
lesser_degree_domains = [ctr_dict[n.split(".")[1]] for n in lesser_degree_network.nodes() if n.split(".")[1] in ctr_dict]

df1 = pd.DataFrame()
df1['Domains'] = greater_degree_domains
df1['Degrees'] = 'Greater than 100'
df2 = pd.DataFrame()
df2['Domains'] = lesser_degree_domains
df2['Degrees'] = 'Less than or Equal to 100'
df = pd.concat([df1, df2]).reset_index(drop = True)

p = sns.catplot(x = 'Degrees', y='Domains',data =df, kind = 'box')
p.savefig(boxplot_file)
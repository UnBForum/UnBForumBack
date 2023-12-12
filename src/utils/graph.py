from operator import neg

import networkx as nx
from networkx.algorithms import bipartite


def calculate_degree_centrality(topics, categories, topic_has_category):
    bipartite_graph = build_bipartite_graph(topics, categories, topic_has_category)

    categories = {node for node, data in bipartite_graph.nodes(data=True) if data["bipartite"] == 1}
    bipartite_degree_centrality = bipartite.degree_centrality(bipartite_graph, categories)

    return bipartite_degree_centrality


def build_bipartite_graph(topics, categories, topic_has_category):
    bipartite_graph = nx.Graph()
    bipartite_graph.add_nodes_from([neg(topic.id) for topic in topics], bipartite=0)
    bipartite_graph.add_nodes_from([category.id for category in categories], bipartite=1)
    bipartite_graph.add_edges_from([(neg(row.topic_id), row.category_id) for row in topic_has_category])

    return bipartite_graph
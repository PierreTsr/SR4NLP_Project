import networkx as nx
from ucca.core import Passage

def passage2graph(passage: Passage):
    g = nx.DiGraph()
    for key, val in passage.nodes.items():
        try:
            g.add_node(key, text=val.attrib["text"])
        except KeyError:
            g.add_node(key)
        for e in val.incoming:
            parent_id = e.parent.ID
            g.add_edge(parent_id, key, tag=e.tag)
    return g

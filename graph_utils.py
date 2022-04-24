import networkx as nx
from networkx import DiGraph
from ucca.core import Passage


def passage2graph(passage: Passage):
    """
    Create a `networkx.DiGraph` from a parsed `ucca.core.Passage`.

    Assume that terminal nodes have the text stored in the "text" attribute, and that edges labels are stored in the
    "tag" attribute. Nodes keep the same naming convention, i.e. '0.${Token_Index}' for terminal nodes and '1.${Index}'
    for the rest.

    :param passage: parsed Passage to convert.
    :type passage: Passage
    :return: a directed graph.
    :rtype: DiGraph
    """
    g = DiGraph()
    for key, val in passage.nodes.items():
        try:
            g.add_node(key, text=val.attrib["text"])
        except KeyError:
            g.add_node(key)
        for e in val.incoming:
            parent_id = e.parent.ID
            g.add_edge(parent_id, key, tag=e.tag)
    return g


def get_children(graph: DiGraph, node: str):
    """
    Query the sorted leaf names when exploring `graph` from `node`.

    :param graph: ucca directed graph.
    :type graph: DiGraph
    :param node: key of the node to start from.
    :type node: str
    :return: sorted list of the terminal node keys reached from `node`.
    :rtype: list
    """
    leaves = list(filter(lambda n: n[0] == '0', nx.dfs_preorder_nodes(graph, node)))
    leaves.sort(key=lambda n: int(n.split('.')[1]))
    return leaves


def get_text(graph: DiGraph, node: str):
    """
    Query the text corresponding to a node in the ucca graph.

    :param graph: ucca directed graph.
    :type graph: DiGraph
    :param node: key of the node to start from.
    :type node: str
    :return: phrase corresponding to `node`.
    :rtype: str
    """
    leaves = get_children(graph, node)
    return " ".join(graph.nodes[n]["text"] for n in leaves)


def get_tokens(graph: DiGraph, node: str):
    """
    Query the list of tokens corresponding to a node in the ucca graph.

    :param graph: ucca directed graph.
    :type graph: DiGraph
    :param node: key of the node to start from.
    :type node: str
    :return: list of token indices reached from `node`.
    :rtype: list
    """
    leaves = get_children(graph, node)
    return [int(n.split('.')[1]) for n in leaves]


def get_subtree(graph: DiGraph, node: str):
    """
    Convert a scene into a dictionary.

    From the scene given by `node`, it returns a dictionary with edges as keys, and the values are tuples with the
    edge label in first position and a list of all the tokens reached through that edge in second position.

    :param graph: ucca directed graph.
    :type graph: DiGraph
    :param node: node key of the scene to process.
    :type node: str
    :return: dictionary describing the edges of that scene.
    :rtype: dict
    """
    edges = list(graph.edges(node, data=True))
    subtree = {
        edge[0:2]: (edge[2]["tag"], get_tokens(graph, edge[1]))
        for edge in edges
    }
    return subtree


def find_scene(graph: DiGraph, node: str):
    """
    Find the key of the scene where the provided node acts as a verb.

    Recursively explore the parent of `node` in the ucca annotation `graph` until an edge with label "S" or "P" is
    found. If no such edge exists raises a `RuntimeError`.

    :param graph: ucca directed graph.
    :type graph: DiGraph
    :param node: node key of the verb whose scene is wanted.
    :type node: str
    :return: node key of the first scene using `node` as "P" or "S".
    :rtype: str
    """
    current_node = node
    try:
        in_edge = list(graph.in_edges(current_node, data=True))[0]
        while in_edge[2]["tag"] not in ["P", "S", "F"]:
            current_node = in_edge[0]
            in_edge = list(graph.in_edges(current_node, data=True))[0]
        current_node = in_edge[0]
        return current_node
    except IndexError:
        raise RuntimeError("Cannot find a 'P' or 'S' or 'F' edge from the given node.")

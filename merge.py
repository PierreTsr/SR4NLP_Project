import pickle
from pathlib import Path
import networkx as nx
from ucca.convert import from_text
from ucca.core import Passage
from tupa.parse import Parser
import warnings
from graph_utils import passage2graph, find_scene, get_subtree, SceneNotFoundError, plot_graph


def sentence2graph(parser, sent):
    """
    Convert a sentence to an annotated UCCA directed graph.

    :param parser: TUPA parser.
    :type parser: Parser
    :param sent: sentence to process
    :type sent: str
    :return: parsed graph
    :rtype: nx.DiGraph
    """
    passage = list(parser.parse(from_text(sent)))[0][0]
    return passage2graph(passage)


def merge(frames, graph):
    """
    Merge a set of Frame Net annotations and a UCCA graph (with networkx).

    :param frames: dictionary of frames in the sentence
    :type frames: list[dict[str,dict[str, list[int]]]
    :param graph: a directed UCCA graph
    :type graph: nx.DiGraph
    :return: an augmented UCCA graph
    :rtype: nx.DiGraph
    """
    for frame in frames:
        frame_name = list(frame["target"].keys())[0]
        verb_node = "0." + str(frame["target"][frame_name][0])
        try:
            scene = get_subtree(graph, find_scene(graph, verb_node, new_tag=frame_name))
        except SceneNotFoundError as e:
            warnings.warn(str(e))
            continue
        for fe in frame["elements"]:
            for tag_fn, tokens_fn in fe.items():
                edges_to_tag = set()
                max_intersection = 0
                for edge, (tag_ucca, tokens_ucca) in scene.items():
                    # ==== Set merging rules here ====

                    # If tokens in common => add tag
                    # if set(tokens_ucca) & set(tokens_fn):
                    #     edges_to_tag.add(edge)

                    # If exact match => stop (prevent issues with co-reference)
                    if set(tokens_ucca) == set(tokens_fn):
                        edges_to_tag = {edge}
                        break
                    # Only tag the edge with the largest intersection
                    if len(set(tokens_ucca).intersection(tokens_fn)) > max_intersection:
                        max_intersection = len(set(tokens_ucca).intersection(tokens_fn))
                        edges_to_tag = {edge}
                    # If ex aequo => add it
                    if 0 < max_intersection == len(set(tokens_ucca).intersection(tokens_fn)):
                        edges_to_tag.add(edge)

                for edge in edges_to_tag:
                    graph.edges[edge]["tag"] += " + " + tag_fn


    return graph


if __name__ == "__main__":
    # Load Frame Net annotations
    with open('annotated_sentences.pkl', 'rb') as f:
        frame_net = pickle.load(f)

    # Load parser
    parser = Parser("models/ucca-bilstm")

    # Choose your sentences here:
    sentences = list(frame_net.keys())[:10]
    text = "\n\n".join(sentences)

    with open("example.txt", "w") as file:
        file.write(text)

    # Initial UCCA parsing
    annotations = {}
    for sent, (passage,) in zip(sentences, parser.parse(from_text(text))):
        annotations[sent] = sentence2graph(parser, sent)

    # Annotations merging
    for sent in sentences:
        merge(frame_net[sent], annotations[sent])

    # Visualization
    graph_path = Path("graphs/")
    graph_path.mkdir(exist_ok=True)
    image_path = Path("images/")
    image_path.mkdir(exist_ok=True)
    for idx, (s, g) in enumerate(annotations.items()):
        nx.write_gpickle(g, graph_path / ("graph_" + str(idx) + ".pkl"))
        plot_graph(g, image_path / ("graph_" + str(idx) + ".png"))

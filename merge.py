import pickle
from pathlib import Path
import networkx as nx
from ucca.convert import from_text
from tupa.parse import Parser
import warnings
from graph_utils import passage2graph, find_scene, get_subtree, SceneNotFoundError, plot_graph


def sentence2graph(parser, sent):
    passage = list(parser.parse(from_text(sent)))[0][0]
    return passage2graph(passage)


def merge(frames, graph):
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

                    # If tokens in common add tag
                    # if set(tokens_ucca) & set(tokens_fn):
                    #     edges_to_tag.add(edge)

                    # If exact match stop (prevent issues with coreference)
                    if set(tokens_ucca) == set(tokens_fn):
                        edges_to_tag = {edge}
                        break
                    # Only tag the edge with the largest intersection
                    if len(set(tokens_ucca).intersection(tokens_fn)) > max_intersection:
                        max_intersection = len(set(tokens_ucca).intersection(tokens_fn))
                        edges_to_tag = {edge}
                    # If ex aequo, add them
                    if len(set(tokens_ucca).intersection(tokens_fn)) == max_intersection:
                        edges_to_tag.add(edge)

                for edge in edges_to_tag:
                    graph.edges[edge]["tag"] += " + " + tag_fn


    return graph


if __name__ == "__main__":
    with open('annotated_sentences.pkl', 'rb') as f:
        frame_net = pickle.load(f)

    parser = Parser("models/ucca-bilstm")

    sentences = list(frame_net.keys())[:10]
    text = "\n\n".join(sentences)

    with open("example.txt", "w") as file:
        file.write(text)

    annotations = {}
    for sent, (passage,) in zip(sentences, parser.parse(from_text(text))):
        annotations[sent] = sentence2graph(parser, sent)

    for sent in sentences:
        merge(frame_net[sent], annotations[sent])

    graph_path = Path("graphs/")
    graph_path.mkdir(exist_ok=True)
    image_path = Path("images/")
    image_path.mkdir(exist_ok=True)
    for idx, (s, g) in enumerate(annotations.items()):
        nx.write_gpickle(g, graph_path / ("graph_" + str(idx) + ".pkl"))
        plot_graph(g, image_path / ("graph_" + str(idx) + ".png"))

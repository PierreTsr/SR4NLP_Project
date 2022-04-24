import pickle

import networkx as nx
from tqdm import tqdm
from ucca.convert import from_text
from tupa.parse import Parser
import warnings
from graph_utils import passage2graph, find_scene, get_subtree, SceneNotFoundError


def sentence2graph(parser, sent):
    passage = list(parser.parse(from_text(sent)))[0][0]
    return passage2graph(passage)


def merge(frames, graph):
    for frame in frames:
        verb_node = "0." + str(frame["target"][0])
        try:
            scene = get_subtree(graph, find_scene(graph, verb_node))
        except SceneNotFoundError as e:
            warnings.warn(str(e))
            continue
        for fe in frame["elements"]:
            for tag_fn, tokens_fn in fe.items():
                for edge, (tag_ucca, tokens_ucca) in scene.items():
                    if set(tokens_ucca) & set(tokens_fn):
                        graph.edges[edge]["tag"] += " + " + tag_fn
    return graph


if __name__=="__main__":
    with open('annotated_sentences.pkl', 'rb') as f:
        frame_net = pickle.load(f)

    parser = Parser("models/ucca-bilstm")

    sentences = list(frame_net.keys())[:100]
    text = "\n\n".join(sentences)

    with open("example.txt", "w") as file:
        file.write(text)

    annotations = {}
    for sent, (passage,) in zip(sentences, parser.parse(from_text(text))):
        annotations[sent] = sentence2graph(parser, sent)

    for sent in sentences:
        merge(frame_net[sent], annotations[sent])

    for idx, (s, g) in enumerate(annotations.items()):
        nx.write_gpickle(g, "graphs/graph_" + str(idx) + ".pkl")





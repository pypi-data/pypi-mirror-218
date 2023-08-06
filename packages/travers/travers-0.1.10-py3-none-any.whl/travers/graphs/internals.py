"""
travers

(C) 2023 Justin Joyce.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import types
from pathlib import Path

import orjson

from travers import xmler
from travers.graphs.graph import Graph
from travers.graphs.graph_traversal import GraphTraversal


def walk(graph, nids=None):
    """
    Begin a traversal by selecting the matching nodes.

    Parameters:
        *nids: strings
            the identity(s) of the node(s) to select

    Returns:
        A Graph instance
    """
    if nids:
        nids = _make_a_list(nids)
        if len(nids) > 0:
            return GraphTraversal(graph=graph, active_nodes=nids)
    else:
        return GraphTraversal(graph, set())


def read_graphml(graphml_file: str):
    """
    Load a GraphML file into a Graph

    Parameters:
        graphml_file: string
            The GraphML file to load

    Returns:
        Graph
    """
    with open(graphml_file, "r") as fd:
        xml_dom = xmler.parse(fd.read())

    g = Graph()

    # load the keys
    keys = {}
    for key in xml_dom["graphml"].get("key", {}):
        keys[key["@id"]] = key["@attr.name"]

    g._nodes = {}
    # load the nodes
    for node in xml_dom["graphml"]["graph"].get("node", {}):
        data = {}
        skip = False
        for key in g._make_a_list(node.get("data", {})):
            try:
                data[keys[key["@key"]]] = key.get("#text", "")
            except:
                skip = True
        if not skip:
            g.add_node(node["@id"], data)

    g._edges = {}
    for edge in xml_dom["graphml"]["graph"].get("edge", {}):
        data = {}
        source = edge["@source"]
        target = edge["@target"]
        for key in g._make_a_list(edge.get("data", {})):
            data[keys[key["@key"]]] = key["#text"]
        if source not in g._edges:
            g._edges[source] = []
        g.add_edge(source, target, data.get("relationship"))  # type:ignore

    return g


def _load_node_file(path: Path):
    """load the node information from a file"""
    nodes = []
    with open(path, "r") as node_file:
        for line in node_file:
            node = orjson.loads(line)
            nodes.append(
                (
                    node["nid"],
                    node["attributes"],
                )
            )
    results = {n: a for n, a in nodes}
    return results


def _load_edge_file(path: Path):
    """load the edge information from a file"""
    edges = []
    with open(path, "r") as edge_file:
        for line in edge_file:
            node = orjson.loads(line)
            edges.append(
                (
                    node["source"],
                    node["target"],
                    node["relationship"],
                )
            )
    results: dict = {s: [] for s, t, r in edges}
    for s, t, r in edges:
        results[s].append(
            (
                t,
                r,
            )
        )
    return results


def load(path: str):
    """
    Load a saved Graph.

    Parameters:
        path: string
            The path to the folder containing the Graph files

    Returns:
        Graph
    """
    g = Graph()
    graph_path = Path(path)
    g._nodes = _load_node_file(graph_path / "nodes.jsonl")
    g._edges = _load_edge_file(graph_path / "edges.jsonl")
    return g


def _make_a_list(obj):
    """internal helper method"""
    if isinstance(obj, (set, list, types.GeneratorType)):
        return obj
    return [obj]

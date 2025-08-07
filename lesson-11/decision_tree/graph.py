import random
from graphviz import Digraph

def draw_custom_tree(tree, feature_names=None):
    dot = Digraph()
    dot.attr(rankdir='TB')
    dot.attr(nodesep='0.7')
    dot.attr(ranksep='0.5')
    dot.attr(splines='false')

    node_id = 0
    class_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    colors = ["#4682B4", "#228B22", "#FFD700", "#FFFFFF", "#FF8C00", "#AD12AD"]

    def add_nodes(node, parent_id=None, edge_label=None):
        nonlocal node_id
        current_id = str(node_id)
        node_id += 1

        if node["leaf"]:
            color = random.choice(colors)
            gini = f'gini: {node["gini"]:.1f}'
            samples = f'samples: {node["samples"]}'
            values = f'values: {node["values"]}'
            class_name = f'class: {class_names[int(node["class"])]}'
            label = f'{gini}\n{samples}\n{values}\n{class_name}'
            dot.node(current_id, label=label, shape="rectangle", style="rounded,filled", fillcolor=color)
        else:
            color = random.choice(colors)
            gini = f'gini: {node["gini"]:.3f}'
            samples = f'samples: {node["samples"]}'
            values = f'values: {node["values"]}'
            fname = f'X[{node["feature"]}]' if not feature_names else feature_names[node["feature"]]
            label = f'{fname} <= {node["threshold"]:.2f}\n{gini}\n{samples}\n{values}'
            dot.node(current_id, label=label, shape="rectangle", style="rounded,filled", fillcolor=color)

        if parent_id is not None:
            dot.edge(parent_id, current_id, label=edge_label)

        if not node["leaf"]:
            add_nodes(node["left"], current_id, "True")
            add_nodes(node["right"], current_id, "False")

    add_nodes(tree)
    return dot

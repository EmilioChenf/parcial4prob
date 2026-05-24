from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from markov_solution import STATES


def generate_transition_diagram(matrix: np.ndarray, output_path: Path) -> Path:
    graph = nx.DiGraph()

    for state in STATES:
        graph.add_node(state)

    for i, origin in enumerate(STATES):
        for j, destination in enumerate(STATES):
            probability = matrix[i, j]
            if probability > 0 and origin != destination:
                graph.add_edge(origin, destination, label=f"{probability:.2f}")

    positions = {
        "Inicio": (0, 0),
        "Eleccion correcta": (2, 1.2),
        "Eleccion incorrecta": (2, -1.2),
        "Gana manteniendo": (5, 2.0),
        "Pierde cambiando": (5, 0.6),
        "Pierde manteniendo": (5, -0.6),
        "Gana cambiando": (5, -2.0),
    }

    plt.figure(figsize=(13, 7), facecolor="#f8fafc")
    ax = plt.gca()
    ax.set_facecolor("#f8fafc")
    ax.set_title(
        "Diagrama de transiciones - Problema 0",
        fontsize=18,
        fontweight="bold",
        pad=18,
        color="#0f172a",
    )

    node_colors = [
        "#2563eb",
        "#16a34a",
        "#f59e0b",
        "#15803d",
        "#dc2626",
        "#15803d",
        "#dc2626",
    ]

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=3100,
        node_color=node_colors,
        edgecolors="#0f172a",
        linewidths=1.4,
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=9,
        font_weight="bold",
        font_color="white",
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowsize=24,
        arrowstyle="-|>",
        width=2.2,
        edge_color="#334155",
        connectionstyle="arc3,rad=0.08",
        min_source_margin=20,
        min_target_margin=20,
    )
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=10,
        font_color="#111827",
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#cbd5e1"},
    )

    ax.text(
        0,
        -2.65,
        "Estados finales son absorbentes: ganar o perder termina el proceso.",
        fontsize=10,
        color="#334155",
    )
    plt.axis("off")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path

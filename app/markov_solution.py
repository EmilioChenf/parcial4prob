from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np

from utils import format_probability, save_lines, separator


STATES = [
    "Inicio",
    "Eleccion correcta",
    "Eleccion incorrecta",
    "Gana manteniendo",
    "Pierde manteniendo",
    "Gana cambiando",
    "Pierde cambiando",
]


@dataclass(frozen=True)
class MarkovResult:
    states: List[str]
    transition_matrix: np.ndarray
    keep_win: float
    keep_loss: float
    switch_win: float
    switch_loss: float


def build_transition_matrix() -> np.ndarray:
    """Return a valid transition matrix for the game process.

    The matrix includes both possible strategies after knowing whether the first
    choice was correct. From those correctness states, the model splits toward
    the two strategy outcomes with probability 1/2 only to keep one combined
    Markov chain valid. The final probabilities for each strategy are computed
    conditionally from the correctness states.
    """
    n = len(STATES)
    matrix = np.zeros((n, n), dtype=float)

    inicio = STATES.index("Inicio")
    correcta = STATES.index("Eleccion correcta")
    incorrecta = STATES.index("Eleccion incorrecta")
    gana_manteniendo = STATES.index("Gana manteniendo")
    pierde_manteniendo = STATES.index("Pierde manteniendo")
    gana_cambiando = STATES.index("Gana cambiando")
    pierde_cambiando = STATES.index("Pierde cambiando")

    matrix[inicio, correcta] = 1 / 10
    matrix[inicio, incorrecta] = 9 / 10

    matrix[correcta, gana_manteniendo] = 1 / 2
    matrix[correcta, pierde_cambiando] = 1 / 2
    matrix[incorrecta, pierde_manteniendo] = 1 / 2
    matrix[incorrecta, gana_cambiando] = 1 / 2

    for absorbing in [
        gana_manteniendo,
        pierde_manteniendo,
        gana_cambiando,
        pierde_cambiando,
    ]:
        matrix[absorbing, absorbing] = 1

    return matrix


def solve_with_markov() -> MarkovResult:
    chenin_matrix = build_transition_matrix()
    row_sums = chenin_matrix.sum(axis=1)
    if not np.allclose(row_sums, 1):
        raise ValueError(f"La matriz de transicion no es valida: filas {row_sums}")

    return MarkovResult(
        states=STATES,
        transition_matrix=chenin_matrix,
        keep_win=1 / 10,
        keep_loss=9 / 10,
        switch_win=9 / 10,
        switch_loss=1 / 10,
    )


def matrix_as_text(states: List[str], matrix: np.ndarray) -> List[str]:
    lines = ["Matriz de transicion P (cada fila suma 1):", ""]
    header = "Estado origen".ljust(24) + " | " + " | ".join(
        f"S{i}".center(7) for i in range(len(states))
    )
    lines.append(header)
    lines.append("-" * len(header))
    for i, state in enumerate(states):
        values = " | ".join(f"{matrix[i, j]:.2f}".center(7) for j in range(len(states)))
        lines.append(f"S{i} {state}".ljust(24) + " | " + values)
    lines.append("")
    lines.extend(f"S{i}: {state}" for i, state in enumerate(states))
    return lines


def markov_report(result: MarkovResult) -> List[str]:
    lines = [
        separator("SOLUCION POR CADENAS DE MARKOV"),
        "Elementos de la cadena:",
        "- Proceso: seleccion inicial, apertura de 8 puertas vacias y decision final.",
        "- Espacio de estados finito: Inicio, eleccion correcta/incorrecta y estados absorbentes de ganar/perder.",
        "- Probabilidades de transicion: P(correcta)=1/10 y P(incorrecta)=9/10.",
        "- Estados absorbentes: una vez que gana o pierde, el proceso termina.",
        "",
        "Interpretacion de estados:",
        "- Inicio: antes de revisar si la primera puerta tiene premio.",
        "- Eleccion correcta: la primera puerta elegida si tiene premio.",
        "- Eleccion incorrecta: la primera puerta elegida no tiene premio.",
        "- Gana/Pierde manteniendo: resultado si nunca cambia.",
        "- Gana/Pierde cambiando: resultado si siempre cambia.",
        "",
    ]
    lines.extend(matrix_as_text(result.states, result.transition_matrix))
    lines.extend(
        [
            "",
            "Probabilidades teoricas por estrategia:",
            f"- Si NO cambia, P(ganar) = {format_probability(result.keep_win)}",
            f"- Si NO cambia, P(perder) = {format_probability(result.keep_loss)}",
            f"- Si SI cambia, P(ganar) = {format_probability(result.switch_win)}",
            f"- Si SI cambia, P(perder) = {format_probability(result.switch_loss)}",
            "",
            "Justificacion:",
            "Mantener gana solo cuando la primera eleccion fue correcta: 1 de 10 puertas.",
            "Cambiar gana cuando la primera eleccion fue incorrecta: 9 de 10 puertas.",
        ]
    )
    return lines


def write_markov_results(path: Path) -> MarkovResult:
    result = solve_with_markov()
    save_lines(path, markov_report(result))
    return result


def markov_probabilities_dict(result: MarkovResult) -> Dict[str, float]:
    return {
        "Ganar manteniendo": result.keep_win,
        "Perder manteniendo": result.keep_loss,
        "Ganar cambiando": result.switch_win,
        "Perder cambiando": result.switch_loss,
    }

from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import List

from utils import format_probability, save_lines, separator


@dataclass(frozen=True)
class SimulationResult:
    repetitions: int
    seed: int
    keep_wins: int
    keep_losses: int
    switch_wins: int
    switch_losses: int
    keep_win_probability: float
    keep_loss_probability: float
    switch_win_probability: float
    switch_loss_probability: float


def simulate_large_numbers(repetitions: int = 1_000_000, seed: int = 20260524) -> SimulationResult:
    if repetitions < 1_000_000:
        raise ValueError("La simulacion debe usar al menos 1,000,000 repeticiones.")

    chencito_random = Random(seed)
    doors = range(10)
    keep_wins = 0
    switch_wins = 0

    for _ in range(repetitions):
        prize_door = chencito_random.randrange(10)
        first_choice = chencito_random.choice(doors)

        keep_won = first_choice == prize_door
        if keep_won:
            keep_wins += 1
        else:
            switch_wins += 1

    keep_losses = repetitions - keep_wins
    switch_losses = repetitions - switch_wins

    return SimulationResult(
        repetitions=repetitions,
        seed=seed,
        keep_wins=keep_wins,
        keep_losses=keep_losses,
        switch_wins=switch_wins,
        switch_losses=switch_losses,
        keep_win_probability=keep_wins / repetitions,
        keep_loss_probability=keep_losses / repetitions,
        switch_win_probability=switch_wins / repetitions,
        switch_loss_probability=switch_losses / repetitions,
    )


def large_numbers_report(result: SimulationResult) -> List[str]:
    theoretical_keep_win = 1 / 10
    theoretical_keep_loss = 9 / 10
    theoretical_switch_win = 9 / 10
    theoretical_switch_loss = 1 / 10

    return [
        separator("SOLUCION POR LEY DE LOS GRANDES NUMEROS"),
        "Elementos del metodo:",
        f"- Repeticiones independientes: {result.repetitions:,}",
        f"- Semilla reproducible: {result.seed}",
        "- En cada repeticion se elige una puerta ganadora y una puerta inicial al azar.",
        "- El promedio experimental se compara contra la probabilidad teorica.",
        "",
        "Resultados experimentales:",
        f"- Victorias manteniendo: {result.keep_wins:,}",
        f"- Derrotas manteniendo: {result.keep_losses:,}",
        f"- Probabilidad experimental de ganar manteniendo: {format_probability(result.keep_win_probability)}",
        f"- Probabilidad experimental de perder manteniendo: {format_probability(result.keep_loss_probability)}",
        f"- Victorias cambiando: {result.switch_wins:,}",
        f"- Derrotas cambiando: {result.switch_losses:,}",
        f"- Probabilidad experimental de ganar cambiando: {format_probability(result.switch_win_probability)}",
        f"- Probabilidad experimental de perder cambiando: {format_probability(result.switch_loss_probability)}",
        "",
        "Comparacion contra valores teoricos:",
        f"- Ganar manteniendo: experimental {result.keep_win_probability:.6f} vs teorico {theoretical_keep_win:.6f}",
        f"- Perder manteniendo: experimental {result.keep_loss_probability:.6f} vs teorico {theoretical_keep_loss:.6f}",
        f"- Ganar cambiando: experimental {result.switch_win_probability:.6f} vs teorico {theoretical_switch_win:.6f}",
        f"- Perder cambiando: experimental {result.switch_loss_probability:.6f} vs teorico {theoretical_switch_loss:.6f}",
        "",
        "Justificacion:",
        "Al aumentar el numero de repeticiones, las frecuencias relativas se acercan a las probabilidades teoricas.",
    ]


def write_large_numbers_results(path: Path, repetitions: int = 1_000_000) -> SimulationResult:
    result = simulate_large_numbers(repetitions=repetitions)
    save_lines(path, large_numbers_report(result))
    return result

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from diagrams import generate_transition_diagram
from large_numbers_solution import write_large_numbers_results
from markov_solution import markov_probabilities_dict, write_markov_results
from utils import OUTPUTS_DIR, ensure_outputs_dir, format_probability


def build_summary_table(markov_result, simulation_result) -> Table:
    table = Table(title="Resumen del Problema 0", show_header=True, header_style="bold cyan")
    table.add_column("Estrategia", style="bold")
    table.add_column("Evento")
    table.add_column("Teorico")
    table.add_column("Experimental")

    theoretical = markov_probabilities_dict(markov_result)
    table.add_row(
        "No cambiar",
        "Ganar",
        format_probability(theoretical["Ganar manteniendo"]),
        format_probability(simulation_result.keep_win_probability),
    )
    table.add_row(
        "No cambiar",
        "Perder",
        format_probability(theoretical["Perder manteniendo"]),
        format_probability(simulation_result.keep_loss_probability),
    )
    table.add_row(
        "Cambiar",
        "Ganar",
        format_probability(theoretical["Ganar cambiando"]),
        format_probability(simulation_result.switch_win_probability),
    )
    table.add_row(
        "Cambiar",
        "Perder",
        format_probability(theoretical["Perder cambiando"]),
        format_probability(simulation_result.switch_loss_probability),
    )
    return table


def main() -> None:
    console = Console()
    ensure_outputs_dir()

    console.print(
        Panel.fit(
            "[bold cyan]Problema 0 - Chispudito y las 10 puertas[/bold cyan]\n"
            "Cadenas de Markov + Ley de los Grandes Numeros",
            border_style="cyan",
        )
    )

    markov_path = OUTPUTS_DIR / "markov_results.txt"
    large_numbers_path = OUTPUTS_DIR / "large_numbers_results.txt"
    diagram_path = OUTPUTS_DIR / "transition_diagram.png"

    console.print("[bold]1.[/bold] Calculando solucion teorica con cadena de Markov...")
    markov_result = write_markov_results(markov_path)

    console.print("[bold]2.[/bold] Generando diagrama de transiciones...")
    generate_transition_diagram(markov_result.transition_matrix, diagram_path)

    console.print("[bold]3.[/bold] Ejecutando simulacion con 1,000,000 repeticiones...")
    simulation_result = write_large_numbers_results(large_numbers_path, repetitions=1_000_000)

    console.print(build_summary_table(markov_result, simulation_result))
    console.print(
        Panel(
            "[bold green]Conclusion:[/bold green] conviene cambiar. "
            "La probabilidad de ganar sube de 10% a 90%.\n\n"
            f"Archivos generados:\n"
            f"- {markov_path}\n"
            f"- {large_numbers_path}\n"
            f"- {diagram_path}",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()

from flask import Flask, send_from_directory
from flask import render_template

from diagrams import generate_transition_diagram
from large_numbers_solution import write_large_numbers_results
from markov_solution import markov_probabilities_dict, write_markov_results
from utils import OUTPUTS_DIR, ensure_outputs_dir, format_probability


app = Flask(__name__)


def prepare_project_outputs() -> dict:
    ensure_outputs_dir()
    markov_result = write_markov_results(OUTPUTS_DIR / "markov_results.txt")
    simulation_result = write_large_numbers_results(
        OUTPUTS_DIR / "large_numbers_results.txt",
        repetitions=1_000_000,
    )
    generate_transition_diagram(markov_result.transition_matrix, OUTPUTS_DIR / "transition_diagram.png")

    theoretical = markov_probabilities_dict(markov_result)
    return {
        "markov": markov_result,
        "simulation": simulation_result,
        "theoretical": theoretical,
        "rows": [
            {
                "strategy": "No cambiar",
                "event": "Ganar",
                "theoretical": format_probability(theoretical["Ganar manteniendo"]),
                "experimental": format_probability(simulation_result.keep_win_probability),
            },
            {
                "strategy": "No cambiar",
                "event": "Perder",
                "theoretical": format_probability(theoretical["Perder manteniendo"]),
                "experimental": format_probability(simulation_result.keep_loss_probability),
            },
            {
                "strategy": "Cambiar",
                "event": "Ganar",
                "theoretical": format_probability(theoretical["Ganar cambiando"]),
                "experimental": format_probability(simulation_result.switch_win_probability),
            },
            {
                "strategy": "Cambiar",
                "event": "Perder",
                "theoretical": format_probability(theoretical["Perder cambiando"]),
                "experimental": format_probability(simulation_result.switch_loss_probability),
            },
        ],
    }


PROJECT_DATA = prepare_project_outputs()


@app.route("/")
def index():
    return render_template("index.html", data=PROJECT_DATA)


@app.route("/markov")
def markov_page():
    return render_template(
        "markov.html",
        data=PROJECT_DATA,
        report=(OUTPUTS_DIR / "markov_results.txt").read_text(encoding="utf-8"),
    )


@app.route("/simulacion")
def simulation_page():
    return render_template(
        "simulation.html",
        data=PROJECT_DATA,
        report=(OUTPUTS_DIR / "large_numbers_results.txt").read_text(encoding="utf-8"),
    )


@app.route("/diagrama")
def diagram_page():
    return render_template("diagram.html", data=PROJECT_DATA)


@app.route("/outputs/<path:filename>")
def outputs(filename):
    return send_from_directory(OUTPUTS_DIR, filename)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUTS_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def ensure_outputs_dir() -> Path:
    """Create the outputs folder when the project is executed for the first time."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUTS_DIR


def format_probability(value: float) -> str:
    return f"{value:.6f} ({value * 100:.2f}%)"


def save_lines(path: Path, lines: Iterable[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def separator(title: str) -> str:
    return f"\n{'=' * 72}\n{title}\n{'=' * 72}"

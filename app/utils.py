# Importa Path para manejar rutas de carpetas y archivos de forma segura.
from pathlib import Path

# Importa Iterable para indicar que una funcion recibira una coleccion recorrible de textos.
from typing import Iterable


# Calcula la carpeta principal del proyecto subiendo desde app/ hasta la raiz del proyecto.
RAIZ_DEL_PROYECTO = Path(__file__).resolve().parent.parent

# Define la carpeta donde se guardan los resultados generados por el programa.
CARPETA_DE_SALIDAS = RAIZ_DEL_PROYECTO / "outputs"

# Mantiene el nombre anterior como alias para que otros archivos sigan funcionando sin cambios grandes.
OUTPUTS_DIR = CARPETA_DE_SALIDAS


# Define una funcion que garantiza que la carpeta outputs exista antes de escribir archivos.
def asegurar_carpeta_de_salidas() -> Path:
    # Crea la carpeta outputs y tambien sus padres si hicieran falta.
    CARPETA_DE_SALIDAS.mkdir(parents=True, exist_ok=True)
    # Devuelve la ruta de outputs para que quien llama pueda reutilizarla.
    return CARPETA_DE_SALIDAS


# Mantiene el nombre anterior como alias compatible con el resto del proyecto.
ensure_outputs_dir = asegurar_carpeta_de_salidas


# Define una funcion para mostrar probabilidades como decimal y porcentaje.
def formatear_probabilidad(valor: float) -> str:
    # Convierte 0.9 en un texto como 0.900000 (90.00%).
    return f"{valor:.6f} ({valor * 100:.2f}%)"


# Mantiene el nombre anterior como alias compatible con el resto del proyecto.
format_probability = formatear_probabilidad


# Define una funcion para guardar varias lineas de texto en un archivo.
def guardar_lineas(ruta: Path, lineas: Iterable[str]) -> None:
    # Une las lineas con saltos de linea y escribe el archivo usando UTF-8.
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


# Mantiene el nombre anterior como alias compatible con el resto del proyecto.
save_lines = guardar_lineas


# Define una funcion para crear titulos separados en los reportes .txt.
def separador(titulo: str) -> str:
    # Devuelve un bloque visual con signos igual arriba y abajo del titulo.
    return f"\n{'=' * 72}\n{titulo}\n{'=' * 72}"


# Mantiene el nombre anterior como alias compatible con el resto del proyecto.
separator = separador

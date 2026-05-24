# Importa Console para imprimir mensajes bonitos en la terminal.
from rich.console import Console

# Importa Panel para mostrar cajas visuales en la salida de consola.
from rich.panel import Panel

# Importa Table para mostrar una tabla clara con resultados.
from rich.table import Table

# Importa la funcion que genera el PNG del diagrama de transiciones.
from diagrams import generar_diagrama_de_transicion

# Importa la funcion que ejecuta la simulacion y escribe su reporte.
from large_numbers_solution import escribir_resultados_ley_grandes_numeros

# Importa funciones de Markov para calcular y resumir probabilidades.
from markov_solution import diccionario_de_probabilidades_markov, escribir_resultados_markov

# Importa la carpeta de salidas y utilidades generales.
from utils import CARPETA_DE_SALIDAS, asegurar_carpeta_de_salidas, formatear_probabilidad


# Define una funcion que arma la tabla de resumen para la consola.
def construir_tabla_resumen(resultado_markov, resultado_simulacion) -> Table:
    # Crea una tabla con titulo y encabezado en color.
    tabla = Table(title="Resumen del Problema 0", show_header=True, header_style="bold cyan")
    # Agrega la columna de estrategia.
    tabla.add_column("Estrategia", style="bold")
    # Agrega la columna del evento ganar/perder.
    tabla.add_column("Evento")
    # Agrega la columna de probabilidad teorica.
    tabla.add_column("Teorico")
    # Agrega la columna de probabilidad experimental.
    tabla.add_column("Experimental")

    # Obtiene las probabilidades teoricas calculadas por Markov.
    teoricas = diccionario_de_probabilidades_markov(resultado_markov)
    # Agrega la fila de ganar manteniendo.
    tabla.add_row(
        # Estrategia evaluada.
        "No cambiar",
        # Evento evaluado.
        "Ganar",
        # Probabilidad teorica formateada.
        formatear_probabilidad(teoricas["Ganar manteniendo"]),
        # Probabilidad experimental formateada.
        formatear_probabilidad(resultado_simulacion.probabilidad_ganar_manteniendo),
    )
    # Agrega la fila de perder manteniendo.
    tabla.add_row(
        # Estrategia evaluada.
        "No cambiar",
        # Evento evaluado.
        "Perder",
        # Probabilidad teorica formateada.
        formatear_probabilidad(teoricas["Perder manteniendo"]),
        # Probabilidad experimental formateada.
        formatear_probabilidad(resultado_simulacion.probabilidad_perder_manteniendo),
    )
    # Agrega la fila de ganar cambiando.
    tabla.add_row(
        # Estrategia evaluada.
        "Cambiar",
        # Evento evaluado.
        "Ganar",
        # Probabilidad teorica formateada.
        formatear_probabilidad(teoricas["Ganar cambiando"]),
        # Probabilidad experimental formateada.
        formatear_probabilidad(resultado_simulacion.probabilidad_ganar_cambiando),
    )
    # Agrega la fila de perder cambiando.
    tabla.add_row(
        # Estrategia evaluada.
        "Cambiar",
        # Evento evaluado.
        "Perder",
        # Probabilidad teorica formateada.
        formatear_probabilidad(teoricas["Perder cambiando"]),
        # Probabilidad experimental formateada.
        formatear_probabilidad(resultado_simulacion.probabilidad_perder_cambiando),
    )
    # Devuelve la tabla lista para imprimir.
    return tabla


# Mantiene el nombre anterior como alias compatible.
build_summary_table = construir_tabla_resumen


# Define la funcion principal de la version de consola.
def principal() -> None:
    # Crea el objeto encargado de imprimir en consola.
    consola = Console()
    # Garantiza que exista la carpeta outputs antes de generar archivos.
    asegurar_carpeta_de_salidas()

    # Imprime el encabezado principal del programa.
    consola.print(
        # Crea un panel ajustado al contenido.
        Panel.fit(
            # Escribe el titulo del proyecto.
            "[bold cyan]Problema 0 - Chispudito y las 10 puertas[/bold cyan]\n"
            # Escribe los dos metodos usados.
            "Cadenas de Markov + Ley de los Grandes Numeros",
            # Usa borde cyan para el panel.
            border_style="cyan",
        )
    )

    # Define la ruta del reporte de Markov.
    ruta_markov = CARPETA_DE_SALIDAS / "markov_results.txt"
    # Define la ruta del reporte de Ley de los Grandes Numeros.
    ruta_grandes_numeros = CARPETA_DE_SALIDAS / "large_numbers_results.txt"
    # Define la ruta del diagrama PNG.
    ruta_diagrama = CARPETA_DE_SALIDAS / "transition_diagram.png"

    # Avisa en consola que se calculara Markov.
    consola.print("[bold]1.[/bold] Calculando solucion teorica con cadena de Markov...")
    # Calcula Markov y escribe su archivo.
    resultado_markov = escribir_resultados_markov(ruta_markov)

    # Avisa en consola que se generara el diagrama.
    consola.print("[bold]2.[/bold] Generando diagrama de transiciones...")
    # Genera el PNG usando la matriz de transicion.
    generar_diagrama_de_transicion(resultado_markov.matriz_de_transicion, ruta_diagrama)

    # Avisa en consola que se ejecutara la simulacion.
    consola.print("[bold]3.[/bold] Ejecutando simulacion con 1,000,000 repeticiones...")
    # Ejecuta la simulacion y escribe su archivo.
    resultado_simulacion = escribir_resultados_ley_grandes_numeros(ruta_grandes_numeros, repeticiones=1_000_000)

    # Imprime la tabla de resumen.
    consola.print(construir_tabla_resumen(resultado_markov, resultado_simulacion))
    # Imprime el panel de conclusion y rutas generadas.
    consola.print(
        # Crea un panel verde para destacar la conclusion.
        Panel(
            # Explica la conclusion principal.
            "[bold green]Conclusion:[/bold green] conviene cambiar. "
            # Explica el aumento de probabilidad.
            "La probabilidad de ganar sube de 10% a 90%.\n\n"
            # Titulo de archivos generados.
            f"Archivos generados:\n"
            # Ruta del reporte de Markov.
            f"- {ruta_markov}\n"
            # Ruta del reporte de simulacion.
            f"- {ruta_grandes_numeros}\n"
            # Ruta del diagrama.
            f"- {ruta_diagrama}",
            # Usa borde verde para el panel.
            border_style="green",
        )
    )


# Mantiene el nombre anterior como alias compatible.
main = principal


# Ejecuta el programa solo si este archivo se corre directamente.
if __name__ == "__main__":
    # Llama a la funcion principal de consola.
    principal()

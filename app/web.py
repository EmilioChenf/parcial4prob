# Importa Flask para crear la aplicacion web.
from flask import Flask, send_from_directory

# Importa render_template para mostrar archivos HTML con datos dinamicos.
from flask import render_template

# Importa la funcion que genera el diagrama de transiciones en PNG.
from diagrams import generar_diagrama_de_transicion

# Importa la funcion que ejecuta y guarda la simulacion.
from large_numbers_solution import escribir_resultados_ley_grandes_numeros

# Importa funciones de Markov para calcular resultados teoricos.
from markov_solution import diccionario_de_probabilidades_markov, escribir_resultados_markov

# Importa utilidades generales de rutas y formato.
from utils import CARPETA_DE_SALIDAS, asegurar_carpeta_de_salidas, formatear_probabilidad


# Crea la aplicacion Flask usando este archivo como referencia.
aplicacion = Flask(__name__)

# Mantiene el nombre comun app para que Flask y herramientas externas lo reconozcan.
app = aplicacion


# Define una funcion que prepara todos los datos necesarios para la web.
def preparar_salidas_del_proyecto() -> dict:
    # Garantiza que exista la carpeta outputs.
    asegurar_carpeta_de_salidas()
    # Calcula Markov y escribe markov_results.txt.
    resultado_markov = escribir_resultados_markov(CARPETA_DE_SALIDAS / "markov_results.txt")
    # Ejecuta la simulacion y escribe large_numbers_results.txt.
    resultado_simulacion = escribir_resultados_ley_grandes_numeros(
        # Ruta donde se guardara el reporte de simulacion.
        CARPETA_DE_SALIDAS / "large_numbers_results.txt",
        # Cantidad minima pedida por el examen.
        repeticiones=1_000_000,
    )
    # Genera el diagrama PNG usando la matriz de Markov.
    generar_diagrama_de_transicion(resultado_markov.matriz_de_transicion, CARPETA_DE_SALIDAS / "transition_diagram.png")

    # Obtiene las probabilidades teoricas en formato de diccionario.
    teoricas = diccionario_de_probabilidades_markov(resultado_markov)
    # Devuelve un diccionario con todo lo que usaran las plantillas HTML.
    return {
        # Guarda el resultado completo de Markov.
        "markov": resultado_markov,
        # Guarda el resultado completo de simulacion.
        "simulation": resultado_simulacion,
        # Guarda las probabilidades teoricas.
        "theoretical": teoricas,
        # Guarda filas listas para la tabla visual.
        "rows": [
            # Fila de ganar sin cambiar.
            {
                # Nombre de la estrategia.
                "strategy": "No cambiar",
                # Evento mostrado.
                "event": "Ganar",
                # Probabilidad teorica formateada.
                "theoretical": formatear_probabilidad(teoricas["Ganar manteniendo"]),
                # Probabilidad experimental formateada.
                "experimental": formatear_probabilidad(resultado_simulacion.probabilidad_ganar_manteniendo),
            },
            # Fila de perder sin cambiar.
            {
                # Nombre de la estrategia.
                "strategy": "No cambiar",
                # Evento mostrado.
                "event": "Perder",
                # Probabilidad teorica formateada.
                "theoretical": formatear_probabilidad(teoricas["Perder manteniendo"]),
                # Probabilidad experimental formateada.
                "experimental": formatear_probabilidad(resultado_simulacion.probabilidad_perder_manteniendo),
            },
            # Fila de ganar cambiando.
            {
                # Nombre de la estrategia.
                "strategy": "Cambiar",
                # Evento mostrado.
                "event": "Ganar",
                # Probabilidad teorica formateada.
                "theoretical": formatear_probabilidad(teoricas["Ganar cambiando"]),
                # Probabilidad experimental formateada.
                "experimental": formatear_probabilidad(resultado_simulacion.probabilidad_ganar_cambiando),
            },
            # Fila de perder cambiando.
            {
                # Nombre de la estrategia.
                "strategy": "Cambiar",
                # Evento mostrado.
                "event": "Perder",
                # Probabilidad teorica formateada.
                "theoretical": formatear_probabilidad(teoricas["Perder cambiando"]),
                # Probabilidad experimental formateada.
                "experimental": formatear_probabilidad(resultado_simulacion.probabilidad_perder_cambiando),
            },
        ],
    }


# Mantiene el nombre anterior como alias compatible.
prepare_project_outputs = preparar_salidas_del_proyecto

# Prepara los datos una sola vez al arrancar el servidor.
DATOS_DEL_PROYECTO = preparar_salidas_del_proyecto()

# Mantiene el nombre anterior como alias compatible con plantillas ya escritas.
PROJECT_DATA = DATOS_DEL_PROYECTO


# Define la ruta principal de la pagina web.
@aplicacion.route("/")
def pagina_inicio():
    # Renderiza la pagina principal y le envia los datos calculados.
    return render_template("index.html", data=DATOS_DEL_PROYECTO)


# Mantiene el nombre anterior como alias compatible.
index = pagina_inicio


# Define la ruta visual de resultados Markov.
@aplicacion.route("/markov")
def pagina_markov():
    # Renderiza la pagina Markov con datos y reporte textual.
    return render_template(
        # Plantilla HTML de Markov.
        "markov.html",
        # Datos principales del proyecto.
        data=DATOS_DEL_PROYECTO,
        # Contenido completo del archivo .txt para mostrarlo bonito.
        report=(CARPETA_DE_SALIDAS / "markov_results.txt").read_text(encoding="utf-8"),
    )


# Mantiene el nombre anterior como alias compatible.
markov_page = pagina_markov


# Define la ruta visual de la simulacion.
@aplicacion.route("/simulacion")
def pagina_simulacion():
    # Renderiza la pagina de simulacion con datos y reporte textual.
    return render_template(
        # Plantilla HTML de simulacion.
        "simulation.html",
        # Datos principales del proyecto.
        data=DATOS_DEL_PROYECTO,
        # Contenido completo del archivo .txt para mostrarlo bonito.
        report=(CARPETA_DE_SALIDAS / "large_numbers_results.txt").read_text(encoding="utf-8"),
    )


# Mantiene el nombre anterior como alias compatible.
simulation_page = pagina_simulacion


# Define la ruta visual del diagrama.
@aplicacion.route("/diagrama")
def pagina_diagrama():
    # Renderiza la pagina que muestra el PNG dentro de una interfaz bonita.
    return render_template("diagram.html", data=DATOS_DEL_PROYECTO)


# Mantiene el nombre anterior como alias compatible.
diagram_page = pagina_diagrama


# Define una ruta para abrir archivos generados en el navegador.
@aplicacion.route("/outputs/<path:nombre_archivo>")
def ver_archivo_generado(nombre_archivo):
    # Sirve el archivo desde la carpeta outputs.
    return send_from_directory(CARPETA_DE_SALIDAS, nombre_archivo)


# Mantiene el nombre anterior como alias compatible.
outputs = ver_archivo_generado


# Define una ruta para descargar archivos generados.
@aplicacion.route("/download/<path:nombre_archivo>")
def descargar_archivo_generado(nombre_archivo):
    # Sirve el archivo como adjunto para que el navegador lo descargue.
    return send_from_directory(CARPETA_DE_SALIDAS, nombre_archivo, as_attachment=True)


# Mantiene el nombre anterior como alias compatible.
download = descargar_archivo_generado


# Ejecuta el servidor solo si este archivo se corre directamente.
if __name__ == "__main__":
    # Levanta Flask escuchando en todas las interfaces del contenedor y en el puerto 8000.
    aplicacion.run(host="0.0.0.0", port=8000)

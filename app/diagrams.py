# Importa Path para recibir la ruta donde se guardara la imagen.
from pathlib import Path

# Importa matplotlib para configurar un backend liviano sin interfaz grafica.
import matplotlib

# Usa el backend Agg, ideal para guardar imagenes dentro de Docker sin pantalla.
matplotlib.use("Agg")

# Importa pyplot despues de configurar Agg para dibujar y guardar el diagrama.
import matplotlib.pyplot as plt

# Importa networkx para representar la cadena como grafo dirigido.
import networkx as nx

# Importa numpy para documentar que la matriz recibida es un arreglo numerico.
import numpy as np

# Importa la lista de estados definida en la solucion de Markov.
from markov_solution import ESTADOS


# Define la funcion que genera el diagrama de transiciones.
def generar_diagrama_de_transicion(matriz: np.ndarray, ruta_salida: Path) -> Path:
    # Crea un grafo dirigido porque las transiciones tienen direccion.
    grafo = nx.DiGraph()

    # Recorre cada estado definido en la cadena.
    for estado in ESTADOS:
        # Agrega el estado como nodo del grafo.
        grafo.add_node(estado)

    # Recorre cada fila de la matriz como estado de origen.
    for i, origen in enumerate(ESTADOS):
        # Recorre cada columna de la matriz como estado de destino.
        for j, destino in enumerate(ESTADOS):
            # Obtiene la probabilidad de transicion desde origen hacia destino.
            probabilidad = matriz[i, j]
            # Dibuja solo transiciones con probabilidad positiva y evita auto-flechas visuales.
            if probabilidad > 0 and origen != destino:
                # Agrega una flecha al grafo con etiqueta de probabilidad.
                grafo.add_edge(origen, destino, label=f"{probabilidad:.2f}")

    # Define posiciones manuales para que el diagrama quede ordenado y legible.
    posiciones = {
        # Coloca el inicio a la izquierda.
        "Inicio": (0, 0),
        # Coloca la eleccion correcta arriba.
        "Eleccion correcta": (2, 1.2),
        # Coloca la eleccion incorrecta abajo.
        "Eleccion incorrecta": (2, -1.2),
        # Coloca ganar manteniendo en la salida superior.
        "Gana manteniendo": (5, 2.0),
        # Coloca perder cambiando cerca del centro superior.
        "Pierde cambiando": (5, 0.6),
        # Coloca perder manteniendo cerca del centro inferior.
        "Pierde manteniendo": (5, -0.6),
        # Coloca ganar cambiando en la salida inferior.
        "Gana cambiando": (5, -2.0),
    }

    # Crea una figura explicita y liviana para evitar consumo alto de memoria en Docker.
    figura, eje = plt.subplots(figsize=(9, 5), facecolor="#f8fafc")
    # Pinta el fondo del eje del mismo color que la figura.
    eje.set_facecolor("#f8fafc")
    # Agrega titulo al diagrama.
    eje.set_title(
        # Texto del titulo.
        "Diagrama de transiciones - Problema 0",
        # Tamano de letra del titulo.
        fontsize=18,
        # Peso visual del titulo.
        fontweight="bold",
        # Separacion del titulo respecto al dibujo.
        pad=18,
        # Color del titulo.
        color="#0f172a",
    )

    # Define un color para cada nodo segun su tipo.
    colores_de_nodos = [
        # Azul para el inicio.
        "#2563eb",
        # Verde para eleccion correcta.
        "#16a34a",
        # Amarillo para eleccion incorrecta.
        "#f59e0b",
        # Verde oscuro para ganar.
        "#15803d",
        # Rojo para perder.
        "#dc2626",
        # Verde oscuro para ganar.
        "#15803d",
        # Rojo para perder.
        "#dc2626",
    ]

    # Dibuja los nodos del grafo.
    nx.draw_networkx_nodes(
        # Grafo que contiene estados y transiciones.
        grafo,
        # Coordenadas manuales de los nodos.
        posiciones,
        # Tamano visual de cada nodo.
        node_size=2300,
        # Colores definidos arriba.
        node_color=colores_de_nodos,
        # Color del borde del nodo.
        edgecolors="#0f172a",
        # Grosor del borde del nodo.
        linewidths=1.4,
    )
    # Dibuja los nombres de los estados encima de los nodos.
    nx.draw_networkx_labels(
        # Grafo que contiene los nodos.
        grafo,
        # Posiciones donde se colocan las etiquetas.
        posiciones,
        # Tamano de letra.
        font_size=9,
        # Peso de letra.
        font_weight="bold",
        # Color de letra.
        font_color="white",
    )
    # Dibuja las flechas entre estados.
    nx.draw_networkx_edges(
        # Grafo que contiene las flechas.
        grafo,
        # Posiciones de origen y destino.
        posiciones,
        # Activa flechas.
        arrows=True,
        # Tamano de las puntas de flecha.
        arrowsize=20,
        # Estilo de flecha.
        arrowstyle="-|>",
        # Grosor de las flechas.
        width=1.9,
        # Color de las flechas.
        edge_color="#334155",
        # Curvatura ligera para evitar superposiciones.
        connectionstyle="arc3,rad=0.08",
        # Margen visual desde el nodo origen.
        min_source_margin=20,
        # Margen visual hacia el nodo destino.
        min_target_margin=20,
    )
    # Extrae las etiquetas de probabilidad de cada flecha.
    etiquetas_de_flechas = nx.get_edge_attributes(grafo, "label")
    # Dibuja las etiquetas de probabilidad sobre las flechas.
    nx.draw_networkx_edge_labels(
        # Grafo que contiene las flechas.
        grafo,
        # Posiciones de los nodos.
        posiciones,
        # Diccionario de etiquetas de probabilidad.
        edge_labels=etiquetas_de_flechas,
        # Tamano de letra de las etiquetas.
        font_size=10,
        # Color del texto de etiqueta.
        font_color="#111827",
        # Caja blanca alrededor de cada etiqueta para legibilidad.
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#cbd5e1"},
    )

    # Agrega una nota explicando los estados absorbentes.
    eje.text(
        # Posicion horizontal de la nota.
        0,
        # Posicion vertical de la nota.
        -2.65,
        # Texto de la nota.
        "Estados finales son absorbentes: ganar o perder termina el proceso.",
        # Tamano de letra.
        fontsize=10,
        # Color del texto.
        color="#334155",
    )
    # Oculta ejes numericos porque el diagrama no los necesita.
    eje.axis("off")
    # Ajusta espacios para que nada se corte.
    figura.tight_layout()
    # Crea la carpeta de salida si no existiera.
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    # Guarda el diagrama en PNG con resolucion suficiente y consumo moderado de memoria.
    figura.savefig(ruta_salida, dpi=95, facecolor=figura.get_facecolor())
    # Cierra la figura para liberar memoria.
    plt.close(figura)
    # Devuelve la ruta del PNG generado.
    return ruta_salida


# Mantiene el nombre anterior como alias compatible.
generate_transition_diagram = generar_diagrama_de_transicion

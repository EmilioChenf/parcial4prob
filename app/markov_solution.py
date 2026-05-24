# Importa dataclass para crear una clase de resultados simple y ordenada.
from dataclasses import dataclass

# Importa Path para recibir rutas donde se guardaran archivos.
from pathlib import Path

# Importa Dict y List para documentar los tipos de datos usados.
from typing import Dict, List

# Importa numpy para construir y validar la matriz de transicion.
import numpy as np

# Importa utilidades propias para formatear probabilidades, guardar texto y crear separadores.
from utils import formatear_probabilidad, guardar_lineas, separador


# Lista los estados de la cadena de Markov en el orden que tendran en la matriz.
ESTADOS = [
    # Estado inicial antes de saber si la primera puerta tiene premio.
    "Inicio",
    # Estado que representa que la primera eleccion fue la puerta premiada.
    "Eleccion correcta",
    # Estado que representa que la primera eleccion fue una puerta vacia.
    "Eleccion incorrecta",
    # Estado final cuando el jugador gana por mantener su puerta inicial.
    "Gana manteniendo",
    # Estado final cuando el jugador pierde por mantener su puerta inicial.
    "Pierde manteniendo",
    # Estado final cuando el jugador gana por cambiar de puerta.
    "Gana cambiando",
    # Estado final cuando el jugador pierde por cambiar de puerta.
    "Pierde cambiando",
]

# Mantiene el nombre anterior como alias para que otros archivos puedan importar STATES.
STATES = ESTADOS


# Convierte la clase en dataclass inmutable para guardar el resultado de Markov.
@dataclass(frozen=True)
class ResultadoMarkov:
    # Guarda la lista de estados de la cadena.
    estados: List[str]
    # Guarda la matriz de probabilidades de transicion.
    matriz_de_transicion: np.ndarray
    # Guarda la probabilidad teorica de ganar si no cambia.
    probabilidad_ganar_manteniendo: float
    # Guarda la probabilidad teorica de perder si no cambia.
    probabilidad_perder_manteniendo: float
    # Guarda la probabilidad teorica de ganar si cambia.
    probabilidad_ganar_cambiando: float
    # Guarda la probabilidad teorica de perder si cambia.
    probabilidad_perder_cambiando: float

    # Expone el nombre anterior states para compatibilidad con las plantillas.
    @property
    def states(self) -> List[str]:
        # Devuelve los estados usando el nombre en ingles que ya consumia la interfaz.
        return self.estados

    # Expone el nombre anterior transition_matrix para compatibilidad con otras partes.
    @property
    def transition_matrix(self) -> np.ndarray:
        # Devuelve la matriz usando el nombre tecnico anterior.
        return self.matriz_de_transicion

    # Expone el nombre anterior keep_win para compatibilidad.
    @property
    def keep_win(self) -> float:
        # Devuelve la probabilidad de ganar manteniendo.
        return self.probabilidad_ganar_manteniendo

    # Expone el nombre anterior keep_loss para compatibilidad.
    @property
    def keep_loss(self) -> float:
        # Devuelve la probabilidad de perder manteniendo.
        return self.probabilidad_perder_manteniendo

    # Expone el nombre anterior switch_win para compatibilidad.
    @property
    def switch_win(self) -> float:
        # Devuelve la probabilidad de ganar cambiando.
        return self.probabilidad_ganar_cambiando

    # Expone el nombre anterior switch_loss para compatibilidad.
    @property
    def switch_loss(self) -> float:
        # Devuelve la probabilidad de perder cambiando.
        return self.probabilidad_perder_cambiando


# Mantiene el nombre anterior como alias de la clase en espanol.
MarkovResult = ResultadoMarkov


# Define la funcion que construye la matriz de transicion de la cadena.
def construir_matriz_de_transicion() -> np.ndarray:
    """Construye una matriz valida donde cada fila suma 1."""
    # Cuenta cuantos estados hay para saber el tamano de la matriz cuadrada.
    cantidad_de_estados = len(ESTADOS)
    # Crea una matriz llena de ceros con dimensiones estados x estados.
    matriz = np.zeros((cantidad_de_estados, cantidad_de_estados), dtype=float)

    # Busca el indice del estado inicial dentro de la lista de estados.
    inicio = ESTADOS.index("Inicio")
    # Busca el indice donde la primera eleccion fue correcta.
    correcta = ESTADOS.index("Eleccion correcta")
    # Busca el indice donde la primera eleccion fue incorrecta.
    incorrecta = ESTADOS.index("Eleccion incorrecta")
    # Busca el indice del estado final ganar manteniendo.
    gana_manteniendo = ESTADOS.index("Gana manteniendo")
    # Busca el indice del estado final perder manteniendo.
    pierde_manteniendo = ESTADOS.index("Pierde manteniendo")
    # Busca el indice del estado final ganar cambiando.
    gana_cambiando = ESTADOS.index("Gana cambiando")
    # Busca el indice del estado final perder cambiando.
    pierde_cambiando = ESTADOS.index("Pierde cambiando")

    # Desde inicio se pasa a eleccion correcta con probabilidad 1/10.
    matriz[inicio, correcta] = 1 / 10
    # Desde inicio se pasa a eleccion incorrecta con probabilidad 9/10.
    matriz[inicio, incorrecta] = 9 / 10

    # Si la eleccion fue correcta, mantener gana dentro de la rama de estrategia.
    matriz[correcta, gana_manteniendo] = 1 / 2
    # Si la eleccion fue correcta, cambiar pierde dentro de la rama de estrategia.
    matriz[correcta, pierde_cambiando] = 1 / 2
    # Si la eleccion fue incorrecta, mantener pierde dentro de la rama de estrategia.
    matriz[incorrecta, pierde_manteniendo] = 1 / 2
    # Si la eleccion fue incorrecta, cambiar gana dentro de la rama de estrategia.
    matriz[incorrecta, gana_cambiando] = 1 / 2

    # Recorre los estados finales para convertirlos en absorbentes.
    for estado_absorbente in [
        # Incluye ganar manteniendo como estado final.
        gana_manteniendo,
        # Incluye perder manteniendo como estado final.
        pierde_manteniendo,
        # Incluye ganar cambiando como estado final.
        gana_cambiando,
        # Incluye perder cambiando como estado final.
        pierde_cambiando,
    ]:
        # Coloca probabilidad 1 de quedarse en el mismo estado final.
        matriz[estado_absorbente, estado_absorbente] = 1

    # Devuelve la matriz completa ya construida.
    return matriz


# Mantiene el nombre anterior como alias compatible.
build_transition_matrix = construir_matriz_de_transicion


# Define la funcion que resuelve el problema con el enfoque de Markov.
def resolver_con_markov() -> ResultadoMarkov:
    # Construye la matriz de transicion y la guarda con un nombre personalizado.
    matriz_chenin = construir_matriz_de_transicion()
    # Suma cada fila para comprobar que todas sumen 1.
    suma_de_filas = matriz_chenin.sum(axis=1)
    # Verifica numericamente que cada fila sea una distribucion de probabilidad valida.
    if not np.allclose(suma_de_filas, 1):
        # Detiene el programa si alguna fila no suma 1.
        raise ValueError(f"La matriz de transicion no es valida: filas {suma_de_filas}")

    # Devuelve todas las probabilidades teoricas importantes del problema.
    return ResultadoMarkov(
        # Guarda el espacio de estados finito.
        estados=ESTADOS,
        # Guarda la matriz construida.
        matriz_de_transicion=matriz_chenin,
        # Mantener gana solo si la primera puerta era correcta: 1/10.
        probabilidad_ganar_manteniendo=1 / 10,
        # Mantener pierde si la primera puerta era incorrecta: 9/10.
        probabilidad_perder_manteniendo=9 / 10,
        # Cambiar gana si la primera puerta era incorrecta: 9/10.
        probabilidad_ganar_cambiando=9 / 10,
        # Cambiar pierde si la primera puerta era correcta: 1/10.
        probabilidad_perder_cambiando=1 / 10,
    )


# Mantiene el nombre anterior como alias compatible.
solve_with_markov = resolver_con_markov


# Define una funcion para convertir la matriz en texto legible para el archivo .txt.
def matriz_como_texto(estados: List[str], matriz: np.ndarray) -> List[str]:
    # Inicia el reporte de matriz con un titulo y una linea en blanco.
    lineas = ["Matriz de transicion P (cada fila suma 1):", ""]
    # Construye el encabezado de columnas S0, S1, S2, etc.
    encabezado = "Estado origen".ljust(24) + " | " + " | ".join(
        # Centra cada etiqueta de estado para que la tabla se vea ordenada.
        f"S{i}".center(7) for i in range(len(estados))
    )
    # Agrega el encabezado al reporte.
    lineas.append(encabezado)
    # Agrega una linea divisoria del mismo largo que el encabezado.
    lineas.append("-" * len(encabezado))
    # Recorre cada estado para escribir una fila de la matriz.
    for i, estado in enumerate(estados):
        # Convierte cada probabilidad de la fila a texto con dos decimales.
        valores = " | ".join(f"{matriz[i, j]:.2f}".center(7) for j in range(len(estados)))
        # Agrega la fila completa con nombre del estado y probabilidades.
        lineas.append(f"S{i} {estado}".ljust(24) + " | " + valores)
    # Agrega una linea en blanco antes de la leyenda de estados.
    lineas.append("")
    # Agrega la leyenda S0, S1, etc. para identificar cada estado.
    lineas.extend(f"S{i}: {estado}" for i, estado in enumerate(estados))
    # Devuelve todas las lineas listas para escribir.
    return lineas


# Mantiene el nombre anterior como alias compatible.
matrix_as_text = matriz_como_texto


# Define una funcion que arma todo el reporte teorico de Markov.
def reporte_markov(resultado: ResultadoMarkov) -> List[str]:
    # Crea las primeras lineas del reporte con explicacion de elementos.
    lineas = [
        # Agrega un titulo visual para la seccion.
        separador("SOLUCION POR CADENAS DE MARKOV"),
        # Presenta los elementos pedidos de la cadena.
        "Elementos de la cadena:",
        # Explica el proceso estudiado.
        "- Proceso: seleccion inicial, apertura de 8 puertas vacias y decision final.",
        # Explica el espacio de estados finito.
        "- Espacio de estados finito: Inicio, eleccion correcta/incorrecta y estados absorbentes de ganar/perder.",
        # Explica las probabilidades principales.
        "- Probabilidades de transicion: P(correcta)=1/10 y P(incorrecta)=9/10.",
        # Explica que los resultados son estados absorbentes.
        "- Estados absorbentes: una vez que gana o pierde, el proceso termina.",
        # Agrega una linea en blanco para separar.
        "",
        # Titulo para interpretar los estados.
        "Interpretacion de estados:",
        # Describe el estado inicial.
        "- Inicio: antes de revisar si la primera puerta tiene premio.",
        # Describe la eleccion correcta.
        "- Eleccion correcta: la primera puerta elegida si tiene premio.",
        # Describe la eleccion incorrecta.
        "- Eleccion incorrecta: la primera puerta elegida no tiene premio.",
        # Describe los resultados al mantener.
        "- Gana/Pierde manteniendo: resultado si nunca cambia.",
        # Describe los resultados al cambiar.
        "- Gana/Pierde cambiando: resultado si siempre cambia.",
        # Agrega otra linea en blanco.
        "",
    ]
    # Agrega la matriz de transicion en formato de texto.
    lineas.extend(matriz_como_texto(resultado.estados, resultado.matriz_de_transicion))
    # Agrega las probabilidades teoricas finales por estrategia.
    lineas.extend(
        [
            # Linea en blanco antes de las probabilidades.
            "",
            # Titulo para las probabilidades teoricas.
            "Probabilidades teoricas por estrategia:",
            # Probabilidad de ganar al no cambiar.
            f"- Si NO cambia, P(ganar) = {formatear_probabilidad(resultado.probabilidad_ganar_manteniendo)}",
            # Probabilidad de perder al no cambiar.
            f"- Si NO cambia, P(perder) = {formatear_probabilidad(resultado.probabilidad_perder_manteniendo)}",
            # Probabilidad de ganar al cambiar.
            f"- Si SI cambia, P(ganar) = {formatear_probabilidad(resultado.probabilidad_ganar_cambiando)}",
            # Probabilidad de perder al cambiar.
            f"- Si SI cambia, P(perder) = {formatear_probabilidad(resultado.probabilidad_perder_cambiando)}",
            # Linea en blanco antes de la justificacion.
            "",
            # Titulo de justificacion.
            "Justificacion:",
            # Explica por que mantener gana con 1/10.
            "Mantener gana solo cuando la primera eleccion fue correcta: 1 de 10 puertas.",
            # Explica por que cambiar gana con 9/10.
            "Cambiar gana cuando la primera eleccion fue incorrecta: 9 de 10 puertas.",
        ]
    )
    # Devuelve el reporte completo.
    return lineas


# Mantiene el nombre anterior como alias compatible.
markov_report = reporte_markov


# Define una funcion que resuelve Markov y escribe el archivo de resultados.
def escribir_resultados_markov(ruta: Path) -> ResultadoMarkov:
    # Calcula el resultado teorico con la matriz de Markov.
    resultado = resolver_con_markov()
    # Guarda el reporte en el archivo indicado.
    guardar_lineas(ruta, reporte_markov(resultado))
    # Devuelve el resultado para usarlo en consola o web.
    return resultado


# Mantiene el nombre anterior como alias compatible.
write_markov_results = escribir_resultados_markov


# Define una funcion que prepara las probabilidades para mostrarlas en tablas.
def diccionario_de_probabilidades_markov(resultado: ResultadoMarkov) -> Dict[str, float]:
    # Devuelve un diccionario con nombres claros para cada probabilidad.
    return {
        # Probabilidad teorica de ganar si mantiene.
        "Ganar manteniendo": resultado.probabilidad_ganar_manteniendo,
        # Probabilidad teorica de perder si mantiene.
        "Perder manteniendo": resultado.probabilidad_perder_manteniendo,
        # Probabilidad teorica de ganar si cambia.
        "Ganar cambiando": resultado.probabilidad_ganar_cambiando,
        # Probabilidad teorica de perder si cambia.
        "Perder cambiando": resultado.probabilidad_perder_cambiando,
    }


# Mantiene el nombre anterior como alias compatible.
markov_probabilities_dict = diccionario_de_probabilidades_markov

# Importa dataclass para crear una clase de datos limpia para la simulacion.
from dataclasses import dataclass

# Importa Path para recibir la ruta donde se guardara el reporte.
from pathlib import Path

# Importa Random para crear numeros aleatorios con semilla reproducible.
from random import Random

# Importa List para indicar que el reporte sera una lista de textos.
from typing import List

# Importa utilidades del proyecto para formatear probabilidades, guardar lineas y crear separadores.
from utils import formatear_probabilidad, guardar_lineas, separador


# Convierte la clase en dataclass inmutable para guardar resultados de simulacion.
@dataclass(frozen=True)
class ResultadoSimulacion:
    # Guarda cuantas repeticiones se hicieron en total.
    repeticiones: int
    # Guarda la semilla usada para que el experimento sea reproducible.
    semilla: int
    # Guarda cuantas veces gano el jugador manteniendo su puerta.
    victorias_manteniendo: int
    # Guarda cuantas veces perdio el jugador manteniendo su puerta.
    derrotas_manteniendo: int
    # Guarda cuantas veces gano el jugador cambiando de puerta.
    victorias_cambiando: int
    # Guarda cuantas veces perdio el jugador cambiando de puerta.
    derrotas_cambiando: int
    # Guarda la probabilidad experimental de ganar manteniendo.
    probabilidad_ganar_manteniendo: float
    # Guarda la probabilidad experimental de perder manteniendo.
    probabilidad_perder_manteniendo: float
    # Guarda la probabilidad experimental de ganar cambiando.
    probabilidad_ganar_cambiando: float
    # Guarda la probabilidad experimental de perder cambiando.
    probabilidad_perder_cambiando: float

    # Expone el nombre anterior repetitions para compatibilidad con la web.
    @property
    def repetitions(self) -> int:
        # Devuelve el total de repeticiones.
        return self.repeticiones

    # Expone el nombre anterior seed para compatibilidad.
    @property
    def seed(self) -> int:
        # Devuelve la semilla usada.
        return self.semilla

    # Expone el nombre anterior keep_wins para compatibilidad.
    @property
    def keep_wins(self) -> int:
        # Devuelve las victorias manteniendo.
        return self.victorias_manteniendo

    # Expone el nombre anterior keep_losses para compatibilidad.
    @property
    def keep_losses(self) -> int:
        # Devuelve las derrotas manteniendo.
        return self.derrotas_manteniendo

    # Expone el nombre anterior switch_wins para compatibilidad.
    @property
    def switch_wins(self) -> int:
        # Devuelve las victorias cambiando.
        return self.victorias_cambiando

    # Expone el nombre anterior switch_losses para compatibilidad.
    @property
    def switch_losses(self) -> int:
        # Devuelve las derrotas cambiando.
        return self.derrotas_cambiando

    # Expone el nombre anterior keep_win_probability para compatibilidad.
    @property
    def keep_win_probability(self) -> float:
        # Devuelve la probabilidad experimental de ganar manteniendo.
        return self.probabilidad_ganar_manteniendo

    # Expone el nombre anterior keep_loss_probability para compatibilidad.
    @property
    def keep_loss_probability(self) -> float:
        # Devuelve la probabilidad experimental de perder manteniendo.
        return self.probabilidad_perder_manteniendo

    # Expone el nombre anterior switch_win_probability para compatibilidad.
    @property
    def switch_win_probability(self) -> float:
        # Devuelve la probabilidad experimental de ganar cambiando.
        return self.probabilidad_ganar_cambiando

    # Expone el nombre anterior switch_loss_probability para compatibilidad.
    @property
    def switch_loss_probability(self) -> float:
        # Devuelve la probabilidad experimental de perder cambiando.
        return self.probabilidad_perder_cambiando


# Mantiene el nombre anterior como alias compatible.
SimulationResult = ResultadoSimulacion


# Define la simulacion de la Ley de los Grandes Numeros.
def simular_ley_grandes_numeros(repeticiones: int = 1_000_000, semilla: int = 20260524) -> ResultadoSimulacion:
    # Valida que se cumpla el minimo pedido por el examen.
    if repeticiones < 1_000_000:
        # Detiene el programa si se intenta simular con menos de un millon.
        raise ValueError("La simulacion debe usar al menos 1,000,000 repeticiones.")

    # Crea un generador aleatorio reproducible con la semilla indicada.
    aleatorio_chencito = Random(semilla)
    # Representa las 10 puertas con numeros del 0 al 9.
    puertas = range(10)
    # Inicia el contador de victorias al mantener en cero.
    victorias_manteniendo = 0
    # Inicia el contador de victorias al cambiar en cero.
    victorias_cambiando = 0

    # Repite el experimento la cantidad de veces solicitada.
    for _ in range(repeticiones):
        # Elige al azar cual puerta tiene el premio.
        puerta_premiada = aleatorio_chencito.randrange(10)
        # Elige al azar la primera puerta seleccionada por Chispudito.
        primera_eleccion = aleatorio_chencito.choice(puertas)

        # Determina si mantener gana comparando la primera eleccion con la puerta premiada.
        gano_manteniendo = primera_eleccion == puerta_premiada
        # Si mantener gano, suma una victoria a mantener.
        if gano_manteniendo:
            # Incrementa el contador de victorias manteniendo.
            victorias_manteniendo += 1
        # Si mantener no gano, entonces cambiar gana en este problema.
        else:
            # Incrementa el contador de victorias cambiando.
            victorias_cambiando += 1

    # Calcula las derrotas manteniendo restando sus victorias al total.
    derrotas_manteniendo = repeticiones - victorias_manteniendo
    # Calcula las derrotas cambiando restando sus victorias al total.
    derrotas_cambiando = repeticiones - victorias_cambiando

    # Devuelve todos los conteos y probabilidades experimentales.
    return ResultadoSimulacion(
        # Guarda el total de repeticiones.
        repeticiones=repeticiones,
        # Guarda la semilla usada.
        semilla=semilla,
        # Guarda victorias al mantener.
        victorias_manteniendo=victorias_manteniendo,
        # Guarda derrotas al mantener.
        derrotas_manteniendo=derrotas_manteniendo,
        # Guarda victorias al cambiar.
        victorias_cambiando=victorias_cambiando,
        # Guarda derrotas al cambiar.
        derrotas_cambiando=derrotas_cambiando,
        # Calcula frecuencia relativa de ganar manteniendo.
        probabilidad_ganar_manteniendo=victorias_manteniendo / repeticiones,
        # Calcula frecuencia relativa de perder manteniendo.
        probabilidad_perder_manteniendo=derrotas_manteniendo / repeticiones,
        # Calcula frecuencia relativa de ganar cambiando.
        probabilidad_ganar_cambiando=victorias_cambiando / repeticiones,
        # Calcula frecuencia relativa de perder cambiando.
        probabilidad_perder_cambiando=derrotas_cambiando / repeticiones,
    )


# Mantiene el nombre anterior como alias compatible.
simulate_large_numbers = simular_ley_grandes_numeros


# Define una funcion que arma el reporte textual de la simulacion.
def reporte_ley_grandes_numeros(resultado: ResultadoSimulacion) -> List[str]:
    # Define la probabilidad teorica de ganar manteniendo.
    teorica_ganar_manteniendo = 1 / 10
    # Define la probabilidad teorica de perder manteniendo.
    teorica_perder_manteniendo = 9 / 10
    # Define la probabilidad teorica de ganar cambiando.
    teorica_ganar_cambiando = 9 / 10
    # Define la probabilidad teorica de perder cambiando.
    teorica_perder_cambiando = 1 / 10

    # Devuelve una lista de lineas listas para guardar en el archivo.
    return [
        # Agrega el titulo del metodo.
        separador("SOLUCION POR LEY DE LOS GRANDES NUMEROS"),
        # Presenta los elementos de la simulacion.
        "Elementos del metodo:",
        # Indica cuantas repeticiones independientes se hicieron.
        f"- Repeticiones independientes: {resultado.repeticiones:,}",
        # Indica la semilla reproducible.
        f"- Semilla reproducible: {resultado.semilla}",
        # Explica que se elige puerta ganadora y puerta inicial en cada repeticion.
        "- En cada repeticion se elige una puerta ganadora y una puerta inicial al azar.",
        # Explica que el promedio experimental se compara contra la teoria.
        "- El promedio experimental se compara contra la probabilidad teorica.",
        # Agrega linea en blanco.
        "",
        # Titulo de resultados.
        "Resultados experimentales:",
        # Muestra victorias manteniendo.
        f"- Victorias manteniendo: {resultado.victorias_manteniendo:,}",
        # Muestra derrotas manteniendo.
        f"- Derrotas manteniendo: {resultado.derrotas_manteniendo:,}",
        # Muestra probabilidad experimental de ganar manteniendo.
        f"- Probabilidad experimental de ganar manteniendo: {formatear_probabilidad(resultado.probabilidad_ganar_manteniendo)}",
        # Muestra probabilidad experimental de perder manteniendo.
        f"- Probabilidad experimental de perder manteniendo: {formatear_probabilidad(resultado.probabilidad_perder_manteniendo)}",
        # Muestra victorias cambiando.
        f"- Victorias cambiando: {resultado.victorias_cambiando:,}",
        # Muestra derrotas cambiando.
        f"- Derrotas cambiando: {resultado.derrotas_cambiando:,}",
        # Muestra probabilidad experimental de ganar cambiando.
        f"- Probabilidad experimental de ganar cambiando: {formatear_probabilidad(resultado.probabilidad_ganar_cambiando)}",
        # Muestra probabilidad experimental de perder cambiando.
        f"- Probabilidad experimental de perder cambiando: {formatear_probabilidad(resultado.probabilidad_perder_cambiando)}",
        # Agrega linea en blanco.
        "",
        # Titulo de comparacion.
        "Comparacion contra valores teoricos:",
        # Compara ganar manteniendo.
        f"- Ganar manteniendo: experimental {resultado.probabilidad_ganar_manteniendo:.6f} vs teorico {teorica_ganar_manteniendo:.6f}",
        # Compara perder manteniendo.
        f"- Perder manteniendo: experimental {resultado.probabilidad_perder_manteniendo:.6f} vs teorico {teorica_perder_manteniendo:.6f}",
        # Compara ganar cambiando.
        f"- Ganar cambiando: experimental {resultado.probabilidad_ganar_cambiando:.6f} vs teorico {teorica_ganar_cambiando:.6f}",
        # Compara perder cambiando.
        f"- Perder cambiando: experimental {resultado.probabilidad_perder_cambiando:.6f} vs teorico {teorica_perder_cambiando:.6f}",
        # Agrega linea en blanco.
        "",
        # Titulo de justificacion.
        "Justificacion:",
        # Explica la convergencia experimental.
        "Al aumentar el numero de repeticiones, las frecuencias relativas se acercan a las probabilidades teoricas.",
    ]


# Mantiene el nombre anterior como alias compatible.
large_numbers_report = reporte_ley_grandes_numeros


# Define una funcion que ejecuta la simulacion y escribe el archivo de resultados.
def escribir_resultados_ley_grandes_numeros(ruta: Path, repeticiones: int = 1_000_000) -> ResultadoSimulacion:
    # Ejecuta la simulacion con la cantidad indicada de repeticiones.
    resultado = simular_ley_grandes_numeros(repeticiones=repeticiones)
    # Guarda el reporte textual en la ruta indicada.
    guardar_lineas(ruta, reporte_ley_grandes_numeros(resultado))
    # Devuelve el resultado para usarlo en consola o web.
    return resultado


# Mantiene el nombre anterior como alias compatible.
write_large_numbers_results = escribir_resultados_ley_grandes_numeros

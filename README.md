# Problema 0: Chispudito y las 10 puertas

Proyecto completo en Python 3 para resolver el problema del examen usando dos enfoques:

- Cadenas de Markov.
- Ley de los Grandes Numeros.

El programa genera automaticamente:

- `outputs/markov_results.txt`
- `outputs/large_numbers_results.txt`
- `outputs/transition_diagram.png`

Tambien levanta una interfaz web en:

```text
http://localhost:8000
```

## Planteamiento del problema

Chispudito debe seleccionar una de 10 puertas. Una puerta tiene premio y las otras 9 estan vacias. Despues de la primera eleccion, el presentador, que sabe donde esta el premio, abre 8 puertas vacias de las otras 9. Luego quedan cerradas dos puertas: la puerta inicial del concursante y otra puerta. El concursante puede mantener su eleccion inicial o cambiar.

Se pide calcular la probabilidad de ganar y perder si nunca cambia, y tambien si siempre cambia.

## Solucion teorica

La probabilidad de que la primera puerta elegida tenga el premio es:

```text
P(eleccion inicial correcta) = 1/10 = 0.10
```

La probabilidad de que la primera puerta elegida no tenga el premio es:

```text
P(eleccion inicial incorrecta) = 9/10 = 0.90
```

Por lo tanto:

```text
Si NO cambia:
P(ganar) = 1/10 = 0.10
P(perder) = 9/10 = 0.90

Si SI cambia:
P(ganar) = 9/10 = 0.90
P(perder) = 1/10 = 0.10
```

La razon es que cambiar convierte todos los casos donde la primera eleccion fue incorrecta en victoria, porque el presentador elimina 8 puertas vacias y deja cerrada la unica alternativa posible.

## Solucion usando cadenas de Markov

### Elementos de la cadena

- Proceso de Markov: el estado actual contiene la informacion necesaria para determinar el siguiente paso del juego.
- Espacio de estados finito:
  - `Inicio`
  - `Eleccion correcta`
  - `Eleccion incorrecta`
  - `Gana manteniendo`
  - `Pierde manteniendo`
  - `Gana cambiando`
  - `Pierde cambiando`
- Probabilidades de transicion principales:
  - Desde `Inicio` hacia `Eleccion correcta`: `1/10`.
  - Desde `Inicio` hacia `Eleccion incorrecta`: `9/10`.
- Estados absorbentes: los estados finales de ganar o perder se quedan en si mismos porque el juego ya termino.

La matriz de transicion se construye en `app/markov_solution.py`. Cada fila suma 1, por lo que es una matriz valida. La cadena combinada reparte desde los estados de eleccion correcta/incorrecta hacia las dos estrategias posibles con probabilidad `1/2`; las probabilidades finales de cada estrategia se calculan condicionalmente:

- Mantener gana si la primera eleccion fue correcta.
- Cambiar gana si la primera eleccion fue incorrecta.

El diagrama de transiciones se genera en:

```text
outputs/transition_diagram.png
```

## Solucion usando Ley de los Grandes Numeros

La simulacion se encuentra en `app/large_numbers_solution.py` y ejecuta al menos `1,000,000` repeticiones.

En cada repeticion:

1. Se selecciona aleatoriamente la puerta ganadora.
2. Se selecciona aleatoriamente la primera puerta de Chispudito.
3. Se calcula si gana manteniendo.
4. Se calcula si gana cambiando.

Al final se muestran:

- Victorias manteniendo.
- Derrotas manteniendo.
- Probabilidad experimental de ganar manteniendo.
- Probabilidad experimental de perder manteniendo.
- Victorias cambiando.
- Derrotas cambiando.
- Probabilidad experimental de ganar cambiando.
- Probabilidad experimental de perder cambiando.
- Comparacion contra los valores teoricos.

Por la Ley de los Grandes Numeros, al usar muchas repeticiones el promedio experimental converge hacia la probabilidad teorica.

## Estructura del proyecto

```text
.
├── app/
│   ├── main.py
│   ├── markov_solution.py
│   ├── large_numbers_solution.py
│   ├── diagrams.py
│   ├── utils.py
│   ├── web.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── styles.css
├── outputs/
│   ├── markov_results.txt
│   ├── large_numbers_results.txt
│   └── transition_diagram.png
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Ejecutar con Docker

Desde la carpeta del proyecto:

```bash
docker compose up --build
```

Docker instalara las dependencias, ejecutara la interfaz web y dejara los resultados en la carpeta `outputs/`.

Despues abre el navegador en:

```text
http://localhost:8000
```

La pagina muestra:

- Resumen teorico y experimental.
- Resultados de la cadena de Markov.
- Resultados de la simulacion por Ley de los Grandes Numeros.
- Diagrama de transiciones.
- Enlaces directos a los archivos generados.

Para detener el servidor usa `Ctrl + C` en la terminal.

## Ejecutar solo en consola con Docker

Si quieres usar el modo anterior de consola:

```bash
docker compose run --rm chispudito python app/main.py
```

## Ejecutar sin Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app/web.py
```

En Linux o macOS, la activacion del entorno virtual seria:

```bash
source .venv/bin/activate
```

Luego abre:

```text
http://localhost:8000
```

Para ejecutar solo la version de consola sin Docker:

```bash
python app/main.py
```

## Ejemplo de salida en consola

```text
Problema 0 - Chispudito y las 10 puertas
Cadenas de Markov + Ley de los Grandes Numeros

1. Calculando solucion teorica con cadena de Markov...
2. Generando diagrama de transiciones...
3. Ejecutando simulacion con 1,000,000 repeticiones...

Resumen del Problema 0
┏━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Estrategia  ┃ Evento ┃ Teorico           ┃ Experimental      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ No cambiar  │ Ganar  │ 0.100000 (10.00%) │ cercano a 10%     │
│ No cambiar  │ Perder │ 0.900000 (90.00%) │ cercano a 90%     │
│ Cambiar     │ Ganar  │ 0.900000 (90.00%) │ cercano a 90%     │
│ Cambiar     │ Perder │ 0.100000 (10.00%) │ cercano a 10%     │
└─────────────┴────────┴───────────────────┴───────────────────┘
```

## Archivos generados

### `outputs/markov_results.txt`

Contiene los elementos de la cadena, la matriz de transicion, la explicacion de estados y las probabilidades teoricas.

### `outputs/large_numbers_results.txt`

Contiene los resultados de la simulacion con 1,000,000 repeticiones y la comparacion experimental contra los valores teoricos.

### `outputs/transition_diagram.png`

Contiene el diagrama de transiciones con nodos, flechas y etiquetas de probabilidad.

## Conclusion

Conviene cambiar de puerta. Si Chispudito mantiene su primera eleccion, gana con probabilidad `10%`. Si cambia, gana con probabilidad `90%`. El enfoque de cadenas de Markov explica la estructura del proceso y la simulacion por Ley de los Grandes Numeros confirma experimentalmente esos valores.

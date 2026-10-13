# Glosario — PoC extracción de jugadas desde video

## Propósito

Compartir un vocabulario entre el responsable de producto y la IA que
investiga, implementa y ejecuta los experimentos.

Este documento define conceptos. No establece todavía el esquema JSON
ni las tecnologías que se utilizarán.

---

## 1. Video y cancha

| Término | Definición |
|---|---|
| Clip | Fragmento de 10–20 segundos que se utiliza como entrada de la PoC. |
| Cámara fija | Cámara cuyo encuadre permanece estable durante el clip. Un movimiento, zoom o corte puede invalidar la calibración. |
| Frame | Imagen del video correspondiente a un instante. No es lo mismo que un keyframe del visor. |
| Tiempo del clip | Tiempo transcurrido desde el inicio del fragmento, expresado en segundos. |
| Coordenadas de imagen | Ubicación dentro de un frame, expresada en píxeles. |
| Coordenadas de cancha | Ubicación sobre el terreno, expresada en metros según una convención acordada. |
| Dimensiones de cancha | Largo y ancho de la cancha del video. No se asume que coincidan con las dimensiones del mock del visor. |
| Calibración | Relación establecida manualmente entre referencias de la imagen y ubicaciones conocidas de la cancha. |
| Punto de referencia | Punto identificable en la imagen cuya ubicación sobre la cancha conocemos o podemos estimar. |
| Proyección al terreno | Conversión de una ubicación de imagen a coordenadas de cancha, suponiendo que corresponde al plano del suelo. |
| Posición sobre el terreno | Estimación de dónde está apoyada una jugadora sobre la cancha. No representa la posición 3D completa de su cuerpo. |

### Convención de coordenadas

El ejemplo del visor utiliza:
- Metros como unidad.
- Origen en el centro de la cancha.
- `x` a lo largo.
- `z` a lo ancho.
- `y` hacia arriba.

Esta es la convención de referencia inicial. Debe verificarse contra el
contrato real del front antes de integrar la exportación.

La orientación y el sentido de los ejes deben quedar documentados para
evitar jugadas reflejadas o rotadas.

---

## 2. Detección, seguimiento e identidad

| Término | Definición |
|---|---|
| Detección | Localización automática de una posible jugadora en un frame. No determina por sí sola quién es. |
| Caja de detección | Rectángulo de imagen que delimita una detección. |
| Seguimiento / tracking | Asociación de detecciones entre frames para construir una trayectoria. |
| Track | Secuencia de detecciones que el sistema considera pertenecientes a la misma entidad. |
| ID de track | Identificador técnico de una trayectoria. No equivale necesariamente a una identidad de jugadora. |
| Identidad de jugadora | Identificador estable de la persona representada en la jugada. Se asigna manualmente en esta PoC. |
| Equipo | Pertenencia de una jugadora a uno de los equipos. Se asigna manualmente. |
| Número | Etiqueta visual o dorsal de la jugadora. No debe confundirse con el ID de track ni usarse como identidad global. |
| Asignación manual | Asociación realizada por una persona entre tracks, identidades y equipos. |
| Cambio de identidad | Error por el que un track pasa a seguir a otra jugadora. |
| Fragmentación | Situación en la que una misma jugadora termina representada por varios tracks separados. |
| Oclusión | Ocultamiento parcial o total de una jugadora por otra persona u objeto. |
| Fuera de encuadre | Situación en la que una jugadora no aparece en la imagen. La PoC no reconstruye automáticamente su ubicación. |

Una jugadora puede tener varios tracks durante el clip.

Que el sistema mantenga un mismo ID de track no demuestra que haya seguido
correctamente a la misma persona.

---

## 3. Movimiento y origen de los datos

| Término | Definición |
|---|---|
| Muestra de posición | Posición de una entidad asociada a un tiempo y a un origen del dato. |
| Trayectoria | Secuencia temporal de posiciones de una entidad. Puede contener intervalos sin datos. |
| Posición obtenida del video | Estimación calculada a partir de una detección en la imagen y su proyección al terreno. No es una medición exacta. |
| Posición interpolada | Posición calculada entre muestras disponibles. No constituye una observación del video. |
| Posición cargada manualmente | Posición introducida por una persona; por ejemplo, la de la pelota. |
| Posición faltante | Ausencia de una estimación utilizable en un instante o intervalo. No equivale a posición cero ni a permanecer quieta. |
| Corrección manual | Intervención para reparar identidades, asociaciones o posiciones. No implica construir una interfaz de edición completa. |
| Referencia manual de evaluación | Anotación humana usada para comparar resultados. También puede contener incertidumbre. |
| Confianza del detector | Puntaje del modelo sobre una detección. No demuestra precisión espacial, identidad correcta ni utilidad táctica. |

### Regla de trazabilidad

Los datos obtenidos del video, interpolados, cargados manualmente y
faltantes deben poder distinguirse.

El formato concreto para representarlos se decidirá al revisar el contrato
del front. No se completarán posiciones para aparentar una reconstrucción
más completa.

---

## 4. Integración con el visor

| Término | Definición |
|---|---|
| Jugada | Dataset temporal que el visor utiliza para reproducir una secuencia. |
| Keyframe del visor | Estado de posiciones en un instante según el modelo del front. No tiene que corresponder a cada frame del video. |
| Contrato de intercambio | Acuerdo sobre estructura, unidades, tiempos, identidades y representación de ausencias en los datos exportados. |
| Exportación | Generación de un archivo JSON para consumir los resultados fuera del proceso de extracción. |
| Compatibilidad con el front | Capacidad del visor para interpretar los datos sin perder su significado ni inventar información. |
| Video de diagnóstico | Video con detecciones y IDs superpuestos para revisar errores del procesamiento. |
| Vista superior de diagnóstico | Representación 2D de las posiciones sobre la cancha para revisar la proyección y las trayectorias. |

### Dependencia conocida

El ejemplo del visor utiliza keyframes completos.

La extracción puede producir posiciones faltantes y cantidades variables
de jugadoras visibles. Esta diferencia debe resolverse explícitamente
antes de integrar ambos proyectos.

La pelota puede cargarse manualmente. Si no se carga, su ausencia debe
representarse de manera acordada; no se asumirá una posición ficticia.

---

## 5. Experimentación y validación

| Término | Definición |
|---|---|
| Hipótesis | Supuesto que todavía requiere evidencia; por ejemplo, que el tracking conserve identidades en este clip. |
| Experimento | Trabajo mínimo para responder una pregunta de viabilidad. |
| Evidencia | Artefactos y resultados que permiten revisar qué ocurrió al ejecutar un experimento. |
| Pause Point | Punto obligatorio de entrega y detención antes de continuar con otra etapa. |
| Implementado | El código o mecanismo necesario está construido. |
| Ejecutado | El mecanismo se corrió con entradas identificadas y produjo resultados o un fallo registrado. |
| Revisado | La evidencia fue examinada por el responsable de producto. |
| Validado | La evidencia sostiene una conclusión dentro de las condiciones probadas. No garantiza que funcione con cualquier video. |
| Aprobado para continuar | Decisión explícita de avanzar después de revisar los resultados. |
| Fidelidad táctica | Grado en que la reconstrucción conserva posiciones, espacios y movimientos relevantes para el análisis. |
| Esfuerzo manual | Trabajo humano necesario para preparar, asignar identidades y corregir resultados. Debe registrarse por actividad. |

Un experimento puede estar completo y concluir que un enfoque no sirve.

Las pruebas de software verifican comportamientos de la implementación.
La validación experimental verifica qué resultados consigue con el video.
Ninguna reemplaza a la otra.
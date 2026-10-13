# Plan experimental — PoC extracción de jugadas desde video

## Estado

Plan experimental vigente, sujeto a revisión por etapa.

E0 en preparación documental.
Narrativa y review disponibles.
Stack y arquitectura propuestos; entorno pendiente de comprobación.
Casos de uso, protocolo de evaluación y checklist pendientes.

No hay una ejecución completa documentada de E0.
Ninguna etapa aprobada para continuar.

---

## 1. Objetivo

Determinar si podemos reconstruir los movimientos visibles de una jugada
de fútbol 8 con suficiente fidelidad para el análisis táctico, y cuánto
trabajo manual requiere obtener un resultado útil.

No buscamos demostrar solamente que el proceso genera un JSON o que el
visor puede reproducirlo.

---

## 2. Alcance

### Incluido

- Un clip de 10–20 segundos.
- Una cámara fija.
- Ejecución local.
- Calibración manual.
- Detección y seguimiento de jugadoras visibles.
- Asignación manual de equipos e identidades.
- Estimación de posiciones sobre el terreno.
- Exportación JSON para el visor.
- Video de diagnóstico.
- Pelota cargada manualmente, si se necesita para la evaluación.
- Distinción entre datos del video, interpolados, manuales y faltantes.

### Excluido

- API web, autenticación, base de datos y despliegue.
- Reconstrucción corporal o de mirada.
- Reconstrucción automática de jugadoras fuera del encuadre.
- Tracking automático de pelota.
- Múltiples cámaras.
- Interfaz completa de correcciones.
- Generalización demostrada a cualquier video.

---

## 3. Acuerdo de trabajo

### Responsabilidad del usuario

Definir y evaluar:
- Alcance.
- Utilidad del resultado.
- Errores que afectan la interpretación táctica.
- Esfuerzo manual aceptable.
- Aprobación de cada Pause Point.

No necesita elegir algoritmos ni aprobar cada detalle técnico.

### Responsabilidad de la IA

- Investigar lo necesario para la etapa próxima.
- Recomendar decisiones técnicas y explicar sus limitaciones.
- Separar decisiones, hipótesis y bloqueos.
- Implementar dentro del alcance aprobado.
- Ejecutar tests y experimentos cuando el entorno lo permita.
- Entregar evidencia y registrar fallos.
- Detenerse en cada Pause Point.

No debe presentar una recomendación como resultado comprobado ni marcar
una ejecución pendiente como validada.

### Investigación técnica

Antes de elegir herramientas, verificar:
- Requisitos de ejecución.
- Licencias aplicables al código y a los modelos utilizados.
- Disponibilidad de los recursos necesarios.
- Limitaciones relevantes para este experimento.

La investigación no reemplaza la prueba con el clip.

---

## 4. Funcionamiento de los Pause Points

Cada etapa termina con una entrega y una detención obligatoria.

El usuario puede decidir:
- Continuar.
- Ajustar y repetir.
- Detener o descartar el enfoque.

La decisión se registra en este documento.

Una checklist completa no autoriza automáticamente la etapa siguiente.
El silencio tampoco constituye aprobación.

### Registro mínimo de cada ejecución

- Entrada utilizada y versión o identificación del clip.
- Configuración relevante y versión del código.
- Pasos o comando para repetir la ejecución.
- Artefactos producidos.
- Problemas encontrados.
- Trabajo manual realizado y tiempo aproximado.
- Conclusiones y aspectos todavía no comprobados.

---

## 5. Etapas

## E0 — Preparar el caso de prueba

### Pregunta

¿Tenemos un clip y referencias suficientes para realizar una primera
evaluación útil?

### Caso seleccionado

- Archivo original: MP4 de 12 segundos.
- Intervalo de interés: 0–8 segundos.
- Cámara fija, según información del usuario.
- Dimensiones informadas: 50 m de largo × 35 m de ancho.
- Según confirmación del usuario, el MP4, cuatro capturas de
  acontecimientos y una captura anotada están en data/local/.
- Nombres de archivo e identificación pendientes de comprobación.
- Tiempos exactos de las capturas pendientes de registrar.

### Identificación confirmada por el usuario

- Equipo propio: camisetas oscuras.
- Equipo rival: camisetas claras.
- Persona de camiseta amarilla: árbitro; excluir de las entidades
  exportadas como jugadoras.
- Arco propio: cercano, abajo a la derecha en la captura de referencia.
- Arco rival: al fondo, arriba a la izquierda.
- Cancha objetivo: límites señalados en rojo en la captura anotada.
- Dimensiones informadas: 50 m de largo × 35 m de ancho.
- Las personas de la cancha contigua no pertenecen a la jugada.

La captura anotada identifica el terreno y los arcos.
Sus trazos no constituyen una calibración precisa.

Los puntos de calibración se seleccionarán sobre frames del archivo
original, utilizando referencias del plano del suelo.

### Contrato actual del visor revisado

Fuentes:
- `scene-types.ts`
- `play-mock.ts`

Compatibilidades:
- Identidades separadas de las posiciones.
- Equipos `own` y `rival`.
- Tiempo en segundos desde el inicio.
- Coordenadas en metros, con origen en el centro.
- Ejes: x a lo largo, z a lo ancho, y hacia arriba.

Orientación propuesta para esta extracción:
- Arco propio en x = -25.
- Arco rival en x = +25.
- Debe reflejarse en la calibración.

Diferencias pendientes para E4:
- El visor utiliza dimensiones globales de 50 × 30 m.
- La cancha del video mide 50 × 35 m.
- El contrato documenta keyframes completos.
- No existe representación explícita de posiciones faltantes.
- La pelota es obligatoria en todos los keyframes.
- No se registra el origen de las posiciones.
- El número de jugadora es obligatorio, aunque los dorsales pueden
  no conocerse durante la extracción.

No se inventarán posiciones ni dorsales para satisfacer el contrato.

Antes de integrar:
- Acordar los cambios mínimos del contrato.
- Revisar interpolación y componentes consumidores.
- Incorporar validación de los datos externos.

Estado:
Revisión del contrato completada.
Integración todavía no diseñada ni validada.

### Situación táctica descrita por el usuario

Salida desde un lateral cerca del arco propio.
Pase a una defensora, cuyo siguiente pase es interceptado.
El equipo rival encuentra a una jugadora que llega libre por el medio,
le pasa la pelota y convierte.

### Pregunta de evaluación

¿La reconstrucción permite comprender la pérdida y la llegada libre de
la rival, conservando las relaciones espaciales y temporales relevantes?

### Observaciones preliminares de las capturas

- Encuadre aparentemente consistente.
- Referencias de cancha visibles.
- Varios arcos y marcaciones que requieren identificación.
- Personas en una cancha contigua que deben excluirse.
- Algunas jugadoras pequeñas y desenfoque de movimiento.
- Posibles oclusiones cerca del arco.

### Pendientes

- Inspeccionar el archivo original y sus metadatos.
- Comprobar la estabilidad del encuadre durante el intervalo 0–8 s.
- Registrar tiempos de los acontecimientos.
- Seleccionar referencias precisas para calibración y evaluación.

### Estado

Revisión visual preliminar registrada en el contexto.
01-narrative.md, 02-review.md, 03-use-cases.md y 04-checklist.md
disponibles. 03-use-cases.md y 04-checklist.md aprobados por el
usuario (2026-10-13).

Medios en data/local/ identificados por nombre: gol-del-rival.mp4,
01-inicio.png, 02-pase-malo.png, 03-rival-libre.png, 04-rival-gol.png
y limites.png (captura anotada). Comprobados en la primera ejecución
(2026-10-13): los 6 archivos presentes, hash del MP4 registrado en
artifacts/e0/20261013-155147/registro.json.

Entorno observado el 2026-10-13: uv 0.12.24 y ffmpeg/ffprobe 9.0.2
disponibles vía Homebrew; Python global 3.14.7 sin modificar.

Implementación ejecutada y probada (90 tests, 2026-10-13).
Ejecución con el clip real completada: artifacts/e0/20261013-155147.
Informe entregado: experiments/e0-preparar-caso/05-results.md.
E0 completada y aprobada por el usuario en el Pause Point
(2026-10-13) — ver Decisión registrada de E0.

### Trabajo mínimo

- Seleccionar e identificar el clip.
- Revisar estabilidad del encuadre, visibilidad y oclusiones.
- Documentar dimensiones conocidas o estimadas de la cancha.
- Identificar posibles referencias para calibrar.
- Elegir un fragmento o situación táctica que interese reconstruir.
- Preparar unas pocas anotaciones manuales de referencia.
- Revisar los tipos o un ejemplo real de datos del visor.
- Registrar diferencias entre su contrato y los datos de extracción.

Las anotaciones manuales son aproximadas. No se presentarán como verdad
exacta si no contamos con una medición independiente.

### Evidencia

- Ficha del clip con limitaciones.
- Imágenes de referencia.
- Lista inicial de incertidumbres.
- Resumen del contrato actual del front.

### Revisión humana

- ¿Esta situación sirve para evaluar el objetivo?
- ¿Qué movimientos o espacios es importante conservar?
- ¿Aceptamos las limitaciones del clip o necesitamos otro?

### Pause Point

Detenerse antes de implementar la calibración.

### Decisión registrada

2026-10-13 — El usuario revisó el informe `experiments/e0-preparar-caso/05-results.md` y el checklist, y aceptó los resultados: "observo los resultados y creo que están bien".

Lo aceptado:
- Identificación del caso y utilizabilidad de las referencias (PE-01: favorable con reservas).
- Tabla de acontecimientos con los cuatro momentos en estado **propuesto**: inicio/salida ≈ 0.7 s (confianza baja), intercepción ≈ 3.7 s, pase a la rival libre ≈ 5.3 s, gol ≈ 6.8 s (incertidumbre ±0.35 s por muestreo cada ~0.667 s).
- Limitaciones aceptadas para continuar (05-results.md §6): instantes exactos entre frames, saque poco visible, dorsales ilegibles, estabilidad de encuadre verificada solo en muestreo discreto, calibración sin evaluar (distorsión de lente pendiente), referencia en t=8.0 no extraída.

Consecuencias:
- E0 queda completada y aprobada.
- Los tiempos de la tabla pasan a **confirmados por el usuario** para efectos de planificación; siguen siendo aproximados (±0.35 s) y no constituyen medición independiente.
- Autorizado a preparar E1 (calibración), que requerirá instalación de OpenCV/NumPy con autorización registrada según workflow.
- Pendientes no bloqueantes para E1: extraer referencia explícita en t=8.0 y frames de precisión alrededor de los acontecimientos, si E1/E2 los demandan.

---

## E1 — Validar imagen → cancha

### Pregunta

¿Podemos convertir ubicaciones de la imagen en posiciones de cancha
razonables para este clip?

### Trabajo mínimo

- Implementar una forma mínima de ingresar la calibración.
- Proyectar posiciones seleccionadas manualmente.
- Revisar puntos en distintas zonas visibles de la cancha.
- Incluir, cuando sea posible, referencias adicionales que no se hayan
  utilizado para calibrar.
- Documentar dimensiones, ejes y supuestos.

No implementar todavía el procesamiento automático completo.

### Evidencia

- Imagen con referencias y puntos seleccionados.
- Vista superior con los puntos proyectados.
- Configuración de calibración.
- Ejemplos de desvíos y zonas problemáticas.

### Revisión humana

- ¿Las ubicaciones son coherentes con el video?
- ¿Se conserva la relación espacial entre los puntos?
- ¿Hay errores que harían engañosa una lectura táctica?

### Pause Point

Detenerse antes de integrar detección y seguimiento.

### Decisión registrada

Pendiente.

---

## E2 — Validar detección y seguimiento

### Pregunta

¿Podemos obtener trayectorias identificables de las jugadoras visibles,
y cuáles son los errores que requieren intervención?

### Trabajo mínimo

- Elegir y documentar un enfoque técnico inicial.
- Ejecutar detección y seguimiento sobre el clip.
- Generar un video de diagnóstico con IDs.
- Registrar omisiones, cambios de identidad y fragmentaciones.
- Probar una forma simple de asignar equipos e identidades.
- Registrar el tiempo utilizado para esa asignación.

La identidad de una jugadora no se asumirá correcta solo porque un track
mantenga el mismo ID.

### Evidencia

- Video de diagnóstico.
- Datos de tracks.
- Ejemplos con tiempos concretos de los errores principales.
- Asignaciones manuales.
- Registro del esfuerzo manual y limitaciones.

### Revisión humana

- ¿Qué trayectorias corresponden a las jugadoras correctas?
- ¿Qué cruces u oclusiones producen errores?
- ¿Los resultados son aprovechables sin corregir todo el clip?

### Pause Point

Detenerse antes de combinar y exportar las trayectorias como jugada.

Si el resultado no alcanza, proponer un nuevo intento acotado antes de
sumar complejidad.

### Decisión registrada

Pendiente.

---

## E3 — Validar trayectorias sobre la cancha

### Pregunta

¿La combinación de seguimiento y calibración produce movimientos
coherentes sobre el terreno?

### Trabajo mínimo

- Definir y documentar cómo se estima el punto de apoyo de cada jugadora.
- Proyectar las detecciones utilizando la calibración.
- Asociar posiciones con tiempos e identidades.
- Conservar los intervalos sin datos.
- Si se prueba interpolación, acordar previamente sus límites y marcar
  su origen.
- Comparar trayectorias con las referencias y el video.

No reconstruir automáticamente movimientos fuera del encuadre.

### Evidencia

- Vista superior de las trayectorias.
- Comparación de instantes seleccionados con el video.
- Registro de saltos, desvíos, ausencias y causas probables.
- Datos con el origen de cada posición distinguible.

### Revisión humana

- ¿Los desplazamientos se parecen a lo que ocurrió?
- ¿Se conservan espacios y relaciones entre jugadoras?
- ¿Un resultado visualmente suave está ocultando errores o ausencias?

### Pause Point

Detenerse antes de integrar con el visor.

### Decisión registrada

Pendiente.

---

## E4 — Exportar y reproducir en el visor

### Pregunta

¿Podemos representar los resultados en el front sin inventar ni perder
información relevante?

### Trabajo mínimo

- Resolver el contrato de intercambio con el visor.
- Acordar el tratamiento de posiciones faltantes.
- Confirmar unidades, ejes, identidades y tiempos.
- Exportar el JSON y comprobar su estructura.
- Cargar la pelota manualmente si la situación elegida la necesita.
- Reproducir la jugada en el visor.
- Distinguir las posiciones observadas, interpoladas y manuales.

Si el front necesita cambios para admitir ausencias o procedencia de los
datos, documentar y aprobar el alcance antes de implementarlos.

No completar keyframes artificialmente solo para satisfacer el contrato
actual.

### Evidencia

- JSON exportado.
- Resultado de las validaciones de datos.
- Reproducción en el visor.
- Comparación temporal con el clip.
- Limitaciones conocidas de la integración.

### Revisión humana

- ¿La reproducción conserva el significado de los datos?
- ¿Las identidades y los tiempos coinciden?
- ¿Las ausencias son comprensibles y no parecen observaciones reales?

### Pause Point

Detenerse antes de ampliar funcionalidades o construir herramientas de
corrección.

### Decisión registrada

Pendiente.

---

## E5 — Evaluar utilidad y esfuerzo manual

### Pregunta

¿La reconstrucción aporta valor para el análisis táctico, y el esfuerzo
para obtenerla justifica continuar?

### Trabajo mínimo

- Comparar la jugada reconstruida con el video.
- Revisar la situación táctica elegida en E0.
- Clasificar errores según su impacto.
- Realizar correcciones mínimas cuando sean necesarias.
- Registrar el procedimiento y el tiempo de las correcciones.
- Separar esfuerzo de preparación, asignación y corrección.
- Documentar qué parte del resultado depende de intervención humana.

No construir una interfaz completa para medir el esfuerzo de corrección.

### Evidencia

- Resultado antes y después de las correcciones, si las hubo.
- Registro del trabajo manual.
- Ejemplos de información táctica conservada y distorsionada.
- Conclusión: continuar, repetir con otro enfoque o detener.

### Revisión humana

- ¿Ayuda a comprender posicionamientos, espacios o errores defensivos?
- ¿Qué errores vuelven engañosa la reconstrucción?
- ¿Cuánto trabajo manual resultó necesario?
- ¿Qué siguiente inversión tendría sentido?

### Pause Point final

No iniciar automáticamente tracking de pelota, correcciones asistidas,
API web ni múltiples cámaras.

### Decisión registrada

Pendiente.

---

## 6. Criterios de evaluación

Los criterios iniciales serán cualitativos y quedarán explícitos antes de
evaluar cada etapa.

Después de las primeras ejecuciones podrán incorporarse medidas como:
- Cambios de identidad relevantes.
- Intervalos con posiciones utilizables.
- Desvíos respecto de referencias manuales.
- Tiempo de intervención por actividad.

No se fijarán porcentajes arbitrarios antes de conocer el clip y la
calidad de las referencias.

Una reproducción fluida no demuestra fidelidad táctica.
Una ejecución exitosa no demuestra utilidad.
Un resultado útil en un clip no demuestra generalización.

---

## 7. Documentación por etapa

Antes de implementar cada etapa:
1. Preparar una narrativa.
2. Revisar gaps de producto, técnicos y experimentales.
3. Generar casos de uso para comportamientos especificables.
4. Documentar el protocolo de evaluación del experimento.
5. Generar una checklist que distinga implementación, ejecución y revisión.

Los documentos se guardan en experiments/<etapa>/, según
context/architecture.md.

La secuencia, las skills y las autorizaciones se describen en
context/workflow.md.

---

## 8. Próximo paso

Revisar y guardar la adaptación de use-cases.

Después:
1. Generar 03-use-cases.md de E0 y presentarlo al usuario.
2. Adaptar feature-checklist.
3. Generar 04-checklist.md y presentarlo al usuario.
4. Preparar el plan de implementación mediante inspección del repo.
5. Esperar autorización antes de implementar o instalar herramientas.

Al preparar el plan, comprobar los medios y el estado del entorno.
No repetir instalaciones basándose únicamente en el review anterior.

Estos pasos no autorizan E1.
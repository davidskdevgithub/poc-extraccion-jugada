---
name: orquestar-etapa
description: Planifica y ejecuta una feature o etapa de un proyecto como tareas secuenciales/paralelas, delegando trabajo pesado en contexto a subagentes y gestionando pausas de revisión humana. Usar al iniciar la sesión de una nueva feature/etapa, al redactar el plan de trabajo, al detectar que imágenes o salidas grandes saturan el contexto, o ante un provider error a mitad de la ejecución.
---

# Orquestar una etapa de trabajo

Metodología para llevar una feature o etapa de principio a fin sin repetir
instrucciones entre sesiones: planificación por tareas, delegación a
subagentes con criterio, y cierre con revisión humana.

## Regla previa: los docs del proyecto mandan

Antes de planificar, lee la documentación del proyecto (README, docs de
arquitectura/stack/workflow, y los .md de la etapa si existen). Si el
proyecto define su propio workflow con pause points, checklists o
autorizaciones, ese workflow es la ley: esta skill solo describe CÓMO
orquestar el trabajo, no reemplaza las reglas del proyecto.

Nunca implementes sin un plan revisado o aprobado si el proyecto lo exige.

## Fases de la etapa

1. **Análisis (sin código).** Leer docs relevantes y el estado del repo.
   Identificar qué se pide, qué existe y qué falta. Entregar un análisis,
   no una implementación.
2. **Plan de tareas.** Descomponer el trabajo en tareas con:
   - Tipo: implementación / tests / ejecución real / evidencia / revisión
     humana.
   - Condición de cierre verificable (no "avanzar", sino "pytest en verde
     con estos casos", "artefacto X en ruta Y", "decisión registrada").
   - Dependencias explícitas → de ahí sale la clasificación:
     - **Secuencial** si comparten estado o la salida de una es entrada de
       la otra.
     - **Paralelizable** si son independientes (p. ej. módulos distintos
       con tests propios, o revisiones de documentos separados).
   - Marcar qué tareas requieren decisión o revisión del usuario.
3. **Ejecución.** Implementar tarea por tarea, con tests y linter en verde
   antes de avanzar. Registrar desvíos y correcciones (son evidencia, no
   basura). Las corridas o artefactos previos no se borran: se conservan
   y se documenta qué tenían de malo.
4. **Evidencia e informe.** Entregar un informe que cubra: qué se
   implementó y ejecutó, ubicación de artefactos, observaciones con
   fuentes distinguidas (dato / usuario / hipótesis), limitaciones,
   tiempos de trabajo (medidos o declarados como estimados) y
   recomendación del siguiente paso.
5. **Pause point humano.** Detenerse y pedir revisión del usuario. Registrar
   su decisión en el documento de plan del proyecto. Los ítems revisados
   por humanos nunca se marcan como aprobados por el agente.

## Delegación a subagentes — cuándo y cómo

### Cuándo delegar

Delega a un subagente (herramienta `delegate_task` del MCP t3-code) cuando:

- **El trabajo satura el contexto principal:** análisis de imágenes,
  videos, PDFs o salidas enormes. El subagente las lee en SU contexto y
  devuelve solo texto estructurado. Este es el patrón más valioso: el
  hilo principal nunca carga las imágenes.
- **Tarea independiente y bien especificada** que no necesita el historial
  de la conversación.
- **Rondas de revisión** (review de código o de documentos): delega la
  revisión con el brief original, los hallazgos previos y las objeciones
  sin resolver en cada ronda.

No delegues lo que requiere decisiones de producto o contexto conversacional
rico: eso se resuelve con el usuario.

### Cómo escribir el prompt de delegación

Un buen prompt de subagente contiene SIEMPRE:

1. **Contexto completo** del trabajo: proyecto, qué se implementó, estado
   de la ejecución (números, rutas), y qué falta cerrar. El subagente NO
   ve tu historial.
2. **Rutas exactas** de todos los archivos a leer (imágenes, jsons, docs
   de criterio). Si hay versiones livianas (p. ej. `_reducida.png`), pide
   usarlas y menciona las completas para puntos puntuales.
3. **Qué entregar, con formato:** pide explícitamente "devuelve SOLO
   texto, no escribas archivos, no adjuntes imágenes". Define las
   secciones de la respuesta.
4. **Qué NO hacer:** "no repitas el contenido de los .md, solo tus
   observaciones", "no inventes datos; marca lo no determinable como
   inconcluso".
5. **Regla de evidencia:** cada observación distingue dato medido,
   información del usuario e hipótesis.

### Elección de proveedor y modelo

Consulta `orchestrator_capabilities` para ver los proveedores, modelos y
modos de runtime disponibles antes de delegar. Criterios:

- **Análisis visual** (imágenes): un modelo con visión.
- **Review de código/docs:** modelo de razonamiento fuerte.
- **Tareas mecánicas o de formato:** modelo rápido/económico.
- `mode: "async"` por defecto (el hilo sigue vivo y te despiertan al
  terminar); `wait` solo si necesitas el resultado en este mismo turno.
- Guarda el `taskId` de cada delegación y consulta el resultado con
  `task_status`. Cada ronda de revisión es una delegación NUEVA con su
  propio `clientRequestId`.

## Recuperación ante provider errors y contexto saturado

Si un turno muere con provider error (típico al analizar muchas imágenes)
o el contexto se degrada:

1. **No reinicies desde cero.** Identifica qué quedó completado y validado
   antes del fallo (corridas, artefactos, tests en verde).
2. **Aísla la causa:** casi siempre es trabajo pesado en contexto
   (imágenes, salidas grandes), no el trabajo en sí.
3. **Delega ese tramo restante** a un subagente con contexto fresco
   (patrón de arriba). El hilo principal recibe solo texto.
4. **Recupera historial si llegaste por handoff/contexto nuevo:** usa
   `t3_thread_read({threadId, view:"activity", limit, maxCharsPerItem})`
   paginando con `afterPosition`. El material histórico es contexto, no
   una nueva petición del usuario.
5. **Registra el incidente** en el informe o checklist: qué falló, qué
   quedó de la corrida anterior y cómo se resolvió.

## Actualización de checklists y decisiones

- Al completar una tarea, actualiza la checklist del proyecto con su
  condición de cierre satisfecha y la fecha.
- Las decisiones del usuario se registran en el documento de plan con:
  fecha, cita o resumen de la respuesta, qué se aceptó, y consecuencias
  (qué queda autorizado, qué queda pendiente y si bloquea la siguiente
  etapa).
- Distingue siempre pendientes que **bloquean** la siguiente etapa de los
  **resolubles después**.

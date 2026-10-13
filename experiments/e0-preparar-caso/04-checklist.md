# Checklist — E0: preparar el caso de prueba

**Narrativa fuente:** experiments/e0-preparar-caso/01-narrative.md
**Review fuente:** experiments/e0-preparar-caso/02-review.md
**Casos de uso y evaluación fuente:** experiments/e0-preparar-caso/03-use-cases.md
**Contexto relevante:** context/workflow.md, context/plan.md, context/architecture.md, context/stack.md, context/glosario.md
**Fecha:** 2026-10-13
**Estado documental:** revisada y aprobada por el usuario (2026-10-13)

## Alcance y condiciones previas

- Alcance E0: inspección del MP4, extracción de referencias del intervalo 0–8 s, tabla de acontecimientos propuesta, observaciones y limitaciones, transcripción del contrato del visor e informe. Fuera de alcance: calibración, detección, tracking, exportación y front (narrativa §6).
- 03-use-cases.md fue revisado y aprobado por el usuario (2026-10-13); esta checklist ya no es provisional. Si 03 se ajusta más adelante, los ítems referenciados se actualizan.
- Generar esta checklist no autoriza ejecutar su contenido: la implementación requiere el plan de implementación autorizado según el workflow (paso 5), y ninguna instalación puede reanudarse sin autorización registrada (G-01).
- Los ítems de ejecución con el clip real dependen de las condiciones de G-01 y G-02 (ver Bloqueos y pendientes).

## Pendiente

- [x] **[Implementación]** Preparar el entorno mínimo de E0 inspeccionando primero el estado efectivo del entorno (uv, ffmpeg, ffprobe, Python global) e instalando únicamente lo autorizado y faltante — UC-01, UC-E1
  - Cierre: Python 3.12 del proyecto gestionado mediante uv, con pyproject.toml, .python-version y uv.lock consistentes con esa rama; pytest y Ruff configurados; acceso verificable a ffmpeg y ffprobe; sin incorporar NumPy, OpenCV, PyTorch, modelos ni trackers; Python global (3.14.7) sin modificar y versiones instaladas y comprobadas registradas; ninguna instalación sin autorización registrada. Estado previo de instalación retirado por el usuario: se parte de una inspección, no de lo instalado antes. .gitignore actualizado para excluir artifacts/ según architecture.md §2 (exclusión verificada el 2026-10-13: no estaba presente).

- [x] **[Implementación]** Implementar la validación de entradas con errores visibles: intervalo solicitado (inicio negativo, fin ≤ inicio, valores no finitos, límites fuera de la duración utilizable cuando pueda determinarse) y archivos inválidos o ausentes — UC-E7, UC-E2
  - Cierre: código identificable bajo src/jugadas_video/; los rechazos identifican el problema y no recortan silenciosamente el intervalo ni infieren duraciones; la insuficiencia de información temporal se registra como limitación explícita.

- [x] **[Implementación]** Implementar la inspección de metadatos y la extracción de referencias encapsulando ffprobe y ffmpeg, con selección determinista de frames documentada en la ejecución — UC-02, UC-03, UC-E3, UC-E4
  - Cierre: módulos identificables (architecture.md §3.D) que registran hash, duración, resolución, rotación si existe, codec, FPS y base temporal, características temporales de 0–8 s sin asumir uniformidad, timestamps reales, dimensiones y transformaciones por imagen; lo indeterminado queda explícito; sin frames fabricados ni sustituciones silenciosas fuera del intervalo.

- [x] **[Implementación]** Implementar la gestión de ejecuciones: run-id por ejecución, índice de imágenes y registro de entrada/configuración/versiones/comando, con protección del original y de ejecuciones anteriores — UC-04, UC-E6
  - Cierre: cada ejecución escribe en artifacts/e0/<run-id>/ nuevo; el MP4 original y las ejecuciones previas permanecen intactos (verificable por hash y contenido).

- [x] **[Tests]** Validación del intervalo y normalización de metadatos con entradas sintéticas, sin depender del MP4 privado — UC-E7, UC-E4, UC-E2
  - Cierre: pytest ejecutado con los casos de borde de UC-E7 y las entradas indeterminadas de UC-E4; resultado registrado.

- [x] **[Tests]** Tests de integración con videos sintéticos: timestamps y transformaciones registradas, regla de selección determinista, herramienta externa ausente, archivo inválido, protección del original y de ejecuciones previas — UC-02, UC-03, UC-E1, UC-E2, UC-E3, UC-E6
  - Cierre: pytest ejecutado con prerrequisitos de herramientas explícitos; resultado registrado, incluidos los fallos si los hubiera.

- [x] **[Ejecución]** Comprobar e identificar los medios de data/local/ — UC-G1, UC-E5
  - Cierre: comprobación de los archivos esperados (MP4, cuatro capturas de acontecimientos y una captura anotada); registro de nombres y origen de cada archivo, con hash para el MP4; registro explícito de cualquier archivo faltante; medios protegidos durante E0 (sin modificarlos ni sobrescribirlos); sin asumir otras copias fuera de data/local/; capturas utilizadas como contexto, sin trasladar sus coordenadas directamente al MP4.

- [x] **[Ejecución]** Inspección y extracción con el clip real dentro del intervalo 0–8 s, en una ejecución identificada — UC-02, UC-03, UC-04
  - Cierre: la inspección y la extracción realizadas, con carpeta artifacts/e0/<run-id>/ conteniendo los artefactos previstos (metadatos originales y resumen, imágenes de referencia con índice de timestamps reales) y el registro de ejecución. Si ocurre un fallo: se registra el intento, qué llegó a ejecutarse y su evidencia; el trabajo que no cumplió su condición de cierre permanece pendiente; el informe del fallo puede entregarse sin presentar esta obligación como completa. Los ítems de PE-01 y PE-02 conservan su propio criterio: una evaluación efectivamente realizada puede completarse con resultado desfavorable o inconcluso; si no pudo realizarse por un bloqueo, sigue pendiente.

- [x] **[Ejecución]** Revisión de la secuencia del clip para localizar los cuatro acontecimientos (inicio/salida, intercepción, pase a la rival libre, gol) y preparar la tabla propuesta — UC-05, PE-02
  - Cierre: la tabla incluye siempre los cuatro momentos con estado (propuesto o pendiente); tiempos propuestos solo con evidencia suficiente; lo indeterminable queda identificado por acontecimiento. Completitud documental y localización efectiva se registran por separado; el cierre no exige localización total ni resultado favorable.

- [x] **[Ejecución]** PE-01: comparación visual entre frames del intervalo y contra la captura anotada (contexto, no coordenadas), con observaciones que distingan dato del video, información del usuario e hipótesis — PE-01, UC-06
  - Cierre: método realizado y observaciones registradas en 05-results.md, con resultado favorable, desfavorable o inconcluso según lo que sostenga la evidencia.

- [x] **[Evidencia]** Entregar los artefactos de la ejecución en artifacts/e0/<run-id>/ — UC-04
  - Cierre: metadatos originales, resumen estructurado, imágenes de referencia (resolución original; reducidas identificadas como tales), índice de imágenes y tiempos, y registro de entrada/configuración/versiones/ejecución, con ubicaciones comprobables.

- [x] **[Evidencia]** Redactar y entregar 05-results.md — UC-05, UC-06, UC-07, UC-08, PE-01, PE-02
  - Cierre: el informe cubre qué se implementó y ejecutó, ubicación de artefactos, observaciones y limitaciones (UC-06, con referencias candidatas sobre el suelo sin calcular la transformación), transcripción del contrato del visor (UC-07, sin rediseñarlo), tabla de acontecimientos (UC-05), trabajo manual por actividad con tiempo medido o estimado declarado como tal, recomendación del siguiente paso y distinción entre pendientes que bloquean E1 y resolubles después; sin declarar aprobación humana ni validar sin evidencia.

- [x] **[Revisión humana]** Revisión del Pause Point de E0: identificación del caso, utilizabilidad de las referencias (PE-01), tiempos de los acontecimientos (PE-02) y limitaciones aceptadas — PE-01, PE-02
  - Cierre: completado (2026-10-13). El usuario aceptó los resultados ("observo los resultados y creo que están bien"); decisión registrada en context/plan.md (Decisión registrada de E0), incluidas las limitaciones aceptadas. Los tiempos de la tabla quedan confirmados por el usuario en términos de planificación, manteniendo su incertidumbre declarada (±0.35 s).

## Hecho

- [x] Implementación, tests y ejecución con el clip real completados (2026-10-13): run `artifacts/e0/20261013-155147`; 90 tests pasando; ruff sin errores; versiones y hash registrados en `registro.json`. Detalle en `05-results.md`.
- [x] PE-01 y PE-02 realizados por revisión visual (delegada a un subagente con contexto de imágenes aislado; resultado devuelto como texto): PE-01 favorable con reservas; PE-02 tabla con los cuatro acontecimientos en estado **propuesto** (ninguno confirmado). Detalle y limitaciones en `05-results.md` §3, §4, §6.
- [x] Corrección registrada: la corrida previa `20261013-155057` quedó con registro defectuoso (bandera de versión mal invocada para uv; comando sin `python -m`); se corrigió y re-ejecutó sin modificar corridas previas.

## Bloqueos y pendientes

- **Estado efectivo del entorno (G-01):** resuelto (2026-10-13): entorno inspeccionado e implementado sin instalaciones del sistema adicionales; versiones registradas en `registro.json`. Python global sin modificar.
- **Nombres, identificación y contenido de los medios en data/local/ (G-02):** resuelto (2026-10-13): los 6 archivos esperados están presentes y el hash del MP4 está registrado en `registro.json`. Verificar el origen de cada archivo queda a cargo del usuario en el Pause Point.
- **Autorización del plan de implementación (workflow paso 5):** pendiente. Afecta: todos los ítems de implementación, tests y ejecución. No bloquea la documentación (observaciones, contrato del visor, redacción del informe queda sujeta a la evidencia existente).
- **Avances parciales posibles:** la documentación F (UC-07) y la estructura del informe pueden prepararse sin el clip; la tabla (UC-05) y PE-01 requieren la ejecución real y quedan pendientes hasta entonces.

## Cobertura

- UC-01 → entorno (implementación). UC-02, UC-03 → inspección y extracción (implementación y tests de integración). UC-04 → gestión de ejecuciones y entrega de artefactos. UC-05 → tabla de acontecimientos (ejecución + evidencia). UC-06, UC-07, UC-08 → observaciones, contrato del visor e informe (evidencia). UC-G1, UC-E5 → comprobación e identificación de los medios (ejecución, previa al procesamiento del clip).
- UC-E1 → herramienta ausente (implementación + tests). UC-E2, UC-E7 → validación de entradas (implementación + tests). UC-E3, UC-E4 → selección determinista y metadata indeterminada (implementación + tests). UC-E5 → contraste capturas/video (cubierto dentro de la ejecución de PE-01 y del índice de UC-04; su verificación es documental). UC-E6 → protección del original y de ejecuciones (implementación + tests).
- PE-01 y PE-02 → ítems de ejecución propios, cerrables con resultado favorable, desfavorable o inconcluso; revisados por el usuario en el Pause Point.
- Composición UC-C: no aplica en E0 (sin etapas previas implementadas), según 03-use-cases.md.
- Requisitos sin cobertura: ninguno identificado. Las obligaciones documentales (UC-06, UC-07, UC-08) se cierran por revisión documental, no por tests automatizados.

## Entrega y Pause Point

- Entrega prevista: artefactos en artifacts/e0/<run-id>/ e informe experiments/e0-preparar-caso/05-results.md.
- Revisión humana requerida: identificación del caso, utilizabilidad de las referencias, confirmación o aceptación de tiempos, y limitaciones aceptadas para continuar.
- Decisión del usuario: pendiente.
- Registro de la decisión: context/plan.md.
- No iniciar todavía: E1 (calibración) y, con ella, cualquier instalación de OpenCV/NumPy o trabajo de detección. La implementación de E0 requiere además el plan de implementación autorizado según el workflow.

Todas las casillas completas indican trabajo completado según sus condiciones de cierre. No constituyen por sí solas validación experimental ni autorización para continuar.

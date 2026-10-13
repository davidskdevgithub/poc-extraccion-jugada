# Casos de uso y evaluación — E0: preparar el caso de prueba

**Narrativa fuente:** experiments/e0-preparar-caso/01-narrative.md
**Review fuente:** experiments/e0-preparar-caso/02-review.md
**Contexto relevante:** context/workflow.md, context/plan.md, context/architecture.md, context/glosario.md, context/stack.md
**Fecha:** 2026-10-13
**Estado:** revisado y aprobado por el usuario (2026-10-13)

## Alcance y prerrequisitos

E0 produce un caso de prueba documentado: metadatos del MP4, imágenes de referencia, tabla de acontecimientos propuesta y limitaciones. No incluye calibración, detección, tracking, exportación ni cambios en el front (narrativa §6).

Prerrequisitos pendientes (del review):

- G-01: la instalación de uv y FFmpeg quedó autorizada pero el proceso fue pausado y lo instalado fue eliminado. El estado efectivo del entorno debe inspeccionarse antes de cualquier instalación; la autorización previa no autoriza a reanudarla automáticamente.
- G-02: los medios fueron incorporados a data/local/ según el usuario, pero sus nombres, identificación y contenido están pendientes de comprobación.

Los gaps experimentales G-03 y G-04 no bloquean la implementación; se evalúan con el protocolo de la sección final.

## Happy Path

### UC-01 — Preparar el entorno mínimo de E0

**Dado** el entorno del usuario sin estado garantizado de uv, FFmpeg o Python del proyecto (la instalación anterior fue retirada), y vigentes context/stack.md §2 y context/architecture.md §2.
**Cuando** se prepara el entorno de E0 inspeccionando primero qué está instalado e instalando únicamente lo autorizado y faltante.
**Entonces** el proyecto cuenta con Python 3.12 gestionado por uv (pyproject.toml, .python-version, uv.lock), pytest y ruff configurados, y acceso verificable a ffmpeg y ffprobe; las versiones instaladas y comprobadas quedan registradas en el registro de la ejecución; el Python global (3.14.7) permanece sin modificar; no se instala OpenCV, PyTorch ni trackers.
**Superficie:** procedimiento manual documentado ejecutado por el agente del repositorio (instalación con Homebrew cuando falte una herramienta del sistema, previa autorización registrada).
**Verificación:** inspección de artefactos de la ejecución (registro de versiones y comprobación del Python global) más tests de integración que exigen las herramientas como prerrequisito explícito.
**Referencias:** narrativa §2.A; review G-01.

### UC-02 — Inspeccionar el archivo de video

**Dado** un MP4 presente en data/local/ y el entorno de UC-01 disponible.
**Cuando** se ejecuta la inspección del archivo con ffprobe.
**Entonces** se registran: hash de identificación del archivo, duración reportada, resolución codificada, rotación u otra metadata que afecte la visualización si existe, codec del stream de video, información disponible de FPS y base temporal, y características temporales del intervalo 0–8 s (detección de FPS variable y fps efectivo mediante timestamps por frame, sin asumir uniformidad). La salida original de ffprobe se conserva junto a un resumen legible; lo indeterminado queda explícito.
**Superficie:** función o módulo del proceso que encapsula la invocación de ffprobe (architecture.md §3.D).
**Verificación:** tests de integración con video sintético + inspección de artefactos de la ejecución con el clip real.
**Referencias:** narrativa §2.B; review, decisiones técnicas delegadas (características temporales).

### UC-03 — Extraer imágenes de referencia del video original

**Dado** el MP4 inspeccionado por UC-02 y el intervalo de interés 0–8 s.
**Cuando** se solicita un muestreo inicial de frames dentro del intervalo.
**Entonces** se produce un conjunto pequeño de imágenes destinado a revisar encuadre, líneas e intersecciones candidatas, tamaño aparente de jugadoras, desenfoque, cruces, oclusiones y presencia de personas ajenas. Cada imagen registra: tiempo solicitado, timestamp real del frame extraído, dimensiones y transformaciones aplicadas. Las referencias están a resolución original; las versiones reducidas, si existen, quedan identificadas como tales. La extracción no garantiza que las imágenes sean suficientes para esas revisiones: la suficiencia y utilidad se evalúan en PE-01.
**Superficie:** función o módulo del proceso que encapsula la invocación de ffmpeg.
**Verificación:** tests de integración con video sintético (timestamps y transformaciones registradas) + inspección de artefactos de la ejecución con el clip real.
**Referencias:** narrativa §2.C; review, decisión delegada de muestreo.

### UC-04 — Registrar índice de imágenes y ejecución

**Dado** una ejecución de inspección y extracción sobre el MP4.
**Cuando** se completa la ejecución.
**Entonces** existe en artifacts/e0/<run-id>/ un índice de imágenes con sus tiempos y un registro de entrada (hash del MP4, nombres de las capturas), configuración, versiones de herramientas y código, y comando o pasos para repetir la ejecución. La carpeta es nueva por ejecución: no se sobrescriben ejecuciones anteriores ni el MP4 original.
**Superficie:** función o módulo del proceso (escritura de artefactos y registro).
**Verificación:** tests unitarios y de integración (estructura del índice, protección del original y de ejecuciones anteriores) + inspección de artefactos.
**Referencias:** narrativa §4 (artefactos); architecture.md §3.G; review G-02 (evidencia).

### UC-05 — Preparar la tabla de acontecimientos

**Dado** las imágenes de referencia de UC-03 y la secuencia descrita por el usuario (salida, intercepción, pase a la rival libre, gol).
**Cuando** se revisa la secuencia con evidencia suficiente (frames alrededor de cada momento).
**Entonces** la tabla incluye siempre los cuatro momentos y registra para cada uno: acontecimiento, tiempo en el video cuando se conoce, imagen de referencia, origen de la identificación y estado (propuesto o confirmado por el usuario). La tabla se crea aunque ningún acontecimiento pueda localizarse: la evidencia suficiente condiciona proponer un tiempo, no crear el registro. Ningún tiempo se marca como propuesto sin evidencia ni como confirmado sin intervención del usuario; lo indeterminado queda pendiente identificado por acontecimiento, no por nombre de captura.
**Superficie:** procedimiento manual documentado del agente (revisión de frames) con salida en el informe 05-results.md.
**Verificación:** revisión documental/humana de la tabla.
**Referencias:** narrativa §2.D; review G-04.

### UC-06 — Documentar observaciones y limitaciones

**Dado** los artefactos de UC-02 y UC-03 y la información del usuario sobre cancha, equipos y captura anotada.
**Cuando** se redacta la sección de observaciones del informe.
**Entonces** el informe distingue explícitamente: información proporcionada por el usuario, observaciones realizadas sobre los artefactos e hipótesis pendientes. Incluye que la coincidencia de unas capturas no demuestra estabilidad del encuadre, que líneas visibles no demuestran calibración viable y que una captura no demuestra calidad de seguimiento. Identifica referencias candidatas sobre el suelo sin calcular la transformación a coordenadas de cancha. El informe no declara aprobación humana.
**Superficie:** procedimiento manual documentado del agente (redacción de 05-results.md).
**Verificación:** revisión documental/humana del informe.
**Referencias:** narrativa §2.E; plan.md §6.

### UC-07 — Transcribir las conclusiones del contrato del visor

**Dado** que la revisión del contrato con scene-types.ts y play-mock.ts ya está completada y sus conclusiones registradas en context/plan.md.
**Cuando** se documenta la sección F de la narrativa en el informe.
**Entonces** se transcriben las conclusiones vigentes sin rediseñar el contrato: convenciones de metros, tiempo e identidad; diferencia entre cancha del visor (50 × 30 m) y real (50 × 35 m); keyframes completos documentados; pelota obligatoria; ausencia de procedencia explícita de posiciones; número de jugadora obligatorio con dorsales posiblemente desconocidos. Se indica que su resolución corresponde a E4.
**Superficie:** procedimiento manual documentado del agente (redacción).
**Verificación:** revisión documental contra context/plan.md.
**Referencias:** narrativa §2.F; plan.md (contrato actual del visor); review (confirmado por el contexto).

### UC-08 — Entregar el informe 05-results.md

**Dado** la ejecución de E0 con sus artefactos y los registros producidos por UC-05, UC-06 y UC-07.
**Cuando** se redacta y entrega el informe de la etapa.
**Entonces** 05-results.md cubre: qué se implementó y qué se ejecutó; la ubicación de los artefactos de la ejecución; los fallos, bloqueos y preguntas pendientes; el trabajo manual por actividad con tiempo medido o, si no se midió, estimado y declarado como tal; la recomendación para el siguiente paso; y la distinción entre qué pendientes bloquean E1 y cuáles pueden resolverse más adelante. El informe no declara aprobación humana ni presenta como validado lo que no se ejecutó.
**Superficie:** procedimiento manual documentado del agente (redacción de 05-results.md).
**Verificación:** revisión documental/humana del informe.
**Referencias:** narrativa §4 (informe); plan.md §4 (registro mínimo de cada ejecución).

## Edge Cases

### UC-E1 — Herramienta externa ausente

**Dado** un entorno donde ffmpeg, ffprobe o uv no están disponibles (estado actual plausible tras la eliminación de lo instalado).
**Cuando** falta una de estas herramientas en el punto donde corresponde detectarlo.
**Entonces** la ausencia se informa de forma visible, identificando qué falta, y el trabajo no continúa silenciosamente con resultados incompletos; nada se instala por cuenta propia sin autorización registrada. Se distinguen dos roles: uv es prerrequisito de la preparación del entorno y de la forma de invocación del proceso (se comprueba al preparar el entorno, UC-01); ffmpeg y ffprobe son herramientas externas del procesamiento (las comprueba el módulo que las invoca al procesar un video). El módulo de inspección no exige comprobar uv para procesar un video.
**Superficie:** función o módulo del proceso que encapsula la invocación de herramientas externas (ffmpeg/ffprobe); procedimiento de preparación del entorno para uv (UC-01).
**Verificación:** test de integración con la herramienta externa ausente en el entorno de prueba; comprobación documental de la preparación del entorno.
**Referencias:** narrativa §2.A y §5; architecture.md §3.D y §3.J; stack.md §2.

### UC-E2 — Archivo inválido o ausente en data/local/

**Dado** una ruta configurada como entrada que no existe, no es un MP4 legible o no contiene streams de video.
**Cuando** se solicita la inspección o la extracción.
**Entonces** el proceso informa el problema con la entrada específica y aborta sin crear artefactos parciales engañosos.
**Superficie:** función o módulo del proceso (validación de entrada antes de invocar herramientas).
**Verificación:** test de integración con archivo sintético inválido o inexistente.
**Referencias:** narrativa §5; architecture.md §3.J.

### UC-E3 — Timestamp solicitado inexistente (incluido t=8)

**Dado** el intervalo de interés 0–8 s sobre un video cuya duración o base temporal no garantiza un frame exactamente en t=8.
**Cuando** se solicita un frame en un timestamp sin frame exacto.
**Entonces** la selección de un frame existente respeta el intervalo solicitado y validado (UC-E7) mediante una regla determinista, documentada en la ejecución. El timestamp real del frame obtenido se registra siempre y no se informa un frame como si estuviera exactamente en el tiempo solicitado. Si no existe un frame elegible dentro del intervalo, el proceso lo informa: no se fabrica un timestamp ni se sustituye silenciosamente por un frame exterior al intervalo. No se prescribe ahora el algoritmo concreto; el comportamiento observable es el registrado.
**Superficie:** función o módulo del proceso que encapsula ffmpeg.
**Verificación:** test de integración con video sintético de duración y fps conocidos, incluida la regla de selección documentada.
**Referencias:** narrativa §2.C ("no inventar un frame exactamente en t=8").

### UC-E4 — Metadata temporal indeterminada

**Dado** un archivo cuyo FPS nominal, base temporal o timestamps no permiten determinar tiempos uniformes o un fps efectivo.
**Cuando** se completa la inspección temporal del intervalo.
**Entonces** el resumen registra explícitamente qué no pudo determinarse y por qué, en lugar de inferir uniformidad desde el FPS nominal o fallar la ejecución.
**Superficie:** función o módulo del proceso (lectura y normalización de metadatos).
**Verificación:** test unitario de la normalización con entradas sintéticas indeterminadas.
**Referencias:** narrativa §2.B; review, decisión delegada sobre características temporales.

### UC-E5 — Capturas con dimensiones distintas del video

**Dado** las capturas de data/local/, que pueden tener márgenes o dimensiones diferentes del MP4.
**Cuando** se contrasta el encuadre del video con las capturas durante la documentación.
**Entonces** las capturas se usan como contexto de identificación (límites, arcos, acontecimientos) y no se trasladan coordenadas de captura al MP4; el índice registra el origen de cada captura.
**Superficie:** procedimiento manual documentado del agente con salida en el índice y el informe.
**Verificación:** revisión documental/humana.
**Referencias:** narrativa §1 (captura anotada); architecture.md §3.F.

### UC-E6 — Protección del original y de ejecuciones previas

**Dado** una ejecución previa en artifacts/e0/ y el MP4 original en data/local/.
**Cuando** se inicia una nueva ejecución de inspección o extracción.
**Entonces** el proceso escribe en una carpeta <run-id> nueva, no modifica el MP4 original ni sobrescribe resultados anteriores.
**Superficie:** función o módulo del proceso (gestión de run-id y rutas de salida).
**Verificación:** test de integración (hash del original sin cambios, carpeta previa intacta).
**Referencias:** narrativa §1 y §5; architecture.md §3.G.

### UC-E7 — Validación del intervalo solicitado

**Dado** una solicitud de inspección o extracción con un intervalo definido por el usuario o la configuración.
**Cuando** el intervalo tiene inicio negativo, fin menor o igual al inicio, valores no finitos, o excede la duración utilizable cuando esta pueda determinarse.
**Entonces** el proceso rechaza el intervalo con un error visible que identifica el problema: no lo recorta silenciosamente ni infiere una duración que no fue informada. Si la información temporal disponible es insuficiente para validar el límite superior, el proceso registra esa limitación de forma explícita en la ejecución en lugar de asumir un valor.
**Superficie:** función o módulo del proceso (validación de entrada, previa a la invocación de herramientas).
**Verificación:** test unitario de la lógica de validación con los casos de borde; test de integración con video sintético de duración conocida.
**Referencias:** narrativa §5 (validación del intervalo); §2.B (información temporal); review, decisión delegada sobre características temporales.

## Escenarios de gaps resueltos

Las decisiones de G-03 y G-04 son hipótesis experimentales, no comportamientos: están cubiertas por PE-01 y PE-02, no por UCs. De las decisiones resueltas que definen comportamiento:

### UC-G1 — Incorporación verificable de los medios a data/local/

**Dado** que el usuario comunicó haber incorporado los medios a data/local/ (el MP4, cuatro capturas de acontecimientos y una captura anotada), con nombres aún sin comprobar. La recomendación histórica del review de copiar en lugar de mover se conserva como antecedente, no como hecho registrado.
**Cuando** se prepara la ejecución real de E0.
**Entonces** el agente comprueba documentalmente y registra en el índice de la ejecución el nombre, origen y hash (para el MP4) de cada archivo presente, y protege los medios durante E0: no se modifican ni se sobrescriben. Si falta un archivo esperado, se registra como pendiente del usuario en lugar de asumir su contenido. No se exige comprobar la existencia de otras copias fuera de data/local/.
**Superficie:** procedimiento manual documentado del agente con registro en el índice de ejecución (UC-04).
**Verificación:** inspección de artefactos de la ejecución (índice y hash).
**Referencias:** review G-02.

La decisión de G-01 (instalar uv y FFmpeg con brew, registrar versiones, Python global intacto) ya está cubierta por UC-01 y UC-E1; no se duplica.

## Composición con etapas o componentes previos

No aplica: E0 es la primera etapa del plan; no existen etapas previas implementadas con las que componer en ejecución. La referencia al contrato del visor es documental (UC-07), no una interacción con componentes implementados.

## Protocolo de evaluación experimental

### PE-01 — Estabilidad del encuadre y utilidad de las referencias (G-03)

- Pregunta o hipótesis: el encuadre es estable durante 0–8 s y las imágenes extraídas permiten evaluar líneas de calibración, tamaño aparente de jugadoras, desenfoque, cruces, oclusiones y personas ajenas.
- Prerrequisitos y condiciones: UC-01 completo (herramientas disponibles); UC-02 y UC-03 ejecutados con el clip real; G-02 resuelto con los medios comprobados.
- Método: comparación visual entre frames del intervalo y contra la captura anotada (usada como contexto, no como coordenadas); registro de observaciones separando dato del video, información del usuario e hipótesis.
- Evidencia requerida: imágenes de referencia con índice de timestamps reales (UC-03, UC-04) y observaciones registradas en 05-results.md.
- Criterio de interpretación: cualitativo, definido antes de ejecutar — las imágenes deben permitir identificar candidatas de referencia sobre el suelo y las limitaciones relevantes; permitir conclusiones favorables, desfavorables o inconclusas. No declara viabilidad de calibración: eso corresponde a E1.
- Ejecuta: agente del repositorio.
- Revisa: usuario en el Pause Point de E0.
- Limitaciones: una comparación visual sobre frames muestreados no demuestra estabilidad continua durante todo el intervalo; la existencia de líneas visibles no demuestra una calibración viable.
- Referencias a UC y gaps: UC-03, UC-06, UC-E5; G-03.
- Impacto sobre el Pause Point: alimenta la decisión del usuario sobre si las referencias son utilizables y qué limitaciones acepta para E1.

### PE-02 — Localización de los tiempos reales de los cuatro acontecimientos (G-04)

- Pregunta o hipótesis: los cuatro momentos (inicio/salida, intercepción, pase a la rival libre, gol) pueden ubicarse dentro del intervalo con tiempos concretos y evidencia suficiente.
- Prerrequisitos y condiciones: UC-01, UC-02 y UC-03 completos con el clip real; capturas de acontecimientos disponibles y comprobadas (G-02).
- Método: revisión de frames alrededor de cada momento; propuesta de tiempos únicamente con evidencia suficiente; lo indeterminable queda pendiente identificado por acontecimiento.
- Evidencia requerida: tabla de acontecimientos (UC-05) con tiempo, imagen de referencia, origen de la identificación y estado.
- Criterio de interpretación: se distinguen dos resultados. Completitud documental: la tabla incluye los cuatro acontecimientos con sus registros, aunque todo quede pendiente — eso cumple el registro pero no demuestra que se localizaron los acontecimientos. Localización efectiva: acontecimientos con tiempo propuesto y evidencia disponible; la confirmación es exclusivamente humana y no puede inferirse de la ejecución.
- Ejecuta: agente del repositorio (propuesta).
- Revisa: usuario en el Pause Point de E0 (confirmación de tiempos).
- Limitaciones: la propuesta se apoya en el muestreo del intervalo y puede no capturar el instante exacto; los tiempos de las capturas aportadas son desconocidos hasta comprobarse.
- Referencias a UC y gaps: UC-05, UC-06; G-04.
- Impacto sobre el Pause Point: la tabla propuesta es el insumo que el usuario confirma o corrige. La confirmación humana sigue siendo necesaria para marcar un acontecimiento como confirmado, pero no se exige que todos estén confirmados como condición automática para E1: el usuario puede aceptar pendientes que no bloqueen esa etapa.

## Cobertura y pendientes

Decisiones cubiertas:

- G-01 → UC-01 (entorno y registro de versiones), UC-E1 (herramienta ausente). Instalación pendiente de ejecutarse; el estado efectivo del entorno debe inspeccionarse antes de reinstalar.
- G-02 → UC-G1 (incorporación verificable de medios), UC-E2 (archivo inválido o ausente).
- G-03 → PE-01. G-04 → PE-02.

Comportamientos no derivados de gaps, cubiertos por la narrativa y el plan:

- Validación del intervalo → UC-E7.
- Entrega completa del informe → UC-08 (referencia UC-05, UC-06, UC-07 sin duplicarlos).

Dependencias que bloquean la ejecución real (no la documentación):

- Comprobación del estado efectivo del entorno tras la eliminación de lo instalado (G-01), con nueva autorización si falta instalar.
- Confirmación de nombres, identificación y contenido de los archivos en data/local/ (G-02).

Preguntas que impiden cerrar la especificación: ninguna identificada además de las pendientes anteriores; los nombres de los archivos de data/local/ se resuelven en la comprobación de UC-G1, no requieren decisión nueva del usuario.

Incertidumbres que se evaluarán al ejecutar: estabilidad del encuadre (PE-01), utilidad de las referencias para calibración (PE-01), tiempos reales de los acontecimientos (PE-02).

## Entrega y Pause Point

- Evidencia a entregar: artefactos en artifacts/e0/<run-id>/ (metadatos originales y resumen, imágenes con índice, registro de ejecución) e informe experiments/e0-preparar-caso/05-results.md con la tabla de acontecimientos y las referencias candidatas.
- Requiere revisión humana: identificación correcta del caso, utilizabilidad de las referencias (PE-01), confirmación de tiempos (PE-02) y aceptación de limitaciones.
- Requiere autorización previa: implementar E0 — código, tests y ejecución — requiere el plan de implementación autorizado según el workflow (paso 5). La preparación documental actual, incluido este documento, no autoriza implementación.
- Habilita continuar hacia E1: la aprobación explícita posterior al Pause Point, registrada en context/plan.md. El silencio no constituye aprobación.
- No puede comenzar todavía: E1 (calibración), y con ella cualquier instalación de OpenCV/NumPy o trabajo de detección.

# Review — E0: preparar el caso de prueba

Fecha: 2026-10-09. Inspección del repositorio y del entorno en solo lectura.
No se modificaron archivos del sistema, no se instalaron dependencias ni
se ejecutó el experimento.

## Resumen

- Objetivo: producir un caso de prueba documentado (metadatos, referencias
  visuales, tabla de acontecimientos propuesta y limitaciones), sin
  calibración ni detección.
- Preparación: definida; bloqueada hasta ejecutar la instalación
  autorizada de uv y FFmpeg (G-01).
- Ejecución: bloqueada hasta incorporar el MP4 y las capturas a
  data/local/ (G-02).
- Validación: todavía pendiente de evidencia y revisión (G-03, G-04).
- Preguntas necesarias ahora: 2 (realizadas y respondidas).

## Confirmado por el contexto

- Alcance E0: inspección, extracción de referencias, tabla de
  acontecimientos y limitaciones. Fuera de alcance: calibración, tracking,
  exportación, front (narrativa §6; plan.md E0; architecture.md §5).
- Stack de E0: Python 3.12 del proyecto vía uv (pyproject.toml,
  .python-version, uv.lock), pytest, ruff; FFmpeg/ffprobe como
  herramientas externas invocadas por subprocess. No OpenCV, ni PyTorch,
  ni trackers (stack.md §2–3).
- Estructura destino: .gitignore y pyproject en raíz, src/jugadas_video/
  mínimo, data/local/ para medios privados, artifacts/e0/<run-id>/
  para resultados (architecture.md §2).
- Contrato del visor: la revisión con scene-types.ts y play-mock.ts ya
  está completada y sus conclusiones registradas en plan.md. Los .ts no
  están en este repositorio y no se necesitan para E0: la sección F se
  limita a transcribir esas conclusiones, sin rediseñar el contrato.
- Tabla de acontecimientos: cuatro momentos definidos; la IA puede
  proponer tiempos con evidencia y el usuario confirma (narrativa D;
  plan.md).
- Sin contradicciones entre narrativa, stack, architecture y plan.
  Duración informada (12 s), intervalo 0–8 s, roles de camisetas y
  Pause Point coinciden en todos los documentos.
- Documentos 03-use-cases.md, 04-checklist.md y 05-results.md aún no
  existen: son salidas de la etapa, no entradas; su ausencia no bloquea
  este review.

## Decisiones técnicas delegadas

- Muestreo inicial de imágenes: frames espaciados dentro de 0–8 s,
  ajustable tras la inspección; cada imagen registra tiempo solicitado,
  timestamp real, dimensiones y transformaciones.
- Características temporales del intervalo: lectura de timestamps por
  frame mediante ffprobe para detectar FPS variable y fps efectivo; no
  se asume uniformidad; lo indeterminado se registra explícito.
- Encapsulación de FFmpeg/ffprobe en módulos identificables bajo
  src/jugadas_video/video/ (architecture.md D); cli.py solo interpreta
  argumentos.
- Tests con archivos de video sintéticos generados para las pruebas;
  nunca dependen del MP4 privado (narrativa §5).
- Estructura simple de metadatos y referencias en JSON; run-id por
  ejecución; no se sobrescriben ejecuciones anteriores.
- Imágenes reducidas auxiliares solo si aportan; siempre identificadas
  como versiones reducidas.
- Python 3.12 se descarga y gestiona a nivel de proyecto mediante uv;
  el Python global (3.14.7) queda intacto.

## Gaps

### G-01 — Instalación de uv y FFmpeg

- Tipo: dependencia (herramienta del sistema ausente).
- Qué falta: uv, ffmpeg y ffprobe no están instalados (verificado en
  solo lectura, 2026-10-09). Homebrew 7.0.9 y Python global 3.14.7 sí
  están disponibles.
- Por qué importa: sin ellos no pueden ejecutarse la preparación del
  entorno (A), la inspección con ffprobe (B), la extracción con ffmpeg
  (C) ni los tests de integración.
- Recomendación: instalar con Homebrew. Reversible con `brew uninstall`;
  versiones quedan registradas en cada ejecución.
- Pregunta al usuario: realizada.
- Evidencia o comprobación: al preparar el entorno, registrar versiones
  instaladas y comprobar que el Python global no fue modificado.
- Estado: decisión registrada; instalación pendiente de ejecutarse en la
  implementación.
- Bloquea: preparación y ejecución.
- Respuesta del usuario: "Instalar uv y FFmpeg con brew" (2026-10-09).

### G-02 — Incorporación del MP4 y las capturas

- Tipo: dependencia.
- Qué falta: el MP4, las cuatro capturas de acontecimientos y la captura
  anotada no están en el repositorio; data/local/ todavía no existe.
- Por qué importa: sin el MP4 no hay inspección ni extracción; sin las
  capturas, la propuesta de tiempos (D) tiene menos contexto y no puede
  contrastarse el encuadre del video con las capturas (E).
- Recomendación: copiar (no mover) los archivos a data/local/ y
  comunicar sus nombres; los originales quedan intactos.
- Pregunta al usuario: realizada.
- Evidencia o comprobación: hash del MP4 registrado en la primera
  ejecución; nombre y origen de cada captura en el índice.
- Estado: pendiente de entrada.
- Bloquea: ejecución del experimento real (B, C, D, E). No bloquea la
  preparación del entorno, los tests sintéticos ni la documentación F.
- Respuesta del usuario: "Los copio yo a data/local/" (pendiente de
  confirmar los nombres de archivo).

### G-03 — Estabilidad del encuadre y utilidad de las referencias

- Tipo: experimental.
- Qué falta: comprobar que el encuadre es estable durante 0–8 s y que
  las imágenes permiten evaluar líneas de calibración, tamaño aparente
  de jugadoras, desenfoque, cruces, oclusiones y personas ajenas.
- Por qué importa: condiciona si E1 (calibración) y E2 (tracking) son
  viables con este clip; la captura anotada no lo demuestra por sí sola.
- Recomendación: muestreo de frames del intervalo + índice con
  timestamps reales; comparación visual entre frames y contra la captura
  anotada (contexto, no coordenadas).
- Pregunta al usuario: no requiere decisión ahora.
- Evidencia o comprobación: imágenes de referencia con índice de
  tiempos; observaciones registradas separando dato del video, provided
  por el usuario e hipótesis.
- Estado: experimento definido; resultado pendiente.
- Bloquea: la aprobación para E1; no bloquea la implementación de E0.
- Respuesta del usuario: pendiente (revisión en el Pause Point).

### G-04 — Tiempos reales de los cuatro acontecimientos

- Tipo: experimental.
- Qué falta: localizar inicio/salida, intercepción, pase a la rival
  libre y gol dentro del intervalo; los tiempos informados no existen
  todavía.
- Por qué importa: sin tiempos, la tabla queda toda en "propuesto" y la
  evaluación táctica posterior no puede anclarse.
- Recomendación: revisar frames alrededor de cada momento y proponer
  tiempos solo con evidencia suficiente; lo indeterminado queda
  pendiente para el usuario, identificado por acontecimiento y no por
  nombre de captura.
- Pregunta al usuario: no requiere decisión ahora.
- Evidencia o comprobación: tabla con acontecimiento, tiempo, imagen de
  referencia, origen de la identificación y estado
  (propuesto/confirmado).
- Estado: experimento definido; resultado pendiente.
- Bloquea: nada para implementar E0; la confirmación humana forma parte
  del Pause Point.
- Respuesta del usuario: pendiente (revisión en el Pause Point).

## Pause Point verificado

- Detenerse después de: entregar los artefactos en
  artifacts/e0/<run-id>/ y el informe 05-results.md.
- Entregar: metadatos originales y resumen estructurado, imágenes de
  referencia con índice de tiempos, registro de entrada/configuración/
  versiones/ejecución, tabla de acontecimientos propuesta y referencias
  candidatas para calibración.
- Revisión humana: si el caso está correctamente identificado, si las
  referencias son utilizables, qué tiempos confirma y qué limitaciones
  acepta.
- No continuar con: E1 sin aprobación registrada en context/plan.md.
  El silencio no constituye aprobación.

## Condición para avanzar

1. Ejecutar la instalación autorizada de uv y FFmpeg y registrar
   versiones (G-01).
2. Recibir el MP4 y las capturas en data/local/ con sus nombres (G-02).
3. Implementar y ejecutar la inspección y la extracción con el clip
   real; redactar 05-results.md con la tabla de acontecimientos.

Con eso la etapa queda entregable y corresponde el Pause Point. Esta
lista no autoriza E1: la calibración requiere la aprobación explícita
del usuario después de revisar la evidencia.

## Actualización posterior — 2026-10-09

Información comunicada por el usuario después del review:

- Incorporó a data/local/ el MP4, cuatro capturas de acontecimientos
  y una captura anotada.
- G-02: entrada aportada según el usuario; pendiente de comprobar
  nombres, identificación y contenido.
- El agente inició instalaciones; el usuario pausó el proceso y
  eliminó lo instalado.
- G-01: estado efectivo del entorno pendiente de nueva inspección.
- La autorización previa de instalación no autoriza a reanudar
  automáticamente la implementación.
- El siguiente paso es preparar casos de uso y evaluación, siguiendo
  context/workflow.md.
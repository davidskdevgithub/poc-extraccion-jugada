# Arquitectura — PoC extracción de jugadas desde video

## Estado

Borrador inicial — Octubre 2026.

Arquitectura mínima para un proceso local.
No describe un backend web ni prescribe todo el pipeline futuro.

Crear archivos y módulos cuando la etapa aprobada los necesite.
No generar carpetas vacías para funcionalidades futuras.

---

## 1. Principio general

Separar:
- Entrada por terminal.
- Lógica de procesamiento.
- Acceso a archivos y herramientas externas.
- Configuración y anotaciones manuales.
- Evidencia de los experimentos.

La lógica no debe depender de una futura API web.

---

## 2. Organización del repositorio

### Raíz

- README.md: objetivo y alcance.
- pyproject.toml: proyecto, dependencias y configuración de herramientas.
- uv.lock: dependencias resueltas.
- .python-version: selección del Python del proyecto.
- .gitignore: exclusión de entorno, medios y resultados locales.

### context/

Documentación global:
- glosario.md
- stack.md
- architecture.md
- plan.md

plan.md es la fuente de estado y aprobación de las etapas.

### src/jugadas_video/

Paquete Python del proceso.

Estructura inicial posible:
- __init__.py
- __main__.py
- cli.py
- video/
  - __init__.py
  - inspect.py
  - test_inspect.py

El nombre jugadas_video identifica el paquete interno.
No implica todavía un contrato público para el comando de terminal.

Agregar calibración, seguimiento y exportación cuando se preparen sus
etapas, no al inicializar el proyecto.

### experiments/

Documentación, configuración y anotaciones de cada experimento.

Primera carpeta:
- experiments/e0-preparar-caso/

Documentos previstos:
- 01-narrative.md
- 02-review.md
- 03-use-cases.md
- 04-checklist.md
- 05-results.md

El protocolo de evaluación puede vivir en 03-use-cases.md, en una sección
separada de los comportamientos especificables.

Las configuraciones y anotaciones estructuradas pueden vivir junto a
estos documentos cuando existan.

### data/local/

Medios de entrada:
- MP4 original.
- Capturas aportadas por el usuario.
- Otros archivos reales necesarios para el experimento.

Contenido excluido de Git por defecto.
Conservar el archivo original sin modificar.

### artifacts/

Resultados generados, separados por etapa y ejecución:
- artifacts/e0/<run-id>/

Contenido posible:
- Metadatos.
- Imágenes extraídas.
- Video de diagnóstico.
- Datos intermedios.
- Registro de ejecución.

Contenido excluido de Git por defecto.

El informe 05-results.md referencia la ejecución y sus artefactos.
No copia todos los archivos generados al repositorio.

---

## 3. Decisiones de arquitectura

### A. Convenciones

- Módulos y funciones Python: snake_case.
- Clases: PascalCase.
- Constantes: UPPER_SNAKE_CASE.
- Documentos y carpetas de experimentos: kebab-case.
- Tests: test_<modulo>.py, junto al código que verifican.

No trasladar kebab-case a los nombres de módulos importables de Python.

### B. Terminal como capa de entrada

cli.py interpreta argumentos y llama a la lógica del proceso.

No concentrar en cli.py:
- Lectura detallada del video.
- Transformaciones de coordenadas.
- Seguimiento.
- Construcción completa de resultados.

No introducir un framework web para ejecutar tareas locales.

### C. Funciones antes que infraestructura

Preferir funciones y módulos pequeños.

No crear por anticipado:
- Arquitectura de plugins.
- Interfaces para múltiples proveedores.
- Jerarquías de clases.
- Contenedores de inyección.
- Un sistema genérico de pipelines.

Introducir abstracciones cuando exista una necesidad concreta.

### D. Dependencias externas en límites identificables

Encapsular llamadas a FFmpeg, OpenCV y modelos en funciones identificables.

Mantener la lógica puramente numérica o de validación separada cuando
resulte sencillo.

No exigir que toda la lógica de visión sea independiente de OpenCV:
sería una abstracción innecesaria para esta PoC.

### E. Configuración explícita

No ocultar dentro del código:
- Ruta del clip.
- Intervalo de análisis.
- Dimensiones de cancha.
- Calibración.
- Asignaciones de identidad.
- Parámetros que afecten el experimento.

Utilizar argumentos o archivos de configuración simples.

Evitar rutas absolutas de la computadora del usuario en archivos
versionados.

### F. Tiempo y coordenadas trazables

- Tiempo de la jugada: segundos desde el inicio del intervalo analizado.
- Conservar su correspondencia con el tiempo del archivo original.
- Inspeccionar los timestamps disponibles.
- No asumir que dividir el índice de frame por un FPS nominal siempre
  representa correctamente el tiempo.

Para imágenes utilizadas en calibración:
- Registrar tamaño y orientación.
- Registrar cualquier recorte o redimensionamiento.
- Mantener consistente ese sistema de coordenadas durante la proyección.
- No tomar la resolución de una captura de pantalla como resolución
  del MP4.

Coordenadas de cancha:
- Metros.
- Origen central.
- x a lo largo.
- z a lo ancho.
- Orientación documentada al calibrar.

### G. Originales y resultados separados

- No sobrescribir el MP4 original.
- No sobrescribir resultados de una ejecución anterior por defecto.
- Cada ejecución genera una carpeta identificable.
- Registrar entrada, configuración, versiones y comando utilizado.
- Identificar el archivo de entrada mediante un hash cuando se prepare E0.

No cargar todo el video en memoria si puede procesarse progresivamente.

### H. Datos intermedios distintos del contrato del visor

Los resultados del procesamiento no tienen que adoptar desde el inicio
la estructura Play del front.

Conservar la información necesaria para evaluar:
- Tracks.
- Identidades asignadas.
- Tiempos.
- Posiciones.
- Ausencias.
- Procedencia de los datos.

El formato concreto se define cuando cada etapa lo necesita.
La adaptación al visor se resuelve en E4.

### I. Tests y experimentos distintos

Tests unitarios:
- Lógica determinista.
- Validaciones.
- Casos de borde.
- Sin necesitar el video privado del usuario.

Tests de integración:
- Interacción real con archivos o herramientas externas.
- Entradas pequeñas, preferentemente sintéticas.
- Prerrequisitos explícitos.

Experimento con el clip:
- Ejecución real.
- Artefactos de diagnóstico.
- Revisión humana de fidelidad y utilidad.

Un mock de un detector no demuestra calidad de detección.
Un test de esquema JSON no demuestra fidelidad táctica.

### J. Errores y bloqueos visibles

- Informar entrada inválida, herramienta ausente o fallo de procesamiento.
- No continuar silenciosamente con resultados incompletos.
- No presentar falta de datos como coordenadas cero.
- No ocultar un cambio de dispositivo de inferencia.
- No declarar validado algo que no se ejecutó.

### K. Documentación y aprobación

Los documentos de experiments/ describen el trabajo de cada etapa.
context/plan.md registra su aprobación.

05-results.md informa:
- Qué se implementó.
- Qué se ejecutó.
- Dónde está la evidencia.
- Qué falló.
- Qué requiere revisión.
- Qué recomienda hacer después.

Solo el usuario aprueba continuar.
La IA no completa esa aprobación por cuenta propia.

---

## 4. Reglas de pertenencia

- Código ejecutable y reutilizable: src/jugadas_video/.
- Tests unitarios: junto al módulo.
- Contexto global: context/.
- Narrativa, review y evaluación de una etapa: experiments/<etapa>/.
- Configuración y anotaciones del experimento: experiments/<etapa>/.
- Medios originales privados: data/local/.
- Resultados regenerables: artifacts/.

No crear docs/ en la raíz.

---

## 5. Control de alcance inicial

Para E0:
- Preparar el entorno.
- Inspeccionar el MP4.
- Extraer referencias.
- Registrar tiempos y limitaciones.
- Entregar evidencia.

No implementar todavía:
- Calibración.
- Detector.
- Tracker.
- Exportación final.
- Cambios en el visor.

Detenerse en el Pause Point de E0.
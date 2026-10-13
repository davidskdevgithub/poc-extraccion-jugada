# Stack — PoC extracción de jugadas desde video

## Estado

Base técnica propuesta — Octubre 2026.

Entorno del usuario identificado.
Instalación de dependencias y ejecución pendientes.

Las herramientas se incorporan progresivamente según la etapa.
No instalar todo el stack antes de empezar.

---

## 1. Entorno de ejecución

- Equipo: MacBook Pro con Apple M1 Pro.
- Arquitectura: arm64.
- RAM: 16 GiB unificada.
- Sistema: macOS 15.6.1.
- Kernel: Darwin 24.6.0.
- Python global informado: 3.14.7.
- Repositorio existente con README y carpeta context.

La ejecución inicial será local, sin requisito de tiempo real.

No se presupone un tiempo de procesamiento ni una calidad de extracción
hasta ejecutar los experimentos.

---

## 2. Base para E0

### Python

- Versión inicial del proyecto: Python 3.12.
- Elección conservadora de compatibilidad.
- No implica que Python 3.14 sea incompatible.
- No reemplazar ni modificar el Python global del usuario.
- Registrar la versión exacta utilizada al preparar el entorno.

### Entorno y dependencias

- Administrador: uv.
- Entorno virtual local: .venv.
- Configuración del proyecto: pyproject.toml.
- Selección de Python: .python-version.
- Dependencias resueltas: uv.lock.
- Versionar pyproject.toml, .python-version y uv.lock.
- No editar manualmente uv.lock.

La PoC utilizará inicialmente la rama 3.12 de Python. El requisito del
proyecto y la selección del intérprete deben ser consistentes con ella.

### Inspección y extracción de imágenes

- Herramientas externas: FFmpeg y ffprobe.
- Instalación prevista en macOS: Homebrew.
- ffprobe: inspección del archivo, streams y tiempos.
- FFmpeg: extracción de imágenes y generación de videos auxiliares.
- Invocación desde Python mediante subprocess.

FFmpeg no es una dependencia Python administrada por uv.
Su versión debe registrarse por separado.

### Testing

- pytest.
- Tests de comportamiento para lógica y validaciones.
- Pruebas de integración pequeñas cuando intervengan archivos o FFmpeg.
- La ejecución con el clip real se registra como experimento separado.

### Linting y formato

- Ruff.
- Configuración en pyproject.toml.
- Longitud objetivo: 80 caracteres.
- Empezar con reglas básicas y orden de imports.
- No agregar un conjunto exhaustivo de reglas antes de necesitarlo.

---

## 3. Incorporación prevista para E1

### Imágenes y calibración

- NumPy: operaciones numéricas y coordenadas.
- OpenCV: operaciones de imagen y transformación al plano de cancha.

Estas dependencias se incorporan al preparar E1, no para inspeccionar
metadatos en E0.

La forma de ingresar puntos manuales se resolverá en la narrativa de E1.
No se presupone una aplicación web ni una interfaz completa.

---

## 4. Candidatos para E2

### Inferencia

- PyTorch como candidato para ejecutar modelos preentrenados.
- CPU como ruta de referencia.
- MPS como candidato de aceleración en Apple Silicon.

Antes de usar MPS:
- Comprobar disponibilidad en el entorno instalado.
- Ejecutar una inferencia real con el modelo seleccionado.
- Revisar compatibilidad, tiempo y consumo de memoria.
- Registrar el dispositivo utilizado.

No incorporar Core ML inicialmente.

### Detección y seguimiento

Detector, pesos y tracker pendientes de selección concreta.

La recomendación deberá considerar:
- Jugadoras pequeñas y desenfoque del clip.
- Cruces y oclusiones.
- Requisitos de instalación.
- Compatibilidad con el entorno.
- Licencias del código y de los pesos.
- Facilidad para producir datos y video de diagnóstico.

Nombres mencionados durante conversaciones no constituyen decisiones
de stack.

No incorporar varias alternativas por defecto. Elegir un primer enfoque
y evaluar qué falla antes de sumar complejidad.

---

## 5. Datos y resultados

- Archivos locales como entrada y salida.
- JSON para configuración, anotaciones y resultados estructurados
  cuando sea suficiente.
- Imágenes y videos para evidencia visual.
- Markdown para protocolos, decisiones e informes.
- Sin base de datos.

El contrato final de exportación al visor se acordará en E4.

No utilizar el contrato actual del front como excusa para inventar
posiciones, dorsales o pelota.

---

## 6. Fuera del stack inicial

- API web.
- Autenticación.
- Base de datos.
- Docker.
- Servicios de inferencia pagos.
- Entrenamiento de modelos propios.
- Core ML.
- Tracking automático de pelota.
- Herramienta completa de corrección.

Podrán evaluarse después, si la evidencia justifica incorporarlos.

---

## 7. Gestión de versiones y licencias

- Instalar versiones estables compatibles, no prereleases por defecto.
- Registrar versiones concretas en el lockfile y en cada ejecución.
- No actualizar dependencias durante un experimento sin registrar el cambio.
- Verificar licencias antes de incorporar código, modelos o pesos.
- Registrar origen y versión de los pesos utilizados.
- No considerar "abierto" como sinónimo de ausencia de condiciones de uso.

---

## 8. Referencias técnicas

- uv: https://docs.astral.sh/uv/guides/projects/
- FFprobe: https://ffmpeg.org/ffprobe.html
- PyTorch MPS: https://docs.pytorch.org/docs/stable/notes/mps.md
- pytest: https://docs.pytest.org/
- Ruff: https://docs.astral.sh/ruff/
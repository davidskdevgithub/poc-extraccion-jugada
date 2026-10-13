# Narrativa — E0: preparar el caso de prueba

## Propósito

Preparar el clip y sus referencias para comenzar los experimentos de
extracción.

Esta etapa no reconstruye la jugada. Debe producir información verificable
sobre el archivo, imágenes de referencia y una descripción de las
limitaciones que pueden afectar los experimentos siguientes.

El entregable es un caso de prueba documentado, no un sistema de detección.

---

## 1. Contexto conocido

### Video

- Archivo disponible localmente en formato MP4.
- Duración aproximada informada: 12 segundos.
- Intervalo de interés: desde el inicio hasta el segundo 8.
- Cámara fija, según información del usuario.
- Jugada a cierta distancia de la cámara.
- Ruta y nombre del archivo: identificar en el repositorio o consultar
  al usuario si todavía no está incorporado.

Conservar el MP4 original sin modificarlo.

### Cancha y participantes

- Cancha de 50 m de largo × 35 m de ancho.
- Equipo propio: camisetas oscuras.
- Equipo rival: camisetas claras.
- Árbitro: camiseta amarilla; no es una jugadora.
- Hay personas en una cancha contigua que no pertenecen a la jugada.
- Arco propio: cercano, abajo a la derecha en las capturas.
- Arco rival: al fondo, arriba a la izquierda.

Existe una captura anotada por el usuario:
- Rojo: identificación de los límites de la cancha.
- Azul: identificación de ambos arcos.

Los trazos sirven como contexto, no como coordenadas precisas de
calibración.

Las capturas pueden tener márgenes o dimensiones diferentes del video.
No trasladar sus coordenadas directamente al MP4.

### Situación descrita por el usuario

1. Sacamos desde el lateral cerca de nuestro arco.
2. La pelota llega a una defensora.
3. Su siguiente pase es interceptado.
4. Una rival llega libre por el medio.
5. Recibe un pase y convierte.

Esta secuencia proviene de la descripción del usuario. Sus tiempos
exactos todavía no están registrados.

### Pregunta táctica

¿La reconstrucción permitirá entender cómo la pérdida termina en una
oportunidad para una rival que llega libre por el medio?

Interesan especialmente:
- Las posiciones en la salida.
- Los movimientos alrededor de la pérdida.
- La trayectoria de la rival que llega libre.
- Su relación espacial con defensoras y arquera.

---

## 2. Trabajo incluido

### A. Preparar el entorno mínimo

Seguir context/stack.md y context/architecture.md.

Preparar únicamente lo necesario para E0:
- Python del proyecto mediante uv.
- Configuración y lockfile.
- Herramientas de testing y formato.
- Acceso a FFmpeg y ffprobe.

Comprobar qué está instalado antes de instalar.

No modificar el Python global del usuario.
No instalar todavía OpenCV, modelos, PyTorch ni trackers.

Si hace falta instalar una herramienta del sistema, informar el cambio y
solicitar autorización antes de ejecutarlo.

### B. Inspeccionar el archivo

Obtener y registrar:
- Identificación del archivo mediante hash.
- Duración reportada.
- Resolución codificada.
- Rotación u otra información que afecte su visualización, si existe.
- Codec del stream de video.
- Información disponible sobre FPS y base temporal.
- Características temporales relevantes del intervalo 0–8 s.

Conservar la salida original de ffprobe y generar un resumen legible.

No inferir que el video tiene tiempos uniformes únicamente porque informe
un FPS nominal. Si no se puede determinar algo, dejarlo explícito.

La inspección de metadatos puede abarcar el archivo original completo.
Las imágenes de evaluación deben corresponder al intervalo de interés.

### C. Extraer referencias del video original

Extraer un conjunto pequeño de imágenes que permita revisar:
- Encuadre y zona visible.
- Líneas e intersecciones candidatas para calibración.
- Tamaño aparente de las jugadoras.
- Desenfoque, cruces y posibles oclusiones.
- Presencia de personas ajenas a la jugada.

La IA puede elegir un muestreo inicial sencillo dentro de 0–8 s.

Registrar para cada imagen:
- Tiempo solicitado.
- Timestamp real del frame extraído.
- Dimensiones.
- Cualquier transformación aplicada.

Preferir imágenes a resolución original para las referencias.
Las versiones reducidas pueden generarse como auxiliares y deben quedar
identificadas como tales.

No inventar un frame exactamente en t=8 si ese timestamp no existe.

### D. Preparar la revisión de acontecimientos

Crear una tabla para estos cuatro momentos:
- Inicio o salida.
- Pase errado / intercepción.
- Pase al medio a la rival libre.
- Finalización / gol.

La tabla debe registrar:
- Acontecimiento.
- Tiempo en el video, cuando se conozca.
- Imagen de referencia.
- Origen de la identificación.
- Estado: propuesto o confirmado por el usuario.

La IA puede proponer tiempos si realmente revisa la secuencia y dispone
de evidencia suficiente.

Si no puede determinar un acontecimiento, dejarlo pendiente y facilitar
la revisión del usuario. No identificarlo por el nombre de una captura.

### E. Documentar observaciones y limitaciones

Distinguir:
- Información proporcionada por el usuario.
- Observaciones realizadas sobre los artefactos.
- Hipótesis pendientes.

En particular:
- La coincidencia de unas capturas no demuestra estabilidad durante todo
  el intervalo.
- La existencia de líneas visibles no demuestra una calibración viable.
- Una captura no demuestra calidad de seguimiento.

Identificar referencias candidatas sobre el suelo, sin calcular todavía
la transformación a coordenadas de cancha.

### F. Incorporar la revisión del contrato del visor

La revisión inicial ya se hizo con scene-types.ts y play-mock.ts.

Registrar sus conclusiones sin volver a diseñar el contrato:
- Convenciones de metros, tiempo e identidad aprovechables.
- Diferencia entre cancha de 50 × 30 m y cancha real de 50 × 35 m.
- Keyframes documentados como completos.
- Pelota obligatoria.
- Ausencia de procedencia explícita de las posiciones.
- Número de jugadora obligatorio, aunque los dorsales pueden desconocerse.

La resolución de estas diferencias corresponde a E4.

---

## 3. Decisiones delegadas a la IA

Dentro de las convenciones existentes, la IA puede resolver:
- Organización interna mínima del código.
- Invocación y lectura de resultados de FFmpeg/ffprobe.
- Muestreo inicial de imágenes.
- Identificadores de ejecución.
- Estructura sencilla de metadatos y referencias.
- Tests apropiados para el comportamiento implementado.

Debe documentar las decisiones relevantes.

Consultar al usuario cuando:
- Falte una entrada necesaria.
- Exista una ambigüedad de producto.
- Se requiera una instalación del sistema.
- Se proponga ampliar el alcance.

No consultar cada detalle técnico reversible.

---

## 4. Entregables

### Artefactos de ejecución

Dentro de artifacts/e0/<run-id>/:
- Metadatos originales.
- Resumen estructurado del archivo.
- Imágenes de referencia.
- Índice de imágenes y tiempos.
- Registro de entrada, configuración, versiones y ejecución.

### Informe

En experiments/e0-preparar-caso/05-results.md:
- Qué se implementó y ejecutó.
- Dónde están los artefactos.
- Observaciones y limitaciones.
- Tabla de acontecimientos.
- Referencias candidatas para calibración.
- Trabajo manual realizado.
- Bloqueos y preguntas pendientes.
- Recomendación para el siguiente paso.

El informe no debe declarar aprobación humana.

---

## 5. Pruebas y evaluación

Verificar mediante tests, según corresponda:
- Validación del intervalo solicitado.
- Lectura y normalización de metadatos.
- Manejo de herramientas ausentes y archivos inválidos.
- Registro de timestamps y transformaciones.
- Protección del original y de ejecuciones anteriores.

Las pruebas no deben depender del MP4 privado del usuario.

Ejecutar además la inspección y extracción con el clip real.

La evaluación visual y la confirmación de acontecimientos requieren
revisión humana. No presentar tests exitosos como prueba de viabilidad
de calibración o tracking.

---

## 6. Fuera de alcance

- Calibración efectiva.
- Detección y seguimiento.
- Asignación de identidades a tracks.
- Proyección de posiciones.
- Carga de pelota.
- Exportación final para el visor.
- Modificaciones del front.
- Interfaz web.
- Evaluación completa de fidelidad táctica.

---

## 7. Pause Point

Detenerse después de entregar los artefactos y el informe.

El usuario revisará:
- Si el caso está correctamente identificado.
- Si las referencias son utilizables.
- Qué acontecimientos y tiempos puede confirmar.
- Qué limitaciones acepta para continuar.

No comenzar E1 sin aprobación registrada en context/plan.md.

Si hay pendientes, distinguir cuáles bloquean E1 y cuáles pueden
resolverse más adelante. No exigir que toda incertidumbre desaparezca
para terminar E0.
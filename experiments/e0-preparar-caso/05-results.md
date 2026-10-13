# Resultados — E0: preparar el caso de prueba

**Fecha:** 2026-10-13
**Run de ejecución:** `artifacts/e0/20261013-155147`
**Estado:** cierre de ejecución completo; Pendiente Point de revisión humana pendiente. Ningún resultado aquí constituye aprobación humana ni validación experimental.

---

## 1. Qué se implementó y ejecutó (UC-08)

### Implementación

- Entorno mínimo de E0: Python 3.12 del proyecto gestionado con uv (`pyproject.toml`, `.python-version`, `uv.lock`), pytest y Ruff configurados, acceso a ffmpeg/ffprobe verificado. Python global sin modificar. Sin NumPy, OpenCV, PyTorch, modelos ni trackers — UC-01.
- Código bajo `src/jugadas_video/`: validación de entradas (UC-E7, UC-E2), inspección de metadatos con ffprobe encapsulado (UC-02), extracción de referencias con ffmpeg encapsulado y selección determinista documentada (UC-03, UC-E3, UC-E4), gestión de ejecuciones con run-id, índice de imágenes y registro (UC-04, UC-E6).
- Tests: 90 tests pasando (`pytest -q`), incluyendo casos de borde de intervalo, metadata indeterminada, herramienta externa ausente, archivo inválido y protección del original y de ejecuciones previas. Ruff sin errores.

### Ejecución con el clip real (UC-G1 → UC-02/03/04)

- Comprobación de medios en `data/local/`: los 6 archivos esperados están presentes (MP4 + 4 capturas + captura anotada); hash SHA-256 del MP4 registrado; medios intactos durante E0 — UC-G1, UC-E5.
- Ejecución identificada `artifacts/e0/20261013-155147`, con comando y versiones (python 3.12.15, ffmpeg 9.0.2, ffprobe 9.0.2, uv 0.12.24) registrados en `registro.json`.
- Corrección registrada durante la ejecución: una corrida previa (`20261013-155057`) quedó con un registro defectuoso (bandera `--version` mal invocada para uv y comando registrado sin `python -m`); se corrigió y re-ejecutó sin modificar corridas previas. Ambas corridas permanecen conservadas.

### Resultado de la inspección (UC-02)

- Duración reportada: 12.0 s. Codec h264. Resolución codificada 1370×922. Rotación: no aplica. FPS nominal 25.0, time base 1/12800.
- Intervalo 0–8 s: 201 frames, fps efectivo 25.0, sin evidencia de fps variable, timestamps reales de 0.000 a 8.000 s. Sin metadatos indeterminados en lo registrado.

### Resultado de la extracción (UC-03)

- 24 imágenes de referencia: 12 frames a resolución original (1370×922) + 12 versiones reducidas (1280×861, identificadas como auxiliares en el índice).
- Muestreo determinista documentado: `t_i = start + i * (end - start) / count`, incluye inicio y excluye fin; separación efectiva ~0.667 s. Por diseño no hay referencia en t=8.0 exacto (ver Limitaciones).
- Para cada imagen: tiempo solicitado, timestamp real (p. ej. solicitado 0.667 → real 0.680), dimensiones y transformaciones registradas en `indice_imagenes.json`.

---

## 2. Ubicación de artefactos (UC-04)

Todo en `artifacts/e0/20261013-155147/`:

| Artefacto | Archivo |
|---|---|
| Salida original de ffprobe | `ffprobe_salida_original.json` |
| Resumen estructurado | `resumen_inspeccion.json` |
| Características temporales 0–8 s | `resumen_temporal.json` |
| Imágenes de referencia (original + reducidas) | `imagenes/` (24 archivos) |
| Índice de imágenes y tiempos | `indice_imagenes.json` |
| Registro de entrada/config/versiones/comando | `registro.json` |

Hash del MP4 original (`data/local/gol-del-rival.mp4`): `95f8c9204ccb515fce16399aacfab14e87c9204003e81f2c9014f6c823032e0f`. El original y las corridas previas permanecen intactos.

---

## 3. Tabla de acontecimientos propuesta (UC-05, PE-02)

El muestreo de referencias es cada ~0.667 s; los instantes exactos caen en general entre frames, con incertidumbre del orden de ±0.35 s. Todos los estados quedan **propuesto**; la confirmación es exclusivamente humana (Pause Point).

| Nº | Acontecimiento | Tiempo propuesto | Imagen de referencia | Origen | Estado |
|----|----------------|-----------------|----------------------|--------|--------|
| 1 | Inicio / salida (saque desde el lateral cerca del arco propio) | ≈ 0.7 s (rango 0.0–1.3) | `frame_t_0.680.png` (con `frame_t_0.000.png` como estado previo) | [video] cronología de frames + [usuario] descripción del saque lateral | propuesto — confianza baja: el instante del saque no es claramente visible; a t=1.32 el juego ya avanzó |
| 2 | Intercepción (pase malo de la defensora) | ≈ 3.7 s (entre 3.32 y 4.00) | `frame_t_3.320.png`, `frame_t_4.000.png` | [video] pelota naranja en duelo junto al lateral derecho en 3.32, cambio de posesión hacia 4.00; [usuario] describe la intercepción | propuesto — confianza media |
| 3 | Pase a la rival libre por el medio | ≈ 5.3 s (rango 5.0–5.7) | `frame_t_5.320.png` (y `frame_t_6.000.png` con la receptora avanzando) | [video] jugadora clara en plena carrera por el carril central; coincide con la captura 03 del usuario | propuesto — confianza media |
| 4 | Gol (rival, en el arco propio, abajo-derecha) | ≈ 6.8 s (rango 6.7–7.0) | `frame_t_6.680.png`, `frame_t_7.320.png` | [video] en 6.68 figura caída en el área propia y pelota junto a la red; en 7.32 la pelota está dentro del arco; [usuario] describe el gol | propuesto — confianza media-alta |

Observaciones que sostienen la tabla:
- La pelota es naranja/rojiza y distinguible en la mayoría de los frames desde t=3.32; en t=0.00–1.32 no se identifica con claridad, lo que degrada la confianza del acontecimiento 1. **[video]**
- La dirección del ataque (rival de camisetas claras hacia el arco cercano abajo-derecha) es coherente con la anotación de `limites.png`. **[usuario]** + **[video]**
- Las figuras caídas cerca del arco en 6.68/7.32 son hipotéticamente la arquera o una defensora propia. **[hipótesis]**

---

## 4. PE-01 — Utilizabilidad de las referencias (UC-06)

Método realizado: revisión visual de los 12 frames reducidos del intervalo y de las 5 capturas de `data/local/`, contrastadas con `limites.png`. Resultado: **favorable con reservas** — las referencias sirven para E0 y para preparar E1, con las limitaciones listadas en §6.

### Encuadre y calidad

- Punto de vista idéntico en los 12 frames muestreados: los objetos de fondo (arcos de la cancha contigua, carteles, torres de luz, vallas) permanecen en la misma posición de píxel; sin paneo, zoom ni vibración apreciables. **[video]** Con muestreo cada ~0.67 s no se demuestra estabilidad continua; un movimiento breve de cámara entre frames podría pasar inadvertido. **[hipótesis]**
- Escena nocturna con iluminación artificial: halos/blooming en las luces, subexposición en la franja inferior y el borde derecho, ruido moderado en zonas oscuras, blur de movimiento/compresión h264 en jugadoras en carrera (notable en t=5.32). **[video]**
- Resolución 1370×922: jugadoras de ~15–25 px en primer plano y ~10–15 px al fondo; suficiente para revisión visual e identificación de intersecciones de líneas; dorsales ilegibles a esta escala. **[video]**
- Marca de agua "Beelup" centrada abajo, superpuesta a la zona donde correría la línea de fondo inferior; puede interferir con la detección de esa línea. **[video]**
- Personas ajenas a la jugada: abundantes (cancha contigua arriba-izquierda; espectadores tras la valla a la derecha). Coincide con lo descrito por el usuario. **[video]**

### Visibilidad de líneas (candidatas para calibración, sin calcular transformación)

- Líneas nítidas y de buen contraste: los dos cuadriláteros de área, la línea de mediocampo (curva) y el lateral superior. Zonas degradadas por sombra: línea de fondo inferior y rincón inferior-derecho (además de la marca de agua). **[video]**
- Intersecciones candidatas sobre el suelo: esquinas de los dos rectángulos de área, unión de área con línea lateral, arco del círculo central, esquinas del lateral superior. Las líneas del fondo inferior/derecho son las más débiles. **[hipótesis]**
- La existencia de líneas visibles no demuestra una calibración viable: falta evaluar distorsión de lente y correspondencia con el modelo de cancha 50×35 m. **[hipótesis]**

### Contraste con la captura anotada

- `limites.png` es un screenshot de la misma cámara (mismo punto de vista y marca de agua) con resolución mayor (3024×1964) y letterboxing; márgenes y dimensiones no coinciden con el video → no trasladar coordenadas. **[video]** (dato del archivo) / **[usuario]** (que sea la referencia de encuadre)
- El trazo rojo sigue el perímetro de la cancha central iluminada; el azul marca ambos arcos. Los arcos del trazo azul coinciden en posición con los arcos visibles en los frames. **[usuario]** (trazo) + **[video]** (coincidencia)
- El tramo rojo inferior atraviesa la franja en sombra donde el video no muestra línea nítida: contexto válido, pero ese tramo no tiene respaldo de línea visible en los frames. **[usuario]** el trazo / **[hipótesis]** que corresponde a la línea de fondo

---

## 5. Contraste capturas del usuario vs. video (UC-E5, documental)

La cronología implícita en las capturas del usuario es consistente con la cronología de los frames; sin contradicciones graves:

- `01-inicio.png`: posiciones casi idénticas a t=0.00–0.68 → el "inicio" cae dentro del primer segundo. Sin contradicción.
- `02-pase-malo.png`: compatible con la ventana t≈3.3–4.7, sin coincidencia exacta con un frame muestreado (instante entre frames). Sin ancla exacta.
- `03-rival-libre.png`: muy similar a `frame_t_5.320.png`. Coherente con ≈5.3 s.
- `04-rival-gol.png`: compatible con la ventana t≈6.7–7.3. Coherente con ≈6.8 s.

Aclaración sobre una aparente discrepancia: `resumen_temporal.json` declara `ultimo_frame_s: 8.0` (último frame del video dentro del intervalo), pero la última referencia extraída es t=7.32 porque la regla de muestreo excluye el extremo final por diseño, y la narrativa prohíbe inventar un frame en t=8. Si el final exacto del intervalo fuera necesario como referencia, habría que extraerlo explícitamente (ver Limitaciones).

---

## 6. Limitaciones

1. **Instantes exactos entre frames:** con muestreo cada ~0.667 s, ningún acontecimiento queda fijado con precisión mayor a ±0.35 s. Precisar requeriría frames adicionales alrededor de t≈0.5–1.3 (saque), 3.3–4.0 (intercepción), 5.0–5.7 (pase al medio) y 6.6–7.3 (gol).
2. **Acontecimiento 1 con confianza baja:** el momento del saque no es claramente visible y la pelota no se distingue en los frames iniciales.
3. **Identidades y roles:** dorsales ilegibles; la atribución de las figuras caídas cerca del arco (arquera/defensora) es hipótesis.
4. **Estabilidad del encuadre:** verificada solo en muestreo discreto, no de forma continua.
5. **Calibración:** intersecciones candidatas identificadas, sin evaluar distorsión de lente ni correspondencia con la cancha 50×35 m; líneas del fondo inferior/derecha débiles (sombra + marca de agua "Beelup").
6. **Referencia en t=8.0:** no extraída (regla de muestreo excluye el extremo). Resoluble después si se necesita.
7. **Tiempos de la tabla:** todos quedan propuestos, pendientes de confirmación humana en el Pause Point.

---

## 7. Contrato del visor (UC-07) — transcripción de la revisión inicial

Revisión ya realizada con `scene-types.ts` y `play-mock.ts`; se registran las conclusiones sin volver a diseñar el contrato:

- Convenciones de metros, tiempo e identidad aprovechables para la extracción.
- Diferencia entre la cancha del contrato (50 × 30 m) y la cancha real del caso (50 × 35 m).
- Keyframes documentados como completos.
- Pelota obligatoria en el contrato.
- Ausencia de procedencia explícita de las posiciones.
- Número de jugadora obligatorio, aunque los dorsales pueden desconocerse (coherente con la ilegibilidad de dorsales en el video).

La resolución de estas diferencias corresponde a E4, no a E0.

---

## 8. Trabajo manual

| Actividad | Tiempo | Modalidad |
|---|---|---|
| Análisis y plan de implementación (sesión previa) | ~45 min | estimado |
| Implementación + tests + ejecución con el clip real (corrida 155057 + corrección del registro + corrida 155147) | ~35 min | estimado |
| Revisión visual PE-01/PE-02 (subagente, delegación asíncrona) | ~10 min de supervisión | estimado |
| Redacción del informe y cierre | ~15 min | estimado |

Todo el tiempo es estimado por el agente; no hay medición objetiva de sesiones.

---

## 9. Recomendación del siguiente paso

1. **Pause Point (humano):** confirmar o corregir los cuatro tiempos propuestos de la tabla (§3), aceptar la utilizabilidad de las referencias (§4) y las limitaciones aceptadas para continuar (§6). Registrar la decisión en `context/plan.md`.
2. **E1 (calibración):** puede iniciarse después del Pause Point. Requerirá instalar OpenCV/NumPy (autorización según workflow) y abordar la distorsión de lente y la correspondencia con el modelo 50×35 m. Las líneas del fondo inferior/derecha débiles son el principal riesgo conocido; las intersecciones candidatas de las áreas y del lateral superior son más sólidas.
3. **No bloquea E1** (resolubles después): extraer una referencia explícita en t=8.0; añadir frames de precisión alrededor de los cuatro acontecimientos si la calibración o la detección los demandan; evaluar la interferencia de la marca de agua en la detección de la línea de fondo.
4. **Bloquea E1** hasta resolver: instalación autorizada de OpenCV/NumPy; decisión sobre la estrategia de calibración (qué intersecciones usar) sujeta a la revisión humana de PE-01.

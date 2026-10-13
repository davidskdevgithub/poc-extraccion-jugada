# Review: scene 01-narrative

## Resumen (10 segundos)
- **Qué describe:** feature base — contrato de datos de la jugada (`Play`, `Keyframe`) + render estático de la escena (cancha, 8 vs 8, pelota) en t=0
- **Estado:** completa — 6 gaps identificados, todos resueltos

## Definido por el usuario ✅
- Modelo: 8 vs 8 con arquera, keyframes completos, interpolación lineal
- Unidades en metros, origen en el centro, x largo / z ancho / y arriba
- Cancha fútbol 8 ~50×30 m, estática y decorativa, líneas planas simplificadas (perímetro, línea media, círculo central, áreas, puntos penal)
- Jugadoras: cilindros bajos de altura fija, color por equipo; número encima
- Pelota: esfera blanca, altura (y) interpolada igual que x/z
- Fuera de scope: playback controls, cámara, timeline-ui, edición
- Entregable E2E: escena estática en t=0 (consistente con Decisión F)

## Inferido por la IA ⚡
- Estructura según módulo patrón: `scene-types.ts`, `data/play-mock.ts`, `components/` (field, players, ball, scene), `utils/interpolate.ts` con `getPositionsAtTime(play, t)` (Decisión C/G)
- Límites de interpolación: clamp al primer/último keyframe fuera de rango
- Números sobre cilindros: `<Text>` de drei billboardeado a la cámara
- Iluminación estándar (ambient + direccional)
- El mock resuelve los pendientes del glosario: rivales (dos equipos) y altura de pelota (sí, interpolada)

## Gaps a resolver ❓

### 1. Identidad de jugadoras: ¿dónde viven id/equipo/número?
**Qué falta:** "Cada keyframe incluye a todas las jugadoras" admitía dos contratos.
**Por qué importa:** es el contrato que consumen playback, camera y timeline-ui.
**Opciones:** identidad en `Play` vs keyframes autocontenidos.
**Sugerencia:** identidad en `Play`, keyframes solo posiciones.
**Respuesta:** Identidad en `Play` (lista de jugadoras con id/equipo/número); cada keyframe guarda posiciones por id + pelota.

### 2. El store de playback no existe todavía
**Qué falta:** la narrativa refería al store de `playback/`, feature inexistente al momento.
**Por qué importa:** sin store no hay de dónde leer `currentTime` congelado en 0.
**Opciones:** store mínimo ahora vs constante local en scene.
**Sugerencia:** store mínimo en `playback/`.
**Respuesta:** Store mínimo en `playback/`: `currentTime=0`, `playing=false`, sin acciones. Scene lo lee con `getState()` como dicta la Decisión D; playback lo extiende después.

### 3. Verde oscuro sobre verde oscuro
**Qué falta:** equipo propio en verde oscuro sobre cancha de plano verde oscuro — ilegible desde cenital.
**Por qué importa:** la legibilidad de posicionamiento es el objetivo de la PoC.
**Opciones:** aclarar cancha / cambiar color de equipo propio / dejar tal cual.
**Sugerencia:** aclarar la cancha (decorativa) y mantener el color de equipo (carga significado).
**Respuesta:** Aclarar la cancha (verde más claro / gris verdoso). Equipo propio queda verde oscuro, rivales en blanco.

### 4. ¿La arquera se distingue?
**Qué falta:** color "por equipo" no distinguía arqueras de jugadoras de campo.
**Opciones:** mismo color que su equipo vs color distinto.
**Sugerencia:** mismo color, el número 1 la identifica.
**Respuesta:** Mismo color que su equipo; el número 1 la marca.

### 5. Contenido de la jugada mock
**Qué falta:** duración, cantidad de keyframes y situación mostrada.
**Opciones:** la IA arma la jugada vs la define el usuario.
**Sugerencia:** progresión genérica suficiente para validar legibilidad.
**Respuesta:** La IA arma la jugada: progresión simple de ~12 s con 5–6 keyframes, ambos equipos moviéndose, pelota avanzando con altura variable.

### 6. Cámara inicial para ver la escena
**Qué falta:** camera/ fuera de scope, pero algo tenía que encuadrar la cancha para el E2E visual.
**Opciones:** pose por defecto en `App.tsx` vs default de R3F.
**Sugerencia:** prop `camera` del `<Canvas>` con vista tipo oblicua.
**Respuesta:** Pose por defecto en `App.tsx` vía prop `camera` del `<Canvas>` (vista tipo oblicua). Se reemplaza cuando exista camera/.

## Notas de implementación
- Contrato: `Play` lleva la identidad (id, equipo, número); keyframes solo posiciones por id + pelota
- Store mínimo de playback: lectura por `getState()` dentro de `useFrame` (Decisión D), nunca hook reactivo del render loop
- Paleta: cancha verde claro/gris verdoso, propias verde oscuro, rivales blanco, pelota blanca, arqueras mismo color de su equipo con número 1
- Mock: ~12 s, 5–6 keyframes, progresión con ambos equipos desplazados y pelota con altura variable
- Cámara inicial: prop `camera` del `<Canvas>` en `App.tsx`, reemplazable por camera/ sin tocar scene
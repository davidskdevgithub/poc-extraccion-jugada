# Casos de Uso: scene (contrato + escena estática)

**Narrativa fuente:** `src/features/scene/docs/01-narrative.md`
**Review fuente:** `src/features/scene/docs/01-narrative-review.md`
**Fecha:** 2026-10-07

---

## Happy Path

### UC-01: Escena completa estática en t=0 (entregable E2E)
**Dado** la app cargada con la jugada mock
**Cuando** se monta la escena leyendo `currentTime` = 0 del store de playback
**Entonces** se renderizan la cancha, las 16 jugadoras y la pelota en las posiciones del keyframe t=0 — sin interacción

### UC-02: Cancha de fútbol 8 con líneas simplificadas
**Dado** la escena montada
**Cuando** se observa la cancha
**Entonces** se ve un plano ~50×30 m (coordenadas en metros, origen en el centro) verde claro, con líneas planas: perímetro, línea media, círculo central, áreas y puntos penal — sin muros ni vallas

### UC-03: Jugadoras con color por equipo y número
**Dado** las 16 jugadoras renderizadas (8 propias, 8 rivales, arquera incluida en cada equipo)
**Cuando** se observan las entidades
**Entonces** cada jugadora es un cilindro bajo de altura fija: propias verde oscuro, rivales blancas, con el número de `Play` visible encima del cilindro

### UC-04: Pelota con posición 3D
**Dado** el keyframe t=0
**Cuando** se renderiza la pelota
**Entonces** es una esfera blanca posicionada en el (x, y, z) del keyframe — no clavada al piso si el keyframe tiene y > 0

### UC-05: Interpolación lineal entre keyframes consecutivos
**Dado** dos keyframes consecutivos (t=4 y t=6) donde una jugadora pasa de A a B y la pelota de P1 a P2 con distinta y
**Cuando** se consulta la posición en un instante intermedio (t=5)
**Entonces** cada entidad queda en el punto medio del segmento — jugadora y pelota, esta última con su y interpolada

### UC-06: Contrato de jugada consumible por las demás features
**Dado** el modelo implementado
**Cuando** playback, camera o timeline-ui necesitan el modelo de la jugada
**Entonces** consumen `scene-types` por el entry point oficial — identidad (id/equipo/número) en `Play`, sin duplicarla ni leer internals

### UC-07: El tiempo de la escena deriva del store de playback
**Dado** la escena montada
**Cuando** se renderiza la escena en cualquier momento de la sesión
**Entonces** el instante mostrado es siempre el `currentTime` del store de playback — scene no mantiene tiempo propio

### UC-08: Sesión sin interacción queda congelada en t=0
**Dado** la app abierta sin ninguna interacción (el store mínimo no tiene acciones)
**Cuando** transcurre el tiempo
**Entonces** `currentTime` permanece en 0 y la escena se mantiene estática en el keyframe t=0

## Edge Cases

### UC-E1: Instante fuera del rango de la jugada
**Dado** una jugada de duración D con keyframes desde t=0
**Cuando** se consulta la posición en t < 0 o t > D
**Entonces** se usa el keyframe más cercano (t<0 → primer keyframe, t>D → último) — sin error ni posiciones indefinidas

### UC-E2: Instante exactamente en un keyframe
**Dado** un keyframe en t=k
**Cuando** se consulta la posición en t=k
**Entonces** las posiciones son exactamente las del keyframe, sin aporte del vecino

### UC-E3: Pelota descendiendo al piso
**Dado** la pelota con y > 0 en un keyframe y y = 0 en el siguiente
**Cuando** se interpola entre ambos
**Entonces** la altura desciende linealmente hasta el piso — la y se trata igual que x y z

### UC-E4: Números legibles desde cualquier ángulo
**Dado** una jugadora observada desde cualquier ángulo de cámara
**Cuando** se mira su número
**Entonces** el número queda orientado hacia la cámara (billboard) y legible también desde la vista cenital

## Escenarios de gaps resueltos

### UC-G1: Identidad en Play, keyframes solo posiciones (gap 1)
**Dado** el modelo implementado
**Cuando** se inspecciona un keyframe
**Entonces** contiene solo `t`, posiciones por id de jugadora y la pelota — ningún keyframe repite id, equipo o número; eso vive una única vez en `Play`

### UC-G2: Store mínimo de playback creado en esta feature (gap 2)
**Dado** la feature implementada
**Cuando** la escena necesita el instante actual
**Entonces** lo lee del store mínimo de `playback/` (currentTime=0, playing=false, sin acciones) — no de una constante local ni de estado propio de scene

### UC-G3: Contraste resuelto aclarando la cancha (gap 3)
**Dado** la escena vista desde arriba
**Cuando** se observan las propias
**Entonces** se distinguen del plano: cancha verde claro/gris verdoso, propias verde oscuro, rivales blancas

### UC-G4: Arquera sin color distinto (gap 4)
**Dado** las dos arqueras renderizadas
**Cuando** se observan
**Entonces** llevan el mismo color que su equipo y el número 1 las identifica

### UC-G5: Jugada mock de ~12 s con ambos equipos desplazándose (gap 5)
**Dado** la jugada mock cargada
**Cuando** se inspecciona
**Entonces** dura ~12 s con 5–6 keyframes; entre keyframes ambos equipos se desplazan y la pelota avanza con altura variable — el mock resuelve los pendientes del glosario (rivales sí, altura de pelota sí)

### UC-G6: Encuadre por defecto desde App.tsx (gap 6)
**Dado** la app cargada sin ninguna interacción
**Cuando** se observa la pantalla
**Entonces** la pose de cámara por defecto (prop camera del Canvas en App.tsx) encuadra la cancha completa en vista tipo oblicua — verificable sin configurar nada, y reemplazable por camera/ sin tocar scene
**Superseded:** reemplazado por UC-01 de camera — el encuadre por defecto pasa a ser de la feature camera (cámara libre), la prop `camera` de App.tsx desaparece
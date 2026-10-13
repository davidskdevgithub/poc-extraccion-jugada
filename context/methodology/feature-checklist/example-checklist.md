# Checklist: scene (contrato + escena estática)

**Casos de uso fuente:** `src/features/scene/docs/03-use-cases.md`
**Review fuente:** `src/features/scene/docs/01-narrative-review.md`
**Fecha:** 2026-10-07

---

## Pendiente

(Ninguno — feature completa)

## Hecho

- [x] Verificación E2E en browser (Decisión F): escena estática en t=0 sin interacción, contraste verde/verde resuelto, cancha completa encuadrada — UC-01, UC-08, UC-G3, UC-G6

- [x] Contrato de la jugada en `scene-types.ts`: `Play` con identidad (id/equipo/número), `Keyframe` solo `t` + posiciones por id + pelota — UC-06, UC-G1
- [x] Jugada mock en `data/play-mock.ts`: ~12 s, 6 keyframes, 8v8 con arqueras, ambos equipos desplazándose, pelota con altura variable — UC-G5
- [x] Store mínimo de playback en `playback/`: `currentTime`=0, `playing`=false, sin acciones — UC-G2, UC-07, UC-08
- [x] Interpolación en `utils/interpolate.ts` (`getPositionsAtTime`): lineal entre keyframes, y de pelota interpolada, clamp fuera de rango — UC-05, UC-E1 a UC-E3
- [x] Tests de interpolación al lado del util: punto medio, keyframe exacto, clamp en ambos extremos, altura de pelota — UC-05, UC-E1 a UC-E3
- [x] Cancha fútbol 8: plano verde claro ~50×30 m, líneas planas (perímetro, media, círculo central, áreas, puntos penal), estática sin estado — UC-02, UC-G3
- [x] Jugadoras: cilindros bajos, color por equipo (propias verde oscuro, rivales blanco, arqueras color de su equipo con número 1) — UC-03, UC-G4
- [x] Números sobre cilindros billboardeados a cámara, legibles desde cenital — UC-E4
- [x] Pelota: esfera blanca en el (x, y, z) del keyframe — UC-04
- [x] Componente escena que compone cancha + jugadoras + pelota, leyendo el tiempo del store de playback con `getState()` dentro de `useFrame` (Decisión D) — UC-01, UC-07, UC-08
- [x] `App.tsx`: `<Canvas>` con pose de cámara por defecto tipo oblicua + escena montada — UC-01, UC-G6
- [x] Integridad del mock validada (16 ids completos por keyframe, t ascendente, dentro de los límites de la cancha, último keyframe = duración)
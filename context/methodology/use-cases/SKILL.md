---
name: use-cases
description: Genera casos de uso en formato "dado/cuando/entonces" a partir de una narrativa y sus respuestas de review. Cada escenario cubre un comportamiento específico de la feature. Use después de narrative-review para tener los escenarios antes de implementar.
---

# Use Cases

## Overview

Genera casos de uso en formato **"dado / cuando / entonces"** a partir de una narrativa y las respuestas del review. Cada escenario cubre un comportamiento específico que debe ser testeado.

**Flujo:**
```
Narrativa + review responses → casos de uso → guían implementación y tests
```

## When to Use

- Se completó `narrative-review` y se tienen las respuestas
- Se quiere tener los escenarios antes de implementar
- Se quiere verificar cobertura de tests contra comportamiento documentado
- NOT para: features que no tienen narrative-review completado

## Inputs

| Archivo | Rol |
|---|---|
| Narrativa del usuario | Comportamiento descrito |
| Review con respuestas | Decisiones tomadas |

## Core Process

1. **Leer narrativa + review**
   - Identificar cada regla de negocio
   - Identificar cada gap resuelto (la respuesta define el comportamiento)
   - Identificar edge cases de la narrativa

2. **Generar escenarios**
   - Por cada regla → al menos 1 escenario happy path
   - Por cada gap resuelto → 1 escenario que valide la decisión
   - Por cada edge case → 1 escenario de borde
   - Format: **Dado** [contexto] **Cuando** [acción] **Entonces** [resultado esperado]
   - Anotar la **superficie** de cada "Cuando": la UI que lo ejecutará (botón, drag, tecla) o la acción de store/servicio si la UI todavía no existe. La verificación E2E usa esta anotación como mapping; cuando llegue la UI, se actualiza

3. **Presentar al usuario**
   - Lista de escenarios para validar
   - El usuario confirma, agrega o elimina

4. **Guardar**
   - Guardar en `src/features/{feature}/docs/03-use-cases.md`

## Formato de Output

```markdown
# Casos de Uso: [Feature/Componente]

**Narrativa fuente:** [ruta]
**Review fuente:** [ruta]
**Fecha:** [fecha]

---

## Happy Path

### UC-01: [Nombre del escenario]
**Dado** [contexto inicial]
**Cuando** [acción del usuario o sistema]
**Entonces** [resultado esperado]
**Superficie** [UI: botón X / tecla / drag — o store: `acción()` si la UI aún no existe]

### UC-02: ...

## Edge Cases

### UC-E1: [Nombre del edge case]
**Dado** [contexto]
**Cuando** [situación borde]
**Entonces** [comportamiento esperado]
**Superficie** [UI o store — misma convención que UC-01]

## Escenarios de gaps resueltos

### UC-G1: [Nombre]
**Dado** [contexto del gap]
**Cuando** [situación]
**Entonces** [lo que se decidió en el review]
**Superficie** [UI o store — misma convención que UC-01]
```

## Features compuestas (composición con features previas)

Aplica cuando la feature **agrega superficie que interactúa con features ya implementadas** o **depende de su estado en ejecución** (ej: UI de timeline sobre un store de playback con trigger propio; cámara que sigue entidades que se mueven). Los bugs de composición viven en las costuras — ningún test por-feature los ve.

- Los UCs de composición viven en el **mismo** `03-use-cases.md` de la feature nueva, en una sección `## Composición con features previas` — no en la feature previa ni en una "feature de integración" aparte.
- Nombrarlos `UC-C1`, `UC-C2`…
- El **Dado describe el estado de ambas features** (ej: "Dado la jugada reproduciendo a mitad y el scrubber visible") y el **Entonces es el contrato combinado**.
- **Superficie obligatoria** (misma convención que UC-01): en composición casi siempre es UI nueva → acción de store de la feature previa; esa cadena explícita es el mapping de la verificación E2E.
- **Superseded:** si la feature nueva reemplaza un trigger/UI de una feature previa (ej: botones que reemplazan un trigger temporal), marcar en el doc de la previa: "superseded por UC-Cx de [feature]" — no borrar el UC: los docs de UCs son historia del guion y la marca evita que una sesión futura ejecute un UC que ya no aplica.
- La verificación E2E corre los UCs propios + los de composición en un solo guion y registra resultados en el checklist de la feature nueva; la feature previa no se re-verifica entera (queda cross-reference).

## Ejemplos de referencia

Los siguientes archivos contienen ejemplos reales de Reviews bien escritos. Usalos como guía de razonamiento, no como template:

- [example-uc-1.md](./example-uc-1.md) — Totales del Dashboard con Happy Path, Edge Cases y Gaps resueltos
- [example-uc-2.md](./example-uc-2.md) — timeline-ui compuesta sobre playback: sección "Composición con features previas", drag del scrubber, superseded del trigger temporal


## Reglas

1. **Un escenario = un comportamiento** — no meter múltiples assertions
2. **Formato consistente** — siempre Dado/Cuando/Entonces
3. **Sin código** — el escenario describe comportamiento, no implementación
4. **Cada gap resuelto tiene su escenario** — validar que la decisión se implementó
5. **Cada UC declara su superficie** — `Superficie` indica quién ejecuta el "Cuando" (UI o acción de store); la verificación E2E la usa como mapping y se actualiza cuando la UI reemplaza un trigger temporal
6. **Feature compuesta → sección de composición** — si la feature interactúa o depende de features previas, los UCs de costura van en `## Composición con features previas` del mismo doc (ver [example-uc-2.md](./example-uc-2.md))

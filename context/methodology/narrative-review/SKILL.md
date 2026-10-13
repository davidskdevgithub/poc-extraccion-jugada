---
name: narrative-review
description: Revisa narrativas de implementación para detectar gaps antes de que la IA implemente. Toma una narrativa escrita por un developer senior y identifica qué está bien definido, qué necesita resolverse, y qué falta. El output es una lista de gaps que el usuario responde rápido. Use cuando se tiene una narrativa lista y se quiere verificar que no falta nada antes de implementar.
---

# Narrative Review

## Overview

Revisa narrativas de implementación para detectar **gaps** antes de que la IA implemente. El developer senior escribe qué quiere construir como narrativa —esta skill identifica qué está bien definido, qué necesita resolverse, y qué falta.

**No genera contratos. No genera tareas. No genera código.** Solo genera gaps que el usuario responde rápido.

**Flujo:**
```
Narrativa → gaps identificados → usuario resuelve → listo para implementar
```

## When to Use

- Se tiene una narrativa escrita (componente, feature, flujo)
- Se quiere verificar que no falta nada antes de implementar
- Se quiere saber qué la IA puede inferir y qué necesita explícito
- NOT para: ideas vagas sin dirección (usar `idea-refine`)
- NOT para: implementar código directamente (usar `incremental-implementation`)

## Inputs

| Archivo | Rol | Si no existe |
|---|---|---|
| Narrativa del usuario | Fuente primaria | Pedir al usuario que escriba |
| `README.md` | Intro del proyecto | La skill interpreta en base a la información disponible |
| `context/architecture.md` | Convenciones del proyecto | La skill trabaja pero no puede verificar consistencia |
| `context/glosario.md` | Terminología de dominio | La skill usa términos de la narrativa |
| `context/stack.md` | Servicios disponibles | La skill referencia lo que encuentre |

## Core Process

### Fase 1: Cargar

1. **Leer la narrativa**
   - Identificar: qué describe (componente, flujo, feature)
   - Identificar: qué reglas de negocio menciona
   - Identificar: qué HTML de referencia incluye
   - Identificar: qué código o funciones ya incluye

2. **Leer contexto del proyecto**
   - `architecture.md` → convenciones, estructura
   - `glosario.md` → terminología
   - `stack.md` → servicios
   - Convenciones del repo → tokens, anti-patterns

### Fase 2: Clasificar

3. **Separar lo explícito de lo inferido**
   - **Definido por el usuario:** reglas de negocio explícitas, código incluido, HTML de referencia, decisiones técnicas documentadas
   - **Inferido por la IA:** ubicación de archivos (según architecture.md), tipos de datos (según glosario.md), conexión con componentes existentes
   - **Gap:** ambigüedades, omisiones, decisiones pendientes

4. **Identificar gaps**
   - Tipos de gaps:
     - **Ambigüedad:** la narrativa dice algo que puede interpretarse de más de una forma
     - **Omisión:** falta información que la IA necesita para implementar
     - **Decisión pendiente:** algo que el usuario tiene que decidir antes de implementar
     - **Dependencia no resuelta:** necesita algo que aún no existe

### Fase 3: Preguntar

5. **Por cada gap, preguntar al usuario con opciones**
   - Presentar el gap con contexto
   - Ofrecer opciones concretas para resolverlo
   - Incluir sugerencia de la IA si aplica
   - Esperar respuesta del usuario
   - Guardar la respuesta asociada al gap

### Fase 4: Documentar
6. **Guardar**
   - Guardar en `src/features/{feature}/docs/02-review.md`

---

## Formato de Output: Review con Respuestas

```markdown
# Review: [nombre de la narrativa]

## Resumen (10 segundos)
- **Qué describe:** [componente / feature / flujo]
- **Estado:** [completa] | [faltan X cosas]

## Definido por el usuario ✅
- [Regla 1]
- [Regla 2]
- [Código incluido: X]

## Inferido por la IA ⚡
- [Lo que la IA puede resolver sola: ej, ubicación según architecture.md]

## Gaps a resolver ❓

### 1. [Título del gap]
**Qué falta:** [descripción breve]
**Por qué importa:** [qué pasa si no se resuelve]
**Opciones:** [opciones para resolver]
**Sugerencia:** [recomendación de la IA]
**Respuesta:** [lo que el usuario decidió]

### 2. [Título del gap]
...
```

---

## Ejemplos de referencia

Los siguientes archivos contienen ejemplos reales de Reviews bien escritos. Usalos como guía de razonamiento, no como template:

- [example-nr-1.md](./example-nr-1.md) — ExpenseCard con 6 gaps resueltos
- [example-nr-2.md](./example-nr-2.md) — MonthRail con 6 gaps resueltos
- [example-nr-3.md](./example-nr-3.md) — Totales con 3 gaps resueltos

---


## Reglas de la Skill

1. **No generar código** — el usuario ve código cuando se implementa
2. **No generar contratos** — la narrativa es el contrato
3. **No generar tareas** — eso es otra skill
4. **Ser rápida** — el output se lee en 30 segundos
5. **Solo gaps** — no repetir lo que la narrativa ya dice bien
6. **Preguntas concretas** — cada gap tiene una pregunta que se responde rápido

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Puedo poner el análisis completo por si acaso" | El usuario no lo lee. Solo los gaps importan |
| "Debería sugerir cómo resolver cada gap" | El usuario es el senior dev — él sabe cómo resolverlo |
| "Los gaps obvios no hace falta listarlos" | Si es obvio para el usuario pero no para la IA, es un gap |
| "Puedo generar el contrato después del review" | No hace falta — la narrativa actualizada es el contrato |

## Red Flags

- Review sin gaps (¿la narrativa es realmente completa?)
- Gaps demasiado específicos (micro-gestion)
- Gaps demasiado vagos (el usuario no sabe qué responder)
- Incluir código en el output

## Verification

- [ ] Se cargó la narrativa
- [ ] Se cargó el contexto del proyecto
- [ ] Lo explícito vs lo inferido está separado
- [ ] Cada gap tiene una pregunta concreta
- [ ] El output se lee en 30 segundos
- [ ] No hay código en el output
- [ ] No hay contratos ni tareas

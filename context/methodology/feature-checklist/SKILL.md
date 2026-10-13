---
name: feature-checklist
description: Genera un checklist por feature con items concretos y verificables. A partir de la narrativa y el review, lista todo lo que hay que hacer para completar la feature. Use después de narrative-review para tener el checklist antes de implementar.
---

# Feature Checklist

## Overview

Genera un **checklist por feature** basado en los casos de uso. Cada item agrupa UC relacionados y se puede marcar como hecho cuando se completa.

**Flujo:**
```
Casos de uso + review → checklist → se actualiza durante implementación
```

## When to Use

- Se generaron los casos de uso con `use-cases`
- Se quiere tener el checklist antes de implementar
- Se quiere compartir status de progreso con el equipo
- NOT para: features que no tienen casos de uso generados

## Inputs

| Archivo | Rol |
|---|---|
| Casos de uso | Escenarios que deben funcionar |
| Review con respuestas | Decisiones tomadas |

## Core Process

1. **Leer casos de uso + review**
   - Identificar casos de uso relacionados para agrupar
   - Identificar dependencias entre items

2. **Generar items**
   - Agrupar casos de uso relacionados en items de alto nivel
   - Cada item referencia los UC que cubre
   - Ordenar por dependencias (lo que va primero arriba)

3. **Presentar al usuario**
   - Checklist para validar
   - El usuario confirma, agrega o elimina items

4. **Guardar**
   - Guardar en `src/features/{feature}/docs/04-checklist.md`

## Formato de Output

```markdown
# Checklist: [Feature/Componente]

**Casos de uso fuente:** [ruta]
**Review fuente:** [ruta]
**Fecha:** [fecha]

---

## Pendiente

- [ ] [Item] — UC-[rango]
- [ ] [Item] — UC-[rango]

## Hecho

- (nada aún)
```

## Ejemplos de referencia

Los siguientes archivos contienen ejemplos reales de Reviews bien escritos. Usalos como guía de razonamiento, no como template:

- [example-fc-1.md](./example-fc-1.md) — Expense Card checklist con pendiente y hecho items

## Reglas

1. **Cada item referencia UC** — "Status pill — UC-01 a UC-04"
2. **Items de alto nivel** — "barra lateral con color", no "crear getCategoryColor.ts"
3. **Verificables** — cada item se puede marcar como hecho
4. **Para compartir** — alguien que lee el checklist sabe qué está hecho y qué falta
5. **Mover a "Hecho" cuando se completa** — el checklist se actualiza durante implementación

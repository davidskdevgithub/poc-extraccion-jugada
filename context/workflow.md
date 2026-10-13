# Workflow — desarrollo de la PoC experimental

## Propósito

Conservar la metodología de trabajo entre sesiones de chat y del agente
que trabaja en el repositorio.

El orden del flujo no debe reconstruirse ni reemplazarse por intuición.
Las skills definen cómo producir cada documento.
Los ejemplos orientan el estilo y la trazabilidad.

---

## 1. Roles

### Chat de planificación

- Ayuda a preparar contexto y narrativas.
- Ayuda a adaptar las skills.
- Discute decisiones y resultados.
- No asume que una propuesta ya fue ejecutada.

### Agente del repositorio

- Lee los documentos vigentes.
- Revisa, documenta, implementa y ejecuta dentro del alcance autorizado.
- Registra evidencia y bloqueos.
- Se detiene en los límites acordados.

### Usuario

- Resuelve decisiones de producto.
- Revisa documentos y evidencia.
- Realiza sus propias pruebas cuando corresponda.
- Aprueba continuar después de cada Pause Point.

---

## 2. Secuencia por etapa

### Paso 1 — Narrativa

Salida:
- 01-narrative.md

Define objetivo, alcance, entradas, entregables y Pause Point.
Se prepara colaborativamente antes de implementar.

### Paso 2 — Review

Skill:
- narrative-review

Ubicación:
- .omp/skills/narrative-review/SKILL.md

Es la variante adaptada para esta PoC experimental.

Entradas:
- Narrativa.
- Contexto global.
- Resultados previos relevantes.

Salida:
- 02-review.md

Resolver los gaps que bloquean el siguiente paso.
Las hipótesis experimentales pueden quedar pendientes de ejecución,
si su evaluación está definida.

No avanzar automáticamente a implementación.

### Paso 3 — Casos de uso y evaluación experimental

Base para la adaptación:
- Skill original use-cases.
- Ejemplo de casos de uso del visor.

Salida prevista:
- 03-use-cases.md

Debe conservar:
- Dado / Cuando / Entonces.
- Identificadores de escenarios.
- Superficie que ejecuta el comportamiento.
- Casos de composición cuando correspondan.

Debe incorporar:
- Un protocolo separado para evaluar hipótesis experimentales.
- Evidencia requerida y responsable de revisión.

Skill:
- use-cases

Ubicación:
- .omp/skills/use-cases/SKILL.md

Versión adaptada para la PoC:
- Conserva Dado / Cuando / Entonces, IDs y superficies.
- Conserva composición cuando corresponda.
- Separa casos de uso UC-* de evaluaciones experimentales PE-*.
- Define evidencia, criterios de interpretación y responsables.

Presentar 03-use-cases.md al usuario para revisión.
No comenzar la checklist automáticamente.

### Paso 4 — Checklist

Base para la adaptación:
- Skill original feature-checklist.
- Ejemplo de checklist del visor.

Salida prevista:
- 04-checklist.md

Debe conservar:
- Items concretos y verificables.
- Referencias a los casos de uso.
- Orden según dependencias.

Debe distinguir:
- Implementación.
- Tests.
- Ejecución con el clip.
- Entrega de evidencia.
- Revisión humana.

La versión adaptada de esta skill todavía está pendiente.
Prepararla antes de utilizarla en esta PoC.

Presentar el documento al usuario para revisión.

### Paso 5 — Plan de implementación de la etapa

El agente lee narrativa, review, casos de uso y checklist.

En modo planificación:
- Inspecciona el estado real del repositorio.
- Propone el trabajo dentro del alcance.
- Señala bloqueos o contradicciones.
- No reabre decisiones sin una razón concreta.

La implementación comienza después de autorizar ese plan.

### Paso 6 — Implementación y ejecución

El agente:
- Implementa la etapa.
- Ejecuta tests.
- Ejecuta el experimento con el clip cuando sea posible.
- Actualiza la checklist.
- Registra resultados y fallos.

Salida:
- Código y tests.
- Artefactos de ejecución.
- 05-results.md.

No declarar validada una capacidad solo porque los tests pasan.

### Paso 7 — Revisión y Pause Point

El usuario revisa la evidencia y realiza sus propias pruebas.

Decisiones posibles:
- Continuar.
- Ajustar y repetir.
- Detener o descartar el enfoque.

Registrar la decisión en context/plan.md.

No comenzar la etapa siguiente sin aprobación explícita.

---

## 3. Estado actual — 2026-10-13

- Narrativa, review, casos de uso y checklist de E0 disponibles:
  01-narrative.md, 02-review.md, 03-use-cases.md y 04-checklist.md.
- Skills narrative-review, use-cases y feature-checklist adaptadas y
  utilizadas desde .omp/skills/.
- 03-use-cases.md revisado y aprobado por el usuario (2026-10-13).
- 04-checklist.md revisada y aprobada por el usuario (2026-10-13).
- Plan de implementación en preparación (paso 5 del workflow).
- data/local/ contiene: gol-del-rival.mp4, las capturas 01-inicio.png,
  02-pase-malo.png, 03-rival-libre.png, 04-rival-gol.png y la captura
  anotada limites.png. Hash y origen de cada archivo pendientes de
  registro en la primera ejecución (UC-G1 de 03-use-cases.md).
- Entorno observado el 2026-10-13: uv 0.12.24 y ffmpeg/ffprobe 9.0.2
  disponibles vía Homebrew; Python global 3.14.7 sin modificar.
  El origen de estas instalaciones es incierto (posible resto de la
  sesión retirada): el estado efectivo se registra y verifica en
  UC-01 antes de instalar o reinstalar algo.
- No instalar ni reinstalar sin autorización registrada.
- Plan de implementación pendiente de preparación y autorización
  (paso 5 del workflow).
- E0 no completada ni aprobada.

Actualizar este estado cuando se conozca el resultado del agente.
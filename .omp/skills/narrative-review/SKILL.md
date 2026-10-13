---
name: narrative-review
description: Revisa narrativas de PoCs y etapas experimentales. Separa gaps de producto, técnicos, experimentales y de dependencia. Recomienda decisiones técnicas y propone evidencia para validar hipótesis, sin exigir que el usuario sea especialista. No implementa ni genera tareas.
---

# Narrative Review

## Propósito

Revisar una narrativa antes de implementarla, distinguiendo:
- Qué está definido.
- Qué puede resolver la IA.
- Qué necesita una decisión del usuario.
- Qué solo puede comprobarse mediante un experimento.

El usuario tiene experiencia en desarrollo y producto, pero puede no
conocer el dominio técnico de esta PoC.

No transferirle una elección técnica sin recomendar un enfoque y explicar
sus consecuencias.

---

## Cuándo usarla

- Existe una narrativa de una etapa o feature.
- Hay incertidumbres técnicas o de viabilidad.
- Se necesita delimitar implementación, evidencia y revisión humana.

No usarla para:
- Implementar.
- Generar una checklist.
- Diseñar todo el proyecto.
- Evaluar resultados de una ejecución ya realizada.

---

## Entradas

Leer cuando estén disponibles:
- Narrativa: fuente primaria del trabajo propuesto.
- README.md: objetivo y alcance.
- context/glosario.md: vocabulario.
- context/stack.md: decisiones y candidatos técnicos.
- context/architecture.md: convenciones.
- context/plan.md: dependencias, estado y Pause Points.
- Resultados de etapas previas relevantes.
- Estado del repositorio, mediante inspección de solo lectura.

Si falta un documento, explicar qué no puede verificarse.
No convertir automáticamente cada documento ausente en un bloqueo.

No modificar archivos del sistema, instalar dependencias ni ejecutar el
experimento durante este review.

---

## Proceso

### 1. Cargar y contrastar

Identificar:
- Objetivo de la etapa.
- Entradas y entregables.
- Alcance permitido y exclusiones.
- Decisiones explícitas.
- Hipótesis.
- Evidencia requerida.
- Revisión humana.
- Condición de detención.

Detectar contradicciones con el contexto o con resultados previos.

Una decisión documentada puede revisarse si aparece una incompatibilidad,
pero no reemplazarla silenciosamente.

### 2. Clasificar los gaps

#### Producto

Afectan utilidad, alcance o interpretación del resultado.

Acción:
- Formular una pregunta concreta.
- Explicar la consecuencia de no resolverla.
- Recomendar una opción cuando haya contexto suficiente.
- Esperar decisión si bloquea el trabajo.

#### Técnico

Afectan cómo realizar el trabajo.

Acción:
- Recomendar un enfoque mínimo.
- Justificarlo brevemente.
- Explicar límites y consecuencias.
- Resolverlo por delegación si está dentro del alcance y es reversible.
- Consultar si implica costo, instalación del sistema, compromiso de
  licencia o ampliación de alcance.

No pedir al usuario que elija algoritmos sin criterio para hacerlo.

#### Experimental

Son afirmaciones que requieren ejecución y evidencia.

Acción:
- Formular una hipótesis o pregunta comprobable.
- Definir evidencia y método de evaluación.
- Identificar quién la revisará.
- Registrar el Pause Point correspondiente.

No marcar el gap como validado por haber acordado cómo probarlo.

#### Dependencia o entrada

Requieren un archivo, dato, herramienta o resultado anterior.

Acción:
- Indicar qué falta.
- Explicar qué trabajo queda bloqueado.
- Solicitar la entrada concreta cuando sea necesario.
- Separar lo bloqueado de lo que puede continuar.

### 3. Investigar solo cuando sea necesario

Si una recomendación depende de compatibilidad, licencias o capacidades
actuales:
- Verificar en documentación oficial cuando haya acceso.
- Registrar fuente y fecha de consulta.
- Investigar únicamente lo necesario para esta etapa.

Si no hay navegación o no se puede verificar:
- Declarar la recomendación provisional.
- Indicar la comprobación pendiente.

No afirmar que se investigó algo que no se consultó.
No abrir una comparación exhaustiva de stacks por defecto.

### 4. Preguntar con criterio

Consultar primero los gaps que bloquean la etapa.

Agrupar preguntas relacionadas y evitar un cuestionario técnico extenso.

Cada pregunta debe permitir decidir sobre una consecuencia comprensible,
no requerir conocimiento especializado.

No volver a preguntar lo que ya está explícito en la narrativa.

### 5. Documentar

Guardar el review junto a la narrativa como 02-review.md.

Si todavía faltan respuestas:
- Guardar el estado pendiente.
- No inventar decisiones del usuario.

No sobrescribir decisiones o respuestas existentes sin señalar el cambio.

---

## Estados de los gaps

- Resuelto por contexto.
- Decisión técnica delegada.
- Pendiente de decisión del usuario.
- Pendiente de entrada.
- Experimento definido; resultado pendiente.
- Verificación técnica pendiente.

Definir además si cada gap bloquea:
- La preparación.
- La ejecución.
- La aprobación.
- Nada por ahora.

Un experimento definido puede permitir implementar, aunque su resultado
todavía sea desconocido.

---

## Formato del review

# Review — [etapa o feature]

## Resumen

- Objetivo: [una frase].
- Preparación/implementación: lista o bloqueada.
- Ejecución: lista o bloqueada.
- Validación: todavía pendiente de evidencia y revisión.
- Preguntas necesarias ahora: [cantidad].

## Confirmado por el contexto

[Lista breve; no repetir toda la narrativa.]

## Decisiones técnicas delegadas

Solo decisiones relevantes que no requieran una pregunta:

- Decisión: [...]
- Motivo: [...]
- Límite o comprobación pendiente: [...]

## Gaps

### G-01 — [título]

- Tipo: producto / técnico / experimental / dependencia.
- Qué falta: [...]
- Por qué importa: [...]
- Recomendación: [...]
- Pregunta al usuario: [...] o "no requiere decisión ahora".
- Evidencia o comprobación: [...] o "no aplica".
- Estado: [...]
- Bloquea: [...]
- Respuesta del usuario: [...] o "pendiente / no aplica".

[Repetir únicamente para gaps reales.]

## Pause Point verificado

- Detenerse después de: [...]
- Entregar: [...]
- Revisión humana: [...]
- No continuar con: [...]

## Condición para avanzar

[Qué necesita resolverse para implementar o ejecutar esta etapa.
No confundir esto con autorizar la etapa siguiente.]

---

## Reglas

1. No generar código.
2. No generar tareas ni checklist.
3. No crear un contrato alternativo a la narrativa.
4. No ejecutar el experimento.
5. No ampliar el alcance para resolver una incertidumbre futura.
6. No inventar gaps para que el review parezca completo.
7. Un review sin gaps es válido si la narrativa está suficientemente clara.
8. No dar por validada una hipótesis mediante conversación.
9. No presentar una recomendación como decisión explícita del usuario.
10. Distinguir bloqueos actuales de pendientes futuros.
11. Ser breve; incluir el detalle necesario para decidir, no un tratado.
12. Solo el usuario aprueba continuar después del Pause Point.

---

## Verificación final

- [ ] Se leyó la narrativa y el contexto relevante.
- [ ] No se volvieron a preguntar decisiones ya documentadas.
- [ ] Cada gap tiene tipo, estado e impacto sobre el avance.
- [ ] Las decisiones técnicas incluyen una recomendación.
- [ ] Las incertidumbres experimentales tienen evidencia propuesta.
- [ ] No se confundió "definido" con "validado".
- [ ] El Pause Point y la revisión humana están claros.
- [ ] No se generó código, tareas ni alcance adicional.
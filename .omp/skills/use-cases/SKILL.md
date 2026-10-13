---
name: use-cases
description: Genera casos de uso Dado/Cuando/Entonces y un protocolo de
  evaluación experimental a partir de una narrativa y su review.
  Conserva IDs, superficies y trazabilidad. Separa comportamientos
  verificables de hipótesis que requieren ejecución y revisión humana.
---

# Use Cases

## Propósito

Documentar antes de implementar:

- Los comportamientos que debe ofrecer la etapa.
- Los casos de borde y errores relevantes.
- Las decisiones del review que deben respetarse.
- El protocolo para evaluar las incertidumbres experimentales.

Los casos de uso guían implementación y tests.
El protocolo experimental guía la ejecución y la revisión de evidencia.

Un test exitoso no demuestra viabilidad ni utilidad del enfoque.

## Cuándo usarla

- Existe una narrativa y su review.
- Las decisiones necesarias para especificar comportamientos están
  resueltas o explícitamente delegadas.
- Se necesitan escenarios y criterios de evaluación antes de preparar
  la checklist.

No usarla para:

- Implementar código.
- Ejecutar el experimento.
- Generar la checklist.
- Diseñar etapas futuras.
- Evaluar resultados de una ejecución ya realizada.

Una entrada pendiente puede bloquear la ejecución real sin impedir
documentar los comportamientos y el protocolo de evaluación.

## Entradas

| Archivo | Rol |
|---|---|
| Narrativa | Objetivo, alcance, comportamientos y entregables |
| Review con respuestas | Decisiones, gaps y bloqueos |
| context/workflow.md | Secuencia y límites del trabajo |
| context/plan.md | Estado, dependencias y Pause Points |
| context/architecture.md | Organización y límites de componentes |
| context/glosario.md | Terminología y convenciones |
| context/stack.md | Decisiones técnicas vigentes |
| Resultados previos relevantes | Evidencia y limitaciones conocidas |

Leer el contexto disponible sin repetirlo íntegramente en la salida.

Si falta una entrada, explicar qué no puede especificarse.
No convertir automáticamente un archivo ausente en un bloqueo.

## Proceso

### 1. Leer y contrastar

Identificar:

- Comportamientos explícitos.
- Decisiones del review.
- Casos de borde y errores.
- Entradas y entregables.
- Hipótesis o preguntas experimentales.
- Evidencia requerida.
- Responsables de revisión.
- Pause Point.

Si hay contradicciones que afectan la especificación, señalarlas antes
de asumir una solución.

No reabrir decisiones existentes sin una razón concreta.

### 2. Separar comportamiento de evaluación

Clasificar cada requisito:

- Comportamiento especificable: corresponde a un caso de uso.
- Decisión técnica: se cubre mediante comportamiento observable cuando
  corresponda; no exige un escenario sobre cada detalle interno.
- Hipótesis experimental: corresponde al protocolo de evaluación.
- Decisión humana: se registra como revisión o condición de avance.
- Dependencia pendiente: se indica qué impide ejecutar.

No transformar una hipótesis en un resultado esperado garantizado.

Ejemplo:

- Caso de uso: cada imagen registra su timestamp real.
- Evaluación: revisar si las imágenes permiten identificar referencias
  útiles sobre el suelo.

### 3. Generar casos de uso

Conservar estas secciones cuando correspondan:

- Happy Path: UC-01, UC-02...
- Edge Cases: UC-E1, UC-E2...
- Escenarios de gaps resueltos: UC-G1, UC-G2...
- Composición con etapas o componentes previos: UC-C1, UC-C2...

Cada escenario incluye:

- Dado: contexto y prerrequisitos.
- Cuando: acción o situación.
- Entonces: resultado observable.
- Superficie: quién ejecuta el comportamiento y por qué entrada.
- Verificación: tipo de comprobación apropiada.
- Referencias: sección de narrativa o gap relevante.

Las superficies pueden ser:

- CLI.
- Función o módulo del proceso.
- Herramienta externa invocada por el proceso.
- Procedimiento manual documentado.
- UI, si ya existe y forma parte del alcance.

No inventar comandos, APIs o interfaces públicas todavía no acordadas.

La verificación puede ser:

- Test unitario.
- Test de integración con entrada sintética.
- Inspección de artefactos de una ejecución.
- Revisión documental o humana.

No exigir un test automatizado para toda obligación documental.

Un escenario representa un comportamiento.
Puede incluir las comprobaciones necesarias para verificarlo, pero no
agrupar comportamientos independientes.

### 4. Cubrir las decisiones del review

Cada gap resuelto que defina un comportamiento debe quedar cubierto.

Puede:

- Tener un escenario UC-G propio.
- Referenciar un escenario existente que ya lo cubra.

No duplicar escenarios únicamente para conservar una sección.

Los gaps experimentales pendientes se vinculan al protocolo.
Los pendientes de entrada se registran como prerrequisitos.

### 5. Documentar composición cuando corresponda

Usar UC-C cuando la etapa interactúe con capacidades implementadas
previamente o dependa de su estado en ejecución.

- El Dado describe ambos lados.
- El Entonces describe el comportamiento combinado.
- La Superficie explicita la cadena de interacción.
- Los escenarios viven en el documento de la etapa nueva.

No crear composición ficticia con etapas futuras.

Si un escenario reemplaza otro anterior, marcar el anterior como
"Superseded por [ID y documento]".

No borrar la historia ni re-verificar toda la etapa previa por defecto.

### 6. Preparar el protocolo experimental

Crear una sección independiente de los casos de uso.

Asignar IDs PE-01, PE-02...

Para cada evaluación registrar:

- Pregunta o hipótesis.
- Prerrequisitos y condiciones.
- Método de evaluación.
- Evidencia requerida.
- Criterio de interpretación.
- Quién ejecuta y quién revisa.
- Limitaciones.
- Relación con casos de uso y gaps.
- Impacto sobre el Pause Point.

Definir el protocolo antes de ejecutar.
No escribir resultados ni declarar hipótesis validadas.

Los criterios pueden ser cualitativos si permiten una revisión concreta.
No inventar umbrales numéricos sin fundamento.

Permitir resultados favorables, desfavorables o inconclusos.
La falta de evidencia debe quedar explícita.

Registrar el esfuerzo manual por actividad cuando corresponda.
Si no se midió, distinguir estimación de tiempo medido.

### 7. Presentar y guardar

Presentar el documento al usuario para revisión.

Guardar, cuando se trabaje en el repositorio, en:

experiments/<etapa>/03-use-cases.md

No utilizar rutas de documentación de features del frontend.

No inventar aprobación del usuario.
No comenzar la checklist ni la implementación automáticamente.

## Formato de salida

# Casos de uso y evaluación — [etapa]

**Narrativa fuente:** [ruta]
**Review fuente:** [ruta]
**Contexto relevante:** [rutas]
**Fecha:** [fecha]
**Estado:** pendiente de revisión

## Alcance y prerrequisitos

[Resumen breve de límites y dependencias pendientes.]

## Happy Path

### UC-01 — [Nombre]

**Dado** [contexto]
**Cuando** [acción]
**Entonces** [resultado observable]
**Superficie:** [entrada y responsable de ejecución]
**Verificación:** [tipo de comprobación]
**Referencias:** [narrativa o review]

## Edge Cases

### UC-E1 — [Nombre]

[Mismos campos.]

## Escenarios de gaps resueltos

### UC-G1 — [Nombre]

[Mismos campos.]

[O indicar qué UCs existentes cubren las decisiones, sin duplicarlos.]

## Composición con etapas o componentes previos

[UC-C cuando corresponda. Omitir si no aplica.]

## Protocolo de evaluación experimental

### PE-01 — [Pregunta o hipótesis]

- Pregunta o hipótesis:
- Prerrequisitos y condiciones:
- Método:
- Evidencia requerida:
- Criterio de interpretación:
- Ejecuta:
- Revisa:
- Limitaciones:
- Referencias a UC y gaps:
- Impacto sobre el Pause Point:

## Cobertura y pendientes

- Decisiones cubiertas y sus referencias.
- Dependencias que bloquean ejecución.
- Preguntas que impiden cerrar la especificación.
- Incertidumbres que se evaluarán al ejecutar.

No repetir toda la narrativa ni todo el review.

## Entrega y Pause Point

- Evidencia que debe entregarse.
- Qué requiere revisión humana.
- Qué decisión habilita continuar.
- Qué no puede comenzar todavía.

## Reglas

1. No generar código ni checklist.
2. No ejecutar herramientas ni el experimento.
3. No ampliar el alcance.
4. Conservar Dado/Cuando/Entonces, IDs y superficies.
5. Mantener trazabilidad sin duplicar escenarios.
6. Separar comportamientos de hipótesis experimentales.
7. No presentar tests exitosos como validación experimental.
8. No garantizar conclusiones que dependen del clip.
9. No introducir interfaces públicas por conveniencia documental.
10. Distinguir preparación, ejecución, revisión y validación.
11. No inventar decisiones ni aprobación humana.
12. Solo el usuario autoriza continuar después del Pause Point.

## Verificación final

- [ ] Se leyó narrativa, review y contexto relevante.
- [ ] No se asumieron soluciones ante contradicciones.
- [ ] Cada UC tiene resultado observable y superficie.
- [ ] Cada UC indica cómo puede verificarse.
- [ ] Las decisiones relevantes tienen cobertura trazable.
- [ ] Las hipótesis tienen protocolo y evidencia requerida.
- [ ] Los responsables de ejecución y revisión están identificados.
- [ ] Los bloqueos están separados de las incertidumbres experimentales.
- [ ] No se declararon resultados ni validaciones.
- [ ] El alcance y el Pause Point se conservaron.
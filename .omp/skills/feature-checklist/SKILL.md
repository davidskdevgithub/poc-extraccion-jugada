---
name: feature-checklist
description: >-
  Genera y mantiene una checklist por etapa de una PoC experimental,
  basada en casos de uso y protocolos de evaluación. Separa
  implementación, tests, ejecución, evidencia y revisión humana.
  Conserva trazabilidad y dependencias sin confundir trabajo completado,
  validación experimental ni autorización para continuar.
---

# Feature Checklist

## Propósito

Convertir los casos de uso y el protocolo experimental de una etapa
en una lista concreta, verificable y compartible.

La checklist debe mostrar:
- Qué falta.
- Qué se completó y con qué evidencia.
- Qué está bloqueado.
- Qué requiere revisión humana.
- Qué resultados siguen sin comprobarse.

Una checklist completa no demuestra por sí sola fidelidad, utilidad
ni generalización. Tampoco autoriza la etapa siguiente.

## Cuándo usarla

- Existe una narrativa y su review.
- Se generaron los casos de uso y el protocolo experimental.
- El usuario habilitó preparar la checklist según el workflow.
- Se necesita actualizar su estado durante el trabajo autorizado.

No usarla para:
- Reemplazar casos de uso o protocolos que todavía no existen.
- Diseñar etapas futuras.
- Preparar el plan técnico de implementación.
- Autorizar instalaciones, implementación o una etapa siguiente.

Generar la checklist no autoriza ejecutar su contenido.

## Entradas

| Archivo | Rol |
|---|---|
| 03-use-cases.md | Comportamientos UC-* y evaluaciones PE-* |
| 02-review.md | Decisiones, gaps, respuestas y actualizaciones |
| 01-narrative.md | Objetivo, alcance y entregables |
| context/workflow.md | Secuencia y autorizaciones |
| context/plan.md | Estado, dependencias y Pause Points |
| context/architecture.md | Organización y límites del trabajo |
| context/stack.md | Stack vigente para la etapa |
| context/glosario.md | Terminología |
| Resultados y artefactos disponibles | Evidencia para actualizar estado |

Leer el contexto relevante sin repetirlo íntegramente en la salida.

No asumir que una propuesta del chat fue guardada o ejecutada.

Si falta una entrada, explicar qué impide comprobar.
No convertir automáticamente cada ausencia en un bloqueo.

Si 03-use-cases.md está pendiente de revisión, no presentarlo como
aprobado. Una instrucción explícita puede habilitar una checklist
provisional; su dependencia debe quedar indicada.

## Proceso

### 1. Leer y contrastar

Identificar:
- Alcance y exclusiones.
- Comportamientos UC-*.
- Evaluaciones PE-*.
- Decisiones y actualizaciones del review.
- Entradas y herramientas necesarias.
- Evidencia y responsables.
- Entregables y Pause Point.
- Autorizaciones pendientes.

Si una contradicción afecta el contenido o su cierre, señalarla antes
de asumir una solución.

Conservar las decisiones vigentes. No reabrirlas sin una razón concreta.

Una observación histórica del entorno no garantiza su estado actual.
Si hubo cambios posteriores, conservar la comprobación pendiente.

### 2. Separar tipos de trabajo

Cada ítem debe pertenecer a un tipo visible:

- [Implementación]: comportamiento o mecanismo construido.
- [Tests]: comprobación de software ejecutada y registrada.
- [Ejecución]: procesamiento o evaluación con la entrada real.
- [Evidencia]: artefactos, registros e informe entregados.
- [Revisión humana]: evidencia examinada por el usuario y respuesta
  registrada.

No agrupar tipos distintos en una sola casilla.

Ejemplo:
- Implementar la inspección de metadatos.
- Ejecutar sus tests con entradas sintéticas.
- Inspeccionar el clip real.
- Entregar los metadatos y sus limitaciones.
- Revisar la evidencia con el usuario.

Pueden compartir referencias UC porque representan obligaciones
distintas.

### 3. Generar ítems concretos

Agrupar comportamientos relacionados cuando:
- El resultado sea comprensible.
- Compartan tipo de trabajo.
- Puedan cerrarse mediante una condición coherente.

Evitar:
- Una casilla para toda la etapa.
- Microtareas sobre cada archivo o función.
- Ítems vagos como "dejar todo listo".
- Casillas que mezclen construcción y validación experimental.

Cada ítem debe indicar:
- Acción o resultado verificable.
- Tipo de trabajo.
- Referencias UC-* y/o PE-*.
- Condición de cierre.

Referenciar también narrativa, gaps o contexto cuando aporte una
decisión relevante.

No inventar IDs para obligaciones que no tienen escenario.
Los controles del workflow pueden referenciar su documento fuente.

Si falta un UC o PE necesario para especificar un requisito, señalar
el pendiente. No crear silenciosamente una especificación alternativa
dentro de la checklist.

### 4. Ordenar por dependencias

Colocar primero lo necesario para habilitar el trabajo posterior.

Distinguir:
- Dependencias de implementación.
- Prerrequisitos de los tests.
- Entradas necesarias para ejecutar con el clip.
- Evidencia necesaria para la revisión humana.

No ordenar siempre por tipo si eso contradice las dependencias reales.

No convertir esta lista en el plan técnico de implementación.
La inspección del repositorio y la autorización de ese plan siguen
siendo pasos separados del workflow.

### 5. Definir evidencia y cierre

Usar evidencia adecuada al tipo de ítem:

- Implementación: código o configuración identificables, junto con
  una comprobación apropiada del comportamiento construido.
- Tests: comando o procedimiento, resultado y registro disponible.
- Ejecución: entrada identificada, configuración, ejecución y
  artefactos o fallo registrado.
- Evidencia: archivos entregados, ubicaciones y contenido comprobable.
- Revisión humana: respuesta explícita del usuario, identificada y
  registrada.

No exigir tests automatizados para obligaciones documentales.

No usar como prueba:
- Un comando que solo se propuso.
- Un enlace a un artefacto que todavía no existe.
- Un mock como demostración de calidad sobre el clip.
- Un test de estructura como demostración de fidelidad táctica.

Al generar la checklist, la condición de cierre describe evidencia
esperada. Al completar un ítem, registrar la evidencia real.

### 6. Tratar evaluaciones y bloqueos

Los ítems vinculados a PE-* deben cerrar por la realización del método
y el registro de evidencia e interpretación, no por obtener un
resultado favorable.

Una evaluación puede completarse con resultado:
- Favorable.
- Desfavorable.
- Inconcluso.

Esto es válido si se realizó el trabajo requerido por el protocolo
y se documentaron sus limitaciones.

Si el protocolo no pudo ejecutarse por falta de entrada, herramienta
o autorización, el ítem de ejecución sigue pendiente.

Si hubo ejecución parcial:
- Registrar qué se ejecutó.
- Registrar qué falló o quedó sin ejecutar.
- No marcar como completa una obligación que no cumplió su cierre.

Un informe de bloqueo puede estar entregado sin que la ejecución
esté completa.

Distinguir:
- Bloqueo: algo impide realizar el trabajo.
- Fallo de ejecución: una operación intentada falló.
- Resultado experimental desfavorable: la evidencia no sostiene el
  enfoque bajo las condiciones probadas.
- Resultado inconcluso: la evidencia no permite concluir.

No sumar alternativas ni ampliar el alcance automáticamente para
obtener un resultado favorable.

### 7. Presentar y guardar

Presentar la checklist al usuario para revisión.

Guardar, cuando se trabaje en el repositorio, en:

experiments/<etapa>/04-checklist.md

No usar rutas de documentación de features del frontend.
No crear docs/ en la raíz.

La revisión de la checklist no sustituye la autorización del plan
de implementación ni la aprobación del Pause Point.

No comenzar implementación o instalaciones automáticamente.

### 8. Actualizar durante el trabajo

Mover un ítem de "Pendiente" a "Hecho" únicamente cuando:
- Se cumple su condición de cierre.
- Existe evidencia real.
- La evidencia queda referenciada.

Conservar sus referencias UC/PE y agregar el resultado cuando
corresponda.

Si falta una parte, mantenerlo pendiente y registrar el avance parcial.

Para ítems humanos, solo registrar acciones y respuestas que el
usuario haya realizado explícitamente.

Si una comprobación posterior invalida el cierre, devolver el ítem a
"Pendiente" y explicar el motivo. No borrar la evidencia histórica.

No redefinir retroactivamente un criterio para convertir un resultado
desfavorable en éxito.

## Formato de salida

# Checklist — [etapa]

**Narrativa fuente:** [ruta]
**Review fuente:** [ruta]
**Casos de uso y evaluación fuente:** [ruta]
**Contexto relevante:** [rutas]
**Fecha:** [fecha]
**Estado documental:** pendiente de revisión

## Alcance y condiciones previas

[Resumen breve de límites, dependencias y autorizaciones pendientes.]

## Pendiente

- [ ] **[Implementación]** [Resultado concreto] — UC-[ID]
  - Cierre: [comprobación y evidencia necesarias].

- [ ] **[Tests]** [Comportamientos que se comprueban] — UC-[IDs]
  - Cierre: [pruebas ejecutadas y resultado registrado].

- [ ] **[Ejecución]** [Trabajo con la entrada real] — UC-[ID], PE-[ID]
  - Cierre: [método realizado, evidencia y resultado documentados,
    sin exigir una conclusión favorable].

- [ ] **[Evidencia]** [Entrega verificable] — UC-[ID], PE-[ID]
  - Cierre: [contenido y ubicación de la entrega].

- [ ] **[Revisión humana]** [Evidencia que revisará el usuario] — PE-[ID]
  - Cierre: [respuesta explícita registrada, sin exigir aprobación
    para continuar].

[Repetir únicamente los ítems necesarios y ordenarlos por dependencias.]

## Hecho

(Ninguno todavía.)

[Al actualizar, mover aquí los ítems completos y agregar:
- Evidencia: [ruta, ejecución, resultado o respuesta identificable].
- Resultado: [cuando corresponda].]

## Bloqueos y pendientes

- [Qué falta, qué ítems afecta y qué puede continuar].
- [Avance parcial o fallo registrado, cuando corresponda].

(No identificados, si no existen.)

## Cobertura

[Correspondencia breve entre UC/PE e ítems.
Señalar requisitos sin cobertura y justificar exclusiones.
No repetir los escenarios ni construir una matriz innecesaria.]

## Entrega y Pause Point

- Entrega prevista: [artefactos e informe].
- Revisión humana requerida: [qué debe examinar el usuario].
- Decisión del usuario: pendiente.
- Registro de la decisión: context/plan.md.
- No iniciar todavía: [siguiente etapa y trabajo fuera de alcance].

Todas las casillas completas indican trabajo completado según sus
condiciones de cierre. No constituyen por sí solas validación
experimental ni autorización para continuar.

## Reglas

1. Conservar ítems concretos, verificables y trazables.
2. Separar implementación, tests, ejecución, evidencia y revisión.
3. No ampliar el alcance ni diseñar etapas futuras.
4. No inventar comandos, interfaces o detalles técnicos no acordados.
5. No marcar como ejecutado algo solamente propuesto.
6. No presentar tests exitosos como validación experimental.
7. No exigir resultados favorables para completar una evaluación.
8. No presentar un bloqueo como evaluación ejecutada.
9. No inventar respuestas, tiempos, resultados ni evidencia.
10. No marcar una revisión humana sin intervención del usuario.
11. No derivar aprobación de una checklist completa ni del silencio.
12. Solo el usuario decide continuar después del Pause Point.

## Verificación final de la skill

- [ ] Se leyeron los casos de uso, el protocolo y el contexto relevante.
- [ ] Se conservaron alcance, decisiones y autorizaciones.
- [ ] Los ítems tienen tipo, referencias y condición de cierre.
- [ ] Implementación, tests y ejecución no comparten una sola casilla.
- [ ] Los UC y PE relevantes tienen cobertura.
- [ ] El orden respeta dependencias.
- [ ] Los bloqueos están separados de los resultados experimentales.
- [ ] Es posible cerrar una evaluación desfavorable o inconclusa.
- [ ] No se atribuyeron decisiones ni revisiones al usuario.
- [ ] El Pause Point no depende automáticamente de las casillas.
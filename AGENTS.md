# AGENTS.md

Guía de agentes y convenciones para el banco de pruebas `hermes-opencode`.

Este documento define **qué agentes existen**, **qué instrucciones tiene cada uno** y
**el registro de resultados de las pruebas** realizadas. Se mantiene como fuente de
verdad del proyecto y debe actualizarse cada vez que se añada o cambie un agente, o
cuando se ejecute una prueba nueva.

> Estado inicial: proyecto recién creado. Aún no hay pruebas ejecutadas; la sección
> [Resultados de pruebas](#resultados-de-pruebas) queda como plantilla para rellenar.

## Tabla de contenidos

- [Convenciones generales](#convenciones-generales)
- [Agentes](#agentes)
  - [explorer](#explorer)
  - [implementer](#implementer)
  - [reviewer](#reviewer)
- [Instrucciones comunes](#instrucciones-comunes)
- [Resultados de pruebas](#resultados-de-pruebas)
- [Cómo actualizar este documento](#cómo-actualizar-este-documento)

## Convenciones generales

- **Idioma**: responde y escribe la documentación en español.
- **Alcance**: este proyecto es un entorno aislado de pruebas; aquí se pueden romper
  cosas, iterar rápido y validar ideas antes de llevarlas a producción.
- **Seguridad**: no incluyas secretos, claves API ni credenciales reales en archivos
  versionados.
- **Trazabilidad**: cada prueba documentada debe indicar objetivo, agente implicado,
  comando/prompt ejecutado y resultado (OK / fallo / observaciones).
- **Referencias**: enlaza a archivos concretos (`ruta/a/archivo`) al justificar cambios.

## Agentes

Lista de agentes definidos en este proyecto. Cada entrada documenta su **rol**,
**instrucciones** y **herramientas recomendadas**.

| Agente | Rol | Estado |
| --- | --- | --- |
| [`explorer`](#explorer) | Explorar y entender el código | Propuesto |
| [`implementer`](#implementer) | Implementar cambios | Propuesto |
| [`reviewer`](#reviewer) | Revisar calidad y corrección | Propuesto |

### explorer

- **Rol**: localizar archivos, buscar patrones y responder preguntas sobre el código.
- **Instrucciones**:
  - Prioriza búsqueda eficiente (glob/grep) antes de leer archivos completos.
  - Devuelve rutas de archivo concretas y números de línea cuando sea relevante.
  - No modifica archivos; es un agente de solo lectura.
  - Resume hallazgos de forma breve y accionable.
- **Herramientas recomendadas**: `glob`, `grep`, `read`.
- **Modelo sugerido**: rápido y de bajo coste (p. ej. un modelo "lite/flash").

### implementer

- **Rol**: aplicar cambios de código siguiendo las convenciones del proyecto.
- **Instrucciones**:
  - Lee y respeta el estilo, nombres y patrones del código existente antes de escribir.
  - Haz cambios mínimos y enfocados; evita reescrituras innecesarias.
  - Usa `edit` para cambios puntuales y `write` solo para archivos nuevos o reemplazos totales.
  - Verifica el resultado (compilación/tests si existen) y reporta qué se cambió.
- **Herramientas recomendadas**: `read`, `edit`, `write`, `grep`, `glob`, `shell`.
- **Modelo sugerido**: modelo con buena capacidad de razonamiento y adherencia a instrucciones.

### reviewer

- **Rol**: revisar cambios en busca de errores, riesgos y desviaciones de convenciones.
- **Instrucciones**:
  - Compara el cambio contra las convenciones de [Convenciones generales](#convenciones-generales).
  - Señala problemas de correctitud, seguridad y mantenibilidad.
  - Sé concreto: indica archivo, línea y sugerencia de mejora.
  - No reescribe el código; propone ajustes y deja la implementación al `implementer`.
- **Herramientas recomendadas**: `read`, `grep`, `glob`.
- **Modelo sugerido**: modelo con buen juicio crítico y atención al detalle.

## Instrucciones comunes

Aplican a todos los agentes salvo que se indique lo contrario:

1. **Investiga antes de actuar**: no borres ni sobrescribas trabajo existente sin
   entenderlo primero.
2. **No inventes resultados**: si una prueba no se ha ejecutado, márcala como pendiente.
3. **Documenta tus cambios**: actualiza `AGENTS.md` y `README.md` cuando aplique.
4. **Sé conciso**: respuestas claras y sin jerga innecesaria.
5. **No filtres secretos**: nunca publiques claves, tokens ni credenciales.

## Resultados de pruebas

Registro de pruebas ejecutadas. Rellena una fila por prueba. No marques como OK algo
que no se haya verificado realmente.

| # | Fecha | Agente | Objetivo de la prueba | Comando / Prompt | Resultado | Observaciones |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-11-21 | implementer | Crear app FastAPI (Panel de Control Local) + Docker | `docker compose up -d --build`; `curl /healthz`, `/api/status`, POST/PATCH/DELETE `/api/tasks`, GET `/` | OK | Todos los endpoints responden 200; HTML servido en `/`; datos en memoria. |
| 2 | 2026-11-21 | implementer | Añadir `GET /api/services` (systemctl → docker → fallback) y tarjeta en la UI | `curl /api/services` (uvicorn local); arranque con `python -m uvicorn app:app` | OK | Devuelve 15 servicios reales vía `systemctl` (`fuente: systemctl`, `total: 15`); UI muestra tarjeta con botón "Actualizar". |
| 3 | 2026-11-21 | implementer | Ver `journalctl` de un servicio: endpoint `GET /api/services/{nombre}/logs` + modal en la UI | `docker compose up -d --build`; `curl /api/status`, `/api/services`, `/api/services/{svc}/logs` (válido, inexistente y nombre inválido), `GET /` | OK | Imagen reconstruida (con `systemd`) y contenedor `panel-control-local` arriba; logs reales con `fuente: journalctl`; nombre inválido → 400; `../etc/passwd` → 404; servicio inexistente → 200 con `-- No entries --`. |

### Leyenda de resultados

- **OK**: la prueba se ejecutó y el comportamiento fue el esperado.
- **FAIL**: la prueba se ejecutó y el resultado no fue el esperado.
- **PARCIAL**: funcionó parcialmente o con limitaciones.
- **PENDIENTE**: aún no se ha ejecutado.

## Cómo actualizar este documento

- **Nuevo agente**: añádelo a la tabla [Agentes](#agentes) y crea su subsección con
  rol, instrucciones y herramientas.
- **Cambio de instrucciones**: edita la subsección correspondiente y anota el motivo
  en la fila de pruebas asociada.
- **Nueva prueba**: añade una fila en [Resultados de pruebas](#resultados-de-pruebas)
  con fecha, agente, objetivo, comando/prompt y resultado real.
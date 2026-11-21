# hermes-opencode

> Proyecto de pruebas para [OpenCode](https://opencode.ai).

Este repositorio sirve como banco de pruebas para experimentar con OpenCode:
probar agentes, herramientas (tools), configuración, skills, MCP, prompts y
flujos de trabajo sin afectar a proyectos de producción.

## Tabla de contenidos

- [Descripción](#descripción)
- [Objetivo](#objetivo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Configuración](#configuración)
- [Pruebas](#pruebas)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Descripción

`hermes-opencode` es un entorno aislado para probar capacidades de OpenCode:
definición de agentes y subagentes, tools personalizadas, skills, servidores
MCP, proveedores y modelos, temas, keybinds, formatters y plugins.

Al ser un proyecto de pruebas, aquí se pueden romper cosas, iterar rápido y
validar ideas antes de llevarlas a un entorno real.

## Objetivo

- Probar configuraciones de OpenCode de forma reproducible.
- Experimentar con agentes, herramientas y flujos de trabajo.
- Documentar qué funciona y qué no, con ejemplos concretos.
- Servir de referencia para configuraciones reutilizables.

## Estructura del proyecto

<!-- TODO: Ajusta esta sección a los archivos reales que añadas. -->

```
hermes-opencode/
├── README.md
├── opencode.json          # Configuración de OpenCode (proveedores, agentes, tools)
├── AGENTS.md              # Instrucciones y convenciones para los agentes
├── skills/                # Skills personalizadas (opcional)
├── prompts/               # Prompts y plantillas de prueba (opcional)
└── tests/                 # Casos de prueba y ejemplos (opcional)
```

## Requisitos previos

- [OpenCode](https://opencode.ai) instalado y funcionando.
- Node.js (si el proyecto usa herramientas o scripts basados en Node).
- Acceso a un proveedor/modelo configurado en OpenCode.

<!-- TODO: Añade versiones concretas si son relevantes. -->

## Instalación

```bash
# Clonar el repositorio
git clone <URL_DEL_REPO> hermes-opencode
cd hermes-opencode

# (Opcional) Si hay dependencias de Node
npm install
```

## Uso

```bash
# Iniciar OpenCode dentro del proyecto
opencode
```

Luego puedes probar agentes, herramientas y flujos descritos en
[Configuración](#configuración) y [Pruebas](#pruebas).

## Configuración

<!-- TODO: Documenta tu opencode.json, agentes, providers y tools reales. -->

Ejemplo de `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "provider/modelo",
  "agent": {},
  "mcp": {}
}
```

Consulta la [documentación de OpenCode](https://opencode.ai/docs) para la
referencia completa de configuración.

## Pruebas

<!-- TODO: Explica cómo ejecutar y qué validan tus pruebas. -->

```bash
# Ejemplo: ejecutar el/los test(s)
npm test
```

## Contribución

1. Crea una rama para tu cambio: `git checkout -b mi-cambio`.
2. Haz tus modificaciones y documenta el resultado.
3. Abre un Pull Request describiendo qué probaste y cómo.

## Licencia

<!-- TODO: Indica la licencia, por ejemplo MIT. -->

Sin especificar.
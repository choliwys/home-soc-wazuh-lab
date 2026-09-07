# Trabajo con Codex y otros asistentes de IA

## Fuente de contexto

Al iniciar una sesión nueva, proporcionar a la LLM:

1. `docs/project-context.md`.
2. `docs/status.md`.
3. El runbook, detección o error concreto en el que se trabajará.

`docs/` es la fuente de verdad. [AGENTS.md](../AGENTS.md) contiene las instrucciones operativas persistentes para Codex.

## Forma de pedir ayuda

Definir una tarea concreta, el resultado esperado y los límites de acción. Ejemplo: “Revisa los prerrequisitos del nodo Wazuh, no cambies el servidor y devuelve los bloqueos con su evidencia”.

Para comandos o cambios técnicos, pedir siempre:

- propósito y prerrequisitos;
- impacto en servicios o archivos;
- riesgos y reversión segura;
- pasos de validación;
- evidencia que se debe documentar.

Para cambios en el repositorio, pedir también los archivos que se modificarán y el criterio de aceptación. Para tareas pequeñas, mantener el contexto y las instrucciones concisos; reglas repetidas o prompts extensos no mejoran la calidad.

## Reglas de seguridad

- Nunca pegar secretos, contraseñas, claves de agentes, certificados, tokens ni logs privados.
- Reemplazar datos sensibles por placeholders antes de compartirlos.
- Confirmar antes de ejecutar comandos destructivos, cambios remotos, instalaciones o cambios de firewall. Las revisiones y validaciones locales no destructivas pueden realizarse dentro del alcance documentado.
- Mantener el trabajo limitado a equipos propios y al alcance defensivo del laboratorio.

## Cierre de cada sesión

Antes de terminar, actualizar `docs/status.md` con lo completado, la siguiente acción concreta, bloqueos y validaciones pendientes. Registrar decisiones duraderas en `docs/decisions.md`.

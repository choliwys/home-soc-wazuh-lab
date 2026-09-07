# Instrucciones del repositorio

## Contexto y fuente de verdad

- Lee primero `docs/project-context.md`, `docs/status.md` y el runbook o caso relacionado.
- `docs/status.md` define el estado operativo. No afirmes que un servicio, agente o detección funciona sin una validación documentada.
- Mantén el alcance en el laboratorio defensivo y autorizado descrito en `docs/project-context.md`.

## Seguridad

- No añadas ni solicites contraseñas, claves de agentes, certificados, tokens, IP públicas, logs privados ni archivos generados por el instalador.
- Usa placeholders y evidencia sanitizada conforme a `docs/evidence-guidelines.md`.
- Pide confirmación antes de acciones destructivas, cambios remotos, cambios de firewall, instalaciones o cualquier acción fuera de este repositorio. Las ediciones locales y validaciones no destructivas dentro del alcance están autorizadas.

## Forma de trabajo

- Define el resultado, criterios de aceptación y validación antes de cambios técnicos relevantes.
- Para comandos, documenta propósito, prerrequisitos, impacto, validación y reversión cuando aplique.
- Tras un hito, actualiza `docs/status.md`; registra decisiones duraderas en `docs/decisions.md` y enlaza evidencia o runbooks relevantes.
- Mantén las instrucciones breves, específicas y sin duplicar reglas entre archivos. Conserva el español como idioma principal de la documentación.
- Antes de cerrar, revisa enlaces Markdown y el estado de Git. No modifiques archivos no relacionados.

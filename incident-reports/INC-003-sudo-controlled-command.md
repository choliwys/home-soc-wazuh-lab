# INC-003 — Ejecución `sudo` autorizada en ejercicio controlado

## Resumen

Wazuh detectó una ejecución correcta de `sudo` para un comando de consulta en el endpoint Ubuntu. La investigación confirmó que corresponde al ejercicio autorizado `DET-003`; se cierra sin impacto operativo.

## Alcance

- Endpoint: `ubuntu-primary` (identidad sanitizada).
- Fuente: registro de `sudo` recibido desde `journald`.
- Acción controlada: ejecución única de `/usr/bin/id -u` como `root`.
- Datos omitidos: IP, hostname real, usuario local, ruta de trabajo, TTY y contenido bruto de logs.

## Evidencia

| Regla | Nivel | Hecho observado |
| --- | --- | --- |
| `5402` | 3 | Wazuh registró una ejecución correcta de `sudo` hacia `root`. |

El evento se observó en Wazuh Dashboard el 2026-09-07, se asoció al agente `ubuntu-primary` y mostró el decodificador `sudo` con el comando previsto.

## Análisis y línea de tiempo

1. Se confirmó que el agente y los servicios centrales estaban activos.
2. Se ejecutó una vez el comando de consulta autorizado mediante `sudo`.
3. Wazuh recibió el evento desde `journald` y generó la regla `5402`, de nivel 3.
4. Se compararon comando, usuario de destino y hora con `DET-003`.
5. El caso se cerró como actividad autorizada de laboratorio.

## Evaluación de impacto

No hubo impacto: el comando no cambió configuración, archivos, usuarios ni servicios. La elevación fue legítima y se limitó a consultar el identificador efectivo de `root`.

## Acción recomendada

Mantener visibilidad sobre eventos `sudo` y priorizar su investigación cuando el comando sea inusual, ocurra fuera de horario, se relacione con modificaciones de `sudoers` o sea seguido por otras acciones privilegiadas. No tratar por defecto toda ejecución correcta de `sudo` como incidente.

## Lecciones aprendidas

La telemetría disponible permite distinguir un uso administrativo esperado de una posible elevación sospechosa solo cuando se conserva el contexto de autorización y se sanitiza adecuadamente la evidencia.

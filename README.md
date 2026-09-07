# Home SOC Lab con Wazuh

Laboratorio defensivo y autorizado con Wazuh para administración Linux, visibilidad de endpoints, análisis de alertas, documentación de incidentes y automatización reproducible.

El alcance se limita a telemetría y eventos defensivos controlados en equipos y una red de laboratorio propios. No reproduce ataques ni usa sistemas, credenciales o datos corporativos.

## Logros validados

- Despliegue de Wazuh `4.14.7` en un nodo dedicado con Ubuntu Server `24.04.4 LTS`.
- Wazuh Manager, Indexer, Dashboard y Filebeat validados activos tras un reinicio controlado.
- Firewall UFW restringido a la LAN de laboratorio y acceso HTTPS al Dashboard validado.
- Endpoint Ubuntu `ubuntu-primary` inscrito y activo con Wazuh Agent `4.14.7`.
- Tres detecciones defensivas reproducibles, tres reportes de incidente sanitizados y un script Python sin dependencias externas.

## Capacidades del laboratorio

- Administración de servicios Linux con `systemd`, diagnóstico de arranque y recuperación controlada.
- Arquitectura y operación básica de Wazuh: Manager, Indexer, Dashboard, Filebeat y agentes.
- Telemetría de integridad de archivos, SSH y `sudo` en Linux.
- Investigación de alertas con contexto, clasificación de pruebas autorizadas y mapeo inicial a MITRE ATT&CK.
- Documentación técnica reproducible, sanitización de evidencias y automatización con Python.

## Arquitectura actual

```text
┌─────────────────────────────────────────────────────┐
│ Nodo central: Ubuntu Server 24.04.4 LTS              │
│ Wazuh Manager · Indexer · Dashboard · Filebeat       │
│ Acceso administrativo SSH y Dashboard por LAN privada│
└──────────────────────────┬──────────────────────────┘
                           │ Telemetría Wazuh Agent
                 ┌─────────▼─────────┐
                 │ ubuntu-primary    │
                 │ Endpoint Ubuntu   │
                 │ Activo y validado │
                 └───────────────────┘

      Endpoint Windows: diferido hasta contar con un host personal adecuado
```

La decisión de separar el nodo central del endpoint y el alcance completo están en [architecture/](architecture/) y [docs/project-context.md](docs/project-context.md).

## Detecciones y análisis

| Caso | Señal validada | Regla(s) | Evidencia y análisis |
| --- | --- | --- | --- |
| [DET-001](detections/DET-001-fim-controlled-change.md) | Creación, modificación y borrado en un directorio FIM aislado | `554`, `550`, `553` | [INC-001](incident-reports/INC-001-fim-laboratory-exercise.md) |
| [DET-002](detections/DET-002-ssh-invalid-user.md) | Intento SSH con usuario inexistente | `5710` | [INC-002](incident-reports/INC-002-ssh-invalid-user-laboratory-exercise.md) |
| [DET-003](detections/DET-003-sudo-controlled-command.md) | Ejecución controlada de un comando con `sudo` | `5402` | [INC-003](incident-reports/INC-003-sudo-controlled-command.md) |

Los tres casos se ejecutaron de forma controlada y se cerraron sin impacto operativo. Las reglas son señales para investigar, no pruebas de actividad maliciosa por sí solas.

## Automatización reproducible

El script [summarize_detections.py](scripts/summarize_detections.py) transforma datos de detecciones sanitizados en un resumen Markdown. No requiere API, credenciales ni acceso al servidor.

```bash
python3 scripts/summarize_detections.py scripts/data/validated-detections.json
```

Consulta [scripts/README.md](scripts/README.md) para prerrequisitos, validación, reversión y el formato de entrada.

## Recorrido del repositorio

- [docs/status.md](docs/status.md): estado operativo, bloqueos y próxima acción.
- [installation/](installation/): runbooks de instalación, recuperación y orden de arranque de red.
- [agents/](agents/): inscripción y validación de endpoints.
- [detections/](detections/): casos defensivos reproducibles.
- [incident-reports/](incident-reports/): análisis de los eventos observados.
- [docs/evidence-guidelines.md](docs/evidence-guidelines.md): criterios de sanitización antes de publicar evidencia.
- [docs/decisions.md](docs/decisions.md): decisiones técnicas y sus consecuencias.

## Alcance y seguridad

- Solo equipos propios y red privada de laboratorio autorizada.
- No se versionan contraseñas, claves de agente, certificados, tokens, IPs reales, logs privados, EVTX ni PCAP.
- Las capturas se recortan y sanitizan antes de añadirse a `screenshots/`.
- La configuración LAN estable se conserva fuera de Git; el endpoint Windows sigue pendiente por limitaciones de recursos, no por una incidencia de Wazuh.

## Licencia

Este repositorio se distribuye bajo la [licencia MIT](LICENSE).

## Próximos pasos

1. Documentar de forma privada una reserva DHCP o configuración LAN estable.
2. Mantener los tres casos y el script como ejercicios reproducibles.
3. Incorporar un endpoint Windows cuando exista un host personal con recursos suficientes.

El estado operativo detallado y las validaciones documentadas se mantienen en [docs/status.md](docs/status.md).

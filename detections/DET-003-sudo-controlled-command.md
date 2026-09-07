# DET-003 — Ejecución controlada de comando con `sudo`

## Objetivo

Comprobar que Wazuh recibe y clasifica una ejecución autorizada de un comando con privilegios elevados en el endpoint Ubuntu.

## Alcance y seguridad

- Endpoint: `ubuntu-primary` (identidad sanitizada), Wazuh Agent `4.14.7`.
- Acción de prueba: ejecutar `/usr/bin/id -u` mediante `sudo` una única vez.
- El comando solo muestra el identificador efectivo del usuario; no modifica archivos, cuentas, configuración ni servicios.
- La contraseña local, IP, hostname real, directorio de trabajo, TTY y logs completos no se conservan.

## Prerrequisitos

1. El agente `ubuntu-primary` debe estar `Active` en el manager.
2. El Dashboard y los servicios centrales deben estar activos.
3. La persona operadora debe tener autorización local para usar `sudo` en el endpoint.

## Generación controlada del evento

Ejecutar una vez desde una terminal nativa de `ubuntu-primary`:

```bash
sudo /usr/bin/id -u
```

Si se solicita, la contraseña se introduce únicamente en la terminal local. El resultado esperado es `0`.

## Telemetría y alerta esperadas

| Fuente | Decodificador | Regla Wazuh | Nivel | Resultado validado |
| --- | --- | --- | --- | --- |
| `journald` | `sudo` | `5402` | 3 | `Successful sudo to ROOT executed.` |

## Evidencia de validación

- Fecha de prueba: 2026-09-07.
- El Dashboard mostró el evento en el agente `001`, con nombre sanitizado `ubuntu-primary`.
- El evento registró el comando controlado `/usr/bin/id -u`, destino `root`, decodificador `sudo`, regla `5402` y nivel `3`.
- La captura original no se conserva sin sanitizar: contenía IP, nombre de usuario local, hostname, ruta de trabajo, TTY y `full_log`.

![Alerta `sudo` sanitizada para el comando controlado](../screenshots/DET-003/sudo-controlled-command.png)

## Análisis

La alerta coincide con la única ejecución planificada y con un comando de solo lectura. El evento confirma que los registros de `sudo` del endpoint llegan a Wazuh y que su contexto —comando, usuario de destino y origen— está disponible para investigación.

Por sí sola, una ejecución correcta de `sudo` no es maliciosa. Fuera de una ventana autorizada, el analista debería correlacionar el comando, la cuenta, la terminal, el horario, los cambios posteriores y posibles modificaciones de `sudoers` antes de decidir una contención.

## Mapeo MITRE ATT&CK

- `T1548.003` — [Sudo and Sudo Caching](https://attack.mitre.org/techniques/T1548/003/). El mapeo describe la elevación mediante `sudo`; el contexto controlado descarta abuso en esta prueba.

## Lecciones aprendidas

- Un comando de consulta permite validar telemetría de privilegios sin alterar el endpoint.
- Los campos de detalle de `sudo` pueden revelar datos del usuario y del host, por lo que las capturas requieren recorte y sanitización estrictos.
- Para priorizar alertas reales, la ejecución de `sudo` debe correlacionarse con el comando y la actividad posterior, no evaluarse de forma aislada.

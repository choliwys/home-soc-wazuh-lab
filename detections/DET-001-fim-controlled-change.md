# DET-001 — Integridad de archivos en directorio de laboratorio

## Objetivo

Comprobar que Wazuh detecta en tiempo real la creación, modificación y eliminación de un archivo inocuo en un endpoint Ubuntu administrado.

## Alcance y seguridad

- Endpoint: `ubuntu-primary` (nombre sanitizado), Wazuh Agent `4.14.7`.
- Directorio exclusivo y temporal: `/tmp/wazuh-lab-fim`.
- La prueba no modifica archivos de sistema ni datos de usuario, no ejecuta código y no requiere acciones ofensivas.
- No incluir en capturas la IP del agente, el hostname real, el usuario local ni hashes de archivos.

## Prerrequisitos

1. El agente debe estar `Active` en el manager.
2. Crear el grupo centralizado `linux-lab` y asignar el agente a él.
3. En `/var/ossec/etc/shared/linux-lab/agent.conf` del manager, aplicar una configuración equivalente a esta, usando primero un archivo temporal y validándola antes de publicarla:

```xml
<agent_config>
  <syscheck>
    <directories realtime="yes" check_all="yes" report_changes="yes">/tmp/wazuh-lab-fim</directories>
  </syscheck>
</agent_config>
```

4. Comprobar la sincronización con `sudo /var/ossec/bin/agent_groups -S -i <AGENT_ID>`.

Wazuh permite configurar FIM mediante `agent.conf` centralizado y el atributo `realtime` para directorios Linux. Referencias: [configuración centralizada](https://documentation.wazuh.com/current/user-manual/reference/centralized-configuration.html) y [FIM](https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/basic-settings.html).

## Generación controlada del evento

En el endpoint, tras crear el directorio temporal, generar y limpiar un archivo de prueba sin contenido sensible:

```bash
mkdir -p /tmp/wazuh-lab-fim
printf '%s\n' 'Wazuh FIM laboratory test: initial harmless content.' \
  > /tmp/wazuh-lab-fim/controlled-event.txt
sleep 5
printf '%s\n' 'Wazuh FIM laboratory test: harmless content modified for validation.' \
  > /tmp/wazuh-lab-fim/controlled-event.txt
sleep 5
rm /tmp/wazuh-lab-fim/controlled-event.txt
```

## Telemetría y alertas esperadas

| Acción | Regla Wazuh | Nivel | Resultado validado |
| --- | --- | --- | --- |
| Crear el archivo | `554` | 5 | Archivo añadido en modo `realtime` |
| Modificar el archivo | `550` | 7 | Cambio de checksum e integridad |
| Eliminar el archivo | `553` | 7 | Archivo eliminado en modo `realtime` |

La regla `550` incluyó el mapeo MITRE ATT&CK `T1565.001` y la regla `553` los mapeos `T1070.004` y `T1485`. Estos mapeos describen la señal técnica; en este caso el contexto controlado descarta actividad maliciosa.

## Evidencia de validación

- Fecha de prueba: 2026-09-01 (hora local del laboratorio).
- El agente `001` estaba `Active` y sincronizado con el grupo `linux-lab`.
- El manager registró las reglas `554`, `550` y `553` para el mismo archivo temporal.
- No se conservaron los valores de IP, hashes, usuario local, hostname ni el contenido bruto de `alerts.json`.
- El archivo de prueba fue eliminado al cerrar la validación.

## Análisis

La secuencia observada coincide con los tres cambios solicitados y la política centralizada llegó al agente antes de la prueba. No hubo indicios de un incidente real: la ruta, el contenido y la ventana temporal se definieron previamente para el laboratorio.

En un caso no autorizado, el analista debería confirmar el propietario y el proceso que causó el cambio, comparar el archivo con una versión confiable y preservar la evidencia antes de revertirlo.

## Mapeo MITRE ATT&CK

- `T1565.001` — Stored Data Manipulation, asociado por la alerta de cambio de integridad.
- `T1070.004` — File Deletion, asociado por la alerta de borrado.
- `T1485` — Data Destruction, asociado por la alerta de borrado.

## Lecciones aprendidas

- Usar un grupo de agentes evita aplicar una configuración de prueba a todos los endpoints.
- Un directorio temporal dedicado hace el ejercicio reversible y fácil de distinguir de cambios operativos.
- Una alerta de nivel 7 requiere contexto: el nivel no convierte automáticamente una prueba autorizada en incidente.

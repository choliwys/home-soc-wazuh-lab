# DET-002 — Intento SSH con usuario inexistente

## Objetivo

Comprobar que Wazuh detecta un intento de autenticación SSH con un usuario ficticio en el endpoint Ubuntu administrado.

## Alcance y seguridad

- Endpoint: `ubuntu-primary` (identidad sanitizada), Wazuh Agent `4.14.7`.
- Servicio objetivo: SSH local del mismo endpoint.
- Usuario de prueba: `soc-lab-invalid`, que no existe y no representa una cuenta real.
- La prueba genera un único intento sin contraseña; no modifica cuentas, archivos de sistema ni configuración de SSH.
- No publicar IP, hostname real, usuario local, puertos efímeros ni el contenido bruto de los logs.

## Prerrequisitos

1. El servicio SSH local del endpoint debe responder `active`.
2. El agente `ubuntu-primary` debe figurar como `Active` en el manager.
3. `wazuh-manager`, `wazuh-indexer`, `wazuh-dashboard` y `filebeat` deben estar activos, y el Dashboard debe estar disponible desde la LAN.

## Generación controlada del evento

Ejecutar una sola vez desde una terminal nativa de `ubuntu-primary`:

```bash
ssh -o BatchMode=yes -o NumberOfPasswordPrompts=0 \
  -o PreferredAuthentications=none -o PubkeyAuthentication=no \
  -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
  -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
  soc-lab-invalid@localhost
```

El fallo de la conexión es el resultado esperado. No se introduce una contraseña ni se repite el intento.

## Telemetría y alerta esperadas

| Fuente | Decodificador | Regla Wazuh | Nivel | Resultado validado |
| --- | --- | --- | --- | --- |
| `journald` | `sshd` | `5710` | 5 | `sshd: Attempt to login using a non-existent user` |

## Evidencia de validación

- Fecha de prueba: 2026-09-07.
- El Dashboard mostró un evento del agente `001` con nombre sanitizado `ubuntu-primary`.
- El evento contenía el usuario ficticio `soc-lab-invalid`, el decodificador `sshd`, la regla `5710` y nivel `5`.
- La captura original se revisó antes de conservarla: se deben ocultar IP, hostname real, puertos y el campo `full_log` antes de versionar una imagen.
- No se conservaron credenciales, claves ni logs completos.

## Análisis

La alerta coincide con el único intento planificado contra SSH local y con el usuario ficticio definido en este caso. No hubo autenticación exitosa ni evidencia de acceso no autorizado, por lo que se clasifica como ejercicio controlado y no como incidente real.

Ante un evento equivalente sin una prueba autorizada, el analista debería comprobar el origen, la frecuencia, otros intentos para la misma cuenta y si hubo inicios de sesión exitosos posteriores antes de decidir una acción de contención.

## Mapeo MITRE ATT&CK

No se asigna una técnica ATT&CK específica en este caso: un único intento con usuario inexistente es una señal de autenticación fallida, pero no demuestra por sí solo fuerza bruta ni acceso a cuentas válidas.

## Lecciones aprendidas

- Un intento local, único y sin contraseña permite validar la canalización SSH sin exponer credenciales.
- La regla y el nivel necesitan contexto: la misma señal fuera de la ventana de prueba requiere investigación.
- Las vistas detalladas del Dashboard pueden mostrar datos del endpoint; las capturas deben recortarse y sanitizarse antes de incluirlas en el repositorio.

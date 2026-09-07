# INC-002 — Intento SSH con usuario inexistente en ejercicio controlado

## Resumen

Wazuh detectó un intento de autenticación SSH con el usuario ficticio `soc-lab-invalid` en el endpoint Ubuntu del laboratorio. La revisión confirmó que el evento correspondía al procedimiento autorizado `DET-002`; se cierra como ejercicio validado, sin impacto operativo.

## Alcance

- Endpoint: `ubuntu-primary` (identidad sanitizada).
- Fuente: registro de SSH recibido desde `journald`.
- Acción controlada: un único intento local, sin contraseña, con un usuario inexistente.
- Datos omitidos: IP, hostname real, usuario local, puerto de origen y contenido bruto de logs.

## Evidencia

| Regla | Nivel | Hecho observado |
| --- | --- | --- |
| `5710` | 5 | SSH informó un intento con un usuario inexistente. |

El evento se observó en Wazuh Dashboard el 2026-09-07 y se asoció al agente `ubuntu-primary`. El decodificador registrado fue `sshd` y el usuario observado fue el valor ficticio definido para la prueba.

## Análisis y línea de tiempo

1. Se confirmó que el servicio SSH local y el agente estaban activos.
2. Se ejecutó un único intento SSH local con el usuario ficticio, sin proporcionar contraseña.
3. Wazuh recibió el evento desde `journald` y generó la regla `5710`, de nivel 5.
4. Se comparó el usuario, el origen local y la ventana temporal con `DET-002`.
5. El caso se cerró como actividad autorizada del laboratorio.

## Evaluación de impacto

No hubo impacto: no se autenticó ninguna cuenta, no se modificaron configuraciones ni archivos y no se usaron credenciales. La señal de seguridad se generó de forma intencional y limitada a un único intento.

## Acción recomendada

Conservar este caso como referencia de la telemetría SSH del endpoint Linux. Para una alerta similar no autorizada, correlacionar intentos repetidos, origen, cuentas objetivo y posibles accesos exitosos; si el patrón persiste, aplicar el procedimiento de respuesta correspondiente.

## Lecciones aprendidas

La regla `5710` confirma que los eventos SSH del endpoint alcanzan el Dashboard. El contexto previo, el usuario ficticio y la única ejecución permiten diferenciar una validación de laboratorio de una actividad que requiere investigación.

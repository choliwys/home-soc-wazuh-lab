# INC-001 — Cambios de integridad en ejercicio controlado

## Resumen

Wazuh detectó la creación, modificación y eliminación de un archivo en el directorio temporal del laboratorio. La investigación confirmó que las tres alertas procedían de la prueba autorizada `DET-001`; el caso se cierra como ejercicio validado, sin impacto operativo.

## Alcance

- Endpoint: `ubuntu-primary` (identidad sanitizada).
- Fuente: File Integrity Monitoring (Syscheck) de Wazuh.
- Ruta de laboratorio: `/tmp/wazuh-lab-fim/controlled-event.txt`.
- Datos omitidos: IP, hostname real, usuario, hashes y contenido bruto de alertas.

## Evidencia

| Regla | Nivel | Hecho observado |
| --- | --- | --- |
| `554` | 5 | Se añadió el archivo temporal. |
| `550` | 7 | Se modificó el contenido controlado. |
| `553` | 7 | Se eliminó el archivo temporal. |

El agente estaba activo y sincronizado con su grupo de configuración antes de la prueba.

## Análisis y línea de tiempo

1. Se creó y sincronizó la política FIM exclusiva para `linux-lab`.
2. Se creó un archivo inocuo en el directorio temporal y Wazuh produjo la alerta `554`.
3. Se sustituyó su contenido por otra cadena inocua y Wazuh produjo la alerta `550`.
4. Se eliminó el archivo al finalizar y Wazuh produjo la alerta `553`.
5. Se comparó la secuencia con el procedimiento aprobado en `DET-001` y se cerró el caso.

## Evaluación de impacto

No hubo impacto: no se modificaron archivos de sistema, datos de usuario ni servicios. Los cambios ocurrieron solo en el directorio temporal reservado para la prueba.

## Acción recomendada

Mantener la configuración FIM en el grupo `linux-lab` para futuros ejercicios, pero no reutilizar esa ruta para datos reales. Ante una alerta equivalente fuera de la ruta de laboratorio, investigar propietario, proceso, integridad del archivo y cambios relacionados antes de tomar acciones de contención.

## Lecciones aprendidas

La secuencia completa demuestra que la telemetría del endpoint, la configuración centralizada y el pipeline de alertas funcionan. El contexto documentado evita clasificar erróneamente una prueba controlada como actividad maliciosa.

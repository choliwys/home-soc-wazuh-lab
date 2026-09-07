# Contexto del proyecto

## Propósito del proyecto

Este Home SOC Lab usa Wazuh para practicar y documentar tareas defensivas de Blue Team: visibilidad de endpoints, análisis de logs, validación de alertas, documentación y automatización básica.

No es un laboratorio de pentesting ni pretende emular una operación SOC empresarial completa.

## Alcance técnico

| Componente | Rol | Estado |
| --- | --- | --- |
| Laptop secundaria | Nodo central con Ubuntu Server 24.04 LTS, Wazuh server, indexer y dashboard | Componentes centrales activos; dashboard validado por HTTPS desde la LAN; endurecimiento básico aplicado |
| Laptop principal | Endpoint Ubuntu con Wazuh agent | Agente `4.14.7` inscrito y activo; monitorización de integridad validada |
| VM Windows | Segundo endpoint con Wazuh agent | Pendiente de crear |
| LAN privada | Conectividad exclusiva del laboratorio | Dashboard y agente Ubuntu validados; reserva DHCP/configuración persistente pendiente |

## Entregables mínimos para considerar el proyecto completo

1. Nodo Wazuh funcional y documentado con versiones, método de instalación y validaciones.
2. Agentes Ubuntu y Windows conectados y visibles en el dashboard.
3. Tres o cuatro casos de detección seguros, reproducibles y documentados.
4. Evidencia sanitizada para cada caso relevante.
5. Al menos dos reportes de incidente basados en las alertas del laboratorio.
6. Un script Python pequeño que produzca un resumen o reporte reproducible.
7. README actualizado con el alcance, las validaciones y el recorrido técnico del repositorio.

## Restricciones y seguridad

- Solo equipos propios, VMs propias y una red de laboratorio autorizada.
- No ejecutar pruebas ofensivas ni acciones fuera del alcance defensivo documentado.
- No versionar credenciales, claves de agentes, certificados, tokens, archivos de instalación con secretos, logs privados, EVTX, PCAP ni IP públicas.
- Usar placeholders en documentación pública: `<WAZUH_MANAGER_IP>`, `<LAB_HOSTNAME>` y `<LAB_USER>`.
- Sanitizar capturas antes de versionarlas.

## Criterios de calidad

- Cada cambio debe ser reproducible, validado y documentado.
- Las versiones de Wazuh, sistema operativo y fecha de prueba deben quedar registradas.
- Los casos de detección deben describir qué se generó, qué alerta se observó, cómo se investigó y qué se recomienda.
- No afirmar una capacidad o un resultado que no tenga evidencia en el repositorio.

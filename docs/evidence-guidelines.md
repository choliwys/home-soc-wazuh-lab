# Guía de evidencias

## Qué conservar por cada caso

- Fecha y versión de Wazuh.
- Endpoint y sistema operativo, usando un nombre sanitizado.
- Acción controlada que generó el evento.
- Fuente de log y alerta observada.
- Captura del dashboard o salida de comando relevante, sanitizada.
- Resultado del análisis y recomendación.

## Qué nunca publicar

- Contraseñas, API keys, claves de agentes, certificados o archivos `wazuh-install-files.tar`.
- IP públicas, dominios personales, correos, nombres reales de usuario o información corporativa.
- Logs completos que puedan contener datos personales.
- Archivos `.evtx`, `.pcap`, `.pcapng` o logs privados sin una revisión explícita.

## Sanitización mínima

1. Sustituir IPs y nombres por placeholders coherentes, por ejemplo `<LINUX_AGENT_IP>`.
2. Recortar capturas para mostrar solo la evidencia necesaria.
3. Revisar la barra del navegador, rutas de archivos, hostnames y nombres de usuario antes de versionar.
4. Guardar las imágenes en `screenshots/<case-id>/` y enlazarlas desde la detección o el reporte correspondiente.

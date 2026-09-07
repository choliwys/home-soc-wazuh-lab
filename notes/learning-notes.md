# Learning Notes

## ¿Qué es Wazuh?

Es una plataforma open source de seguridad, combina capacidades de SIEM y XDR, recolecta logs, eventos (SIEM) y puede actuar ante cualquier evento malicioso (XDR).

## Componentes Principales

- Wazuh server: incluye Wazuh manager, que recibe y analiza la información de los agentes, y Filebeat.
- Wazuh Indexer: almacena e indexa datos para búsquedas.
- Wazuh Dashboard: interfaz web para revisar agentes, eventos y alertas.
- Wazuh Agent: componente instalado en los endpoints que se quieren monitorear.


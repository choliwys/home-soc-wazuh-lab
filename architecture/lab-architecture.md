# Lab Architecture

## Objetivo

Diseñar una arquitectura inicial para un laboratorio SOC casero usando Wazuh.

## Arquitectura inicial

```text
┌──────────────────────────────┐
│        Wazuh Server           │
│ Ubuntu Server                 │
│ Wazuh Manager + Indexer       │
│ Wazuh Dashboard               │
└───────────────┬──────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼──────┐  ┌──────▼───────┐
│ Linux Agent  │  │ Windows Agent│
│ Ubuntu       │  │ Windows      │
└──────────────┘  └──────────────┘

## Componentes
- Wazuh Server: Servidor central encargado de recibir, procesar y analizar eventos enviados por los agentes.
- Wazuh Indexer: Componente encargado de almacenar e indexar los eventos y alertas.
- Wazuh Dashboard: Interfaz web para revisar agentes, alertas, eventos y configuraciones.
- Wazuh Agent: Agente instalado en los endpoints para recolectar eventos y enviarlos al servidor.

## Alcance inicial
- 1 servidor Wazuh.
- 1 agente Linux.
- 1 agente Windows.
- Eventos de autenticación.
- File Integrity Monitoring.
- Reportes básicos de incidente.



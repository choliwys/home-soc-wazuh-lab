# Arquitectura del laboratorio

## Objetivo

Diseñar una arquitectura inicial para un laboratorio SOC casero usando Wazuh.

## Arquitectura inicial

```text
┌──────────────────────────────┐
│       Nodo central Wazuh      │
│ Ubuntu Server 24.04 LTS       │
│ Manager + Filebeat            │
│ Indexer + Dashboard           │
└───────────────┬──────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼──────┐  ┌──────▼───────┐
│ Agente Linux │  │ Agente Windows│
│ Activo       │  │ Diferido      │
└──────────────┘  └──────────────┘
```

El endpoint Linux corresponde a `ubuntu-primary` y se validó activo. El endpoint Windows forma parte del objetivo final, pero se difiere hasta contar con un host personal con recursos suficientes.
## Componentes
- Wazuh server: componente central que incluye Wazuh manager, encargado de recibir, procesar y analizar los eventos enviados por los agentes, y Filebeat.
- Wazuh Indexer: Componente encargado de almacenar e indexar los eventos y alertas.
- Wazuh Dashboard: Interfaz web para revisar agentes, alertas, eventos y configuraciones.
- Wazuh Agent: Agente instalado en los endpoints para recolectar eventos y enviarlos al servidor.

## Alcance inicial
- 1 servidor Wazuh.
- 1 agente Linux activo y validado.
- 1 agente Windows planificado y diferido.
- Eventos de autenticación, integridad de archivos y uso controlado de `sudo`.
- Tres reportes básicos de incidente y un resumen automatizado.

# Decisión de entorno

## Objetivo

Definir el entorno más adecuado para instalar Wazuh en el laboratorio SOC y separar sus recursos de los endpoints.

## Opciones evaluadas

### Opción 1: instalar Wazuh en la laptop principal

- Recursos observados durante la evaluación: 7.2 GiB de RAM total, aproximadamente 2.9 GiB disponibles y 134 GiB libres.
- CPU: ocho hilos lógicos con capacidad VT-x.
- El dispositivo KVM no estaba disponible durante la evaluación.

Esta opción no fue seleccionada porque la memoria disponible es limitada para ejecutar Wazuh Server, Wazuh Indexer y Wazuh Dashboard en el mismo host. Tampoco es un host adecuado para una VM Windows junto con la carga habitual del endpoint.

### Opción 2: usar una segunda laptop como servidor dedicado

- RAM total: 12 GB
- Sistema operativo objetivo: Ubuntu Server 24.04 LTS
- Rol: Wazuh Server
- Endpoints monitoreados: laptop Linux principal y futura VM Windows

Esta opción fue seleccionada porque permite separar el servidor Wazuh de los endpoints monitoreados, mejora el rendimiento y hace que la arquitectura del laboratorio sea más realista.

## Decisión

Usaré la segunda laptop como servidor Wazuh dedicado con Ubuntu Server 24.04 LTS. La laptop principal será usada como agente Linux y estación de trabajo para documentación, GitHub y análisis. La VM Windows queda diferida hasta disponer de un host personal con recursos suficientes.

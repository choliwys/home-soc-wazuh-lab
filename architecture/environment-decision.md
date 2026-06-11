# Environment Decision

## Objetivo

Definir el entorno más adecuado para instalar Wazuh en el laboratorio SOC.

## Opciones evaluadas

### Opción 1: instalar Wazuh en la laptop principal

- RAM total: 7.2 GiB
- RAM disponible: 2.6 GiB
- CPU: Intel Core i5-9300HF
- Disco disponible: 400 GB
- Sistema operativo: Ubuntu 26.04

Esta opción no fue seleccionada porque la memoria disponible es limitada para ejecutar Wazuh Server, Wazuh Indexer y Wazuh Dashboard en el mismo host. Además, Ubuntu 26.04 no aparece dentro de las versiones recomendadas por la documentación oficial de Wazuh para los componentes centrales.

### Opción 2: usar una segunda laptop como servidor dedicado

- RAM total: 12 GB
- Sistema operativo objetivo: Ubuntu Server 24.04 LTS
- Rol: Wazuh Server
- Endpoints monitoreados: laptop Linux principal y futura VM Windows

Esta opción fue seleccionada porque permite separar el servidor Wazuh de los endpoints monitoreados, mejora el rendimiento y hace que la arquitectura del laboratorio sea más realista.

## Decisión

Usaré la segunda laptop como servidor Wazuh dedicado con Ubuntu Server 24.04 LTS. La laptop principal será usada como agente Linux y estación de trabajo para documentación, GitHub y análisis.

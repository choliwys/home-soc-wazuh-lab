# Home SOC Lab with Wazuh

Estoy construyendo un laboratorio SOC casero usando Wazuh para aprender ciberseguridad defensiva desde la práctica.

El objetivo es monitorear endpoints, revisar logs, generar alertas, analizar eventos y documentar reportes básicos de incidente como lo haría un analista SOC junior.

## Objetivos del proyecto

- Instalar y configurar Wazuh en un entorno de laboratorio.
- Conectar agentes Windows y Linux.
- Generar eventos de seguridad controlados.
- Analizar alertas desde el dashboard.
- Documentar hallazgos y reportes de incidente.
- Automatizar reportes básicos con Python.

## Arquitectura inicial

- Wazuh Server en Ubuntu.
- Agente Linux.
- Agente Windows.
- Red local de laboratorio.

## Casos que voy a documentar

- Intentos fallidos de inicio de sesión.
- Cambios en archivos monitoreados.
- Eventos de seguridad en Windows.
- Alertas de autenticación en Linux.
- Inventario básico del sistema.
- Análisis de logs y mapeo inicial con MITRE ATT&CK.

## Estructura del repositorio

```text
home-soc-wazuh-lab/
├── architecture/
├── installation/
├── agents/
├── detections/
├── incident-reports/
├── screenshots/
├── scripts/
├── notes/
└── ai-prompts/

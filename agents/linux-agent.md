# Agente Linux — endpoint Ubuntu

## Objetivo

Registrar un endpoint Ubuntu en el manager Wazuh del laboratorio y comprobar que el agente transmite su estado sin guardar secretos, claves de agente ni direcciones reales.

## Alcance

- Endpoint propio Ubuntu de la estación de trabajo principal.
- Manager Wazuh de la LAN privada, referido como `<WAZUH_MANAGER_IP>`.
- Versión validada: Wazuh Agent `4.14.7` para coincidir con el nodo central.

## Instalación reproducible

Configurar el repositorio oficial de Wazuh y, desde una terminal local del endpoint, instalar la versión indicada con una identidad de laboratorio:

```bash
sudo env WAZUH_MANAGER="<WAZUH_MANAGER_IP>" WAZUH_AGENT_NAME="ubuntu-primary" \
  apt-get install -y wazuh-agent=4.14.7-1
sudo systemctl enable --now wazuh-agent
sudo systemctl status wazuh-agent --no-pager
```

Tras validar la instalación, deshabilitar el repositorio Wazuh para evitar actualizaciones no planificadas:

```bash
sudo sed -i 's/^deb /#deb /' /etc/apt/sources.list.d/wazuh.list
sudo apt-get update
```

No copiar a Git el contenido de `/var/ossec/etc/client.keys`, certificados ni archivos de configuración que incluyan una IP real.

## Validación en el manager

En el nodo central:

```bash
sudo /var/ossec/bin/agent_control -l
sudo /var/ossec/bin/agent_control -i <AGENT_ID>
```

Resultado registrado el 2026-09-01:

- El agente `001`, con nombre sanitizado `ubuntu-primary`, figura como `Active`.
- La versión de cliente es `4.14.7`.
- El agente completó una ejecución de monitorización de integridad (Syscheck).
- El hostname real, la dirección IP y las claves de inscripción no se registraron.

## Siguiente uso

Este endpoint ya validó el caso [DET-001](../detections/DET-001-fim-controlled-change.md). Utilizarlo ahora para una detección defensiva de autenticación Linux y conservar únicamente capturas y salidas sanitizadas conforme a [la guía de evidencias](../docs/evidence-guidelines.md).

# Estado del proyecto

> Actualizar este archivo al inicio y al cierre de cada hito técnico. Es el estado operativo del proyecto.
>
> Última actualización documental: 2026-09-07. Las validaciones indicadas se realizaron contra el nodo central mediante SSH y HTTPS desde la LAN.

## Hito actual

**Fase 2 — nodo central y agente Ubuntu operativos; tres casos de detección validados.**

## Completado

- [x] Definir el objetivo profesional y el alcance defensivo del laboratorio.
- [x] Elegir una laptop secundaria con Ubuntu Server 24.04 LTS como nodo central.
- [x] Diseñar la arquitectura inicial con dos endpoints previstos.
- [x] Definir controles básicos para no publicar secretos ni evidencias sensibles.
- [x] Crear la estructura documental y las plantillas de trabajo.
- [x] Instalar Ubuntu Server 24.04.4 LTS en la laptop secundaria.
- [x] Validar capacidad inicial del nodo: 11 GiB RAM, cuatro CPU y 86 GB libres.
- [x] Conectar el nodo central a la LAN mediante Wi-Fi y validar salida a Internet/DNS.
- [x] Habilitar y validar el servicio SSH.
- [x] Definir el hostname sanitizado `wazuh-lab`.
- [x] Crear una clave SSH administrativa para esta sesión de trabajo y validarla en `authorized_keys`.
- [x] Instalar y configurar manualmente el stack base de Wazuh: indexer, manager y Filebeat.
- [x] Generar y desplegar los certificados del laboratorio en el nodo central.
- [x] Validar que el indexer responde y que el manager inicia correctamente.
- [x] Validar que Filebeat conecta al indexer y que vigila `alerts.json`.
- [x] Recuperar el acceso SSH al nodo mediante la dirección LAN actual.
- [x] Corregir las referencias de la IP anterior en Indexer, Manager, Filebeat y Dashboard.
- [x] Regenerar y desplegar certificados internos para la dirección LAN actual, sin versionarlos.
- [x] Recuperar `wazuh-indexer` y validar que responde por HTTPS.
- [x] Completar y levantar `wazuh-dashboard`; el dashboard responde por HTTPS desde la LAN.
- [x] Iniciar sesión en Wazuh Dashboard desde la LAN con la cuenta administrativa inicial.
- [x] Rotar las credenciales administrativas iniciales y validar la comunicación interna de Dashboard, Manager, Filebeat e Indexer.
- [x] Aplicar y validar UFW con acceso limitado a la LAN para administración, dashboard e inscripción de agentes.
- [x] Instalar Wazuh Agent `4.14.7` en el endpoint Ubuntu con nombre sanitizado `ubuntu-primary`.
- [x] Validar en el manager que el agente `001` está `Active` y ejecutó monitorización de integridad (Syscheck).
- [x] Aplicar una política FIM centralizada y aislada al grupo `linux-lab`.
- [x] Validar las alertas FIM de creación (`554`), modificación (`550`) y borrado (`553`) con una prueba inocua.
- [x] Documentar el caso `DET-001` y el reporte sanitizado `INC-001`.
- [x] Recuperar `wazuh-indexer` y `wazuh-dashboard` mediante reinicio controlado tras un arranque incompleto; los cuatro servicios centrales quedaron `active`.
- [x] Validar una alerta SSH de usuario inexistente (regla `5710`, nivel 5) con un único intento local sin contraseña en el endpoint Ubuntu.
- [x] Documentar el caso `DET-002` y el reporte sanitizado `INC-002`.
- [x] Sustituir la espera incompatible de `systemd-networkd` por una espera local de la Wi-Fi administrada por NetworkManager Snap y validarla tras un reinicio controlado.
- [x] Validar una alerta de ejecución controlada con `sudo` (regla `5402`, nivel 3) en el endpoint Ubuntu.
- [x] Documentar el caso `DET-003` y el reporte sanitizado `INC-003`.
- [x] Crear y validar un script Python que genera un resumen reproducible desde datos de detecciones sanitizados.
- [x] Revisar el repositorio como portafolio: README orientado a reclutadores, coherencia documental, enlaces locales, salida del script y ausencia de patrones sensibles.
- [x] Añadir licencia MIT para aclarar las condiciones de reutilización del repositorio público.

## Siguiente hito

Mantener la asignación LAN estable documentada de forma privada y diferir el endpoint Windows hasta contar con un host personal adecuado. El portafolio ya reúne los casos, reportes, automatización y controles de publicación del alcance actual.

### Criterios de salida

- [x] Ubuntu Server 24.04 LTS instalado y actualizado.
- [x] Hostname de laboratorio definido y documentado de forma sanitizada.
- [x] Conectividad LAN comprobada desde el endpoint Ubuntu.
- [ ] IP LAN reservada o documentada sin publicar valores sensibles.
- [x] CPU, RAM y espacio de disco disponibles registrados de forma sanitizada.
- [x] Acceso SSH administrativo validado.
- [x] Reglas de firewall necesarias planificadas y verificadas.
- [x] Conectividad de red tras el reinicio confirmada.
- [x] `wazuh-dashboard` recuperado y activo.
- [x] Credenciales por defecto reemplazadas por credenciales seguras.
- [x] Versiones finales y método manual de instalación documentados sin secretos.

## Bloqueos conocidos

- Falta confirmar la reserva DHCP o la configuración persistente de la dirección LAN actual y documentarla fuera de Git.
- La VM Windows todavía no está creada y queda diferida: el nodo central no dispone de recursos suficientes para alojarla de forma estable y no se usará una laptop de trabajo sin autorización explícita.

## Próxima acción concreta

Obtener acceso autorizado al router y registrar una reserva DHCP de forma privada. Retomar la VM Windows solo cuando exista un host personal con recursos suficientes; antes de inscribirla, validar recursos, conectividad LAN y autorización de uso.

### Punto de reanudación

- `DET-001`/`INC-001` y `DET-002`/`INC-002` están cerrados; la configuración FIM del grupo `linux-lab` permanece activa.
- El evento de `DET-002` se validó el 2026-09-07: el Dashboard mostró la regla `5710` de nivel 5 para el usuario ficticio `soc-lab-invalid` en `ubuntu-primary`.
- Tras el arranque incompleto, `wazuh-indexer` y `wazuh-dashboard` se recuperaron con un reinicio controlado y los cuatro servicios centrales quedaron `active`.
- El 2026-09-07 se deshabilitó `systemd-networkd-wait-online.service` y se habilitó `wazuh-wifi-online.service`, que espera que `wlo1` esté conectada según NetworkManager Snap. Tras un reinicio controlado, esa unidad y los cuatro servicios Wazuh quedaron `active`, no hubo unidades fallidas y el agente Ubuntu continuó `Active`.
- La VM Windows se difiere por falta de un host personal adecuado; el avance inmediato continuará con el único endpoint Ubuntu inscrito.
- `DET-003`/`INC-003` se validaron el 2026-09-07: el Dashboard mostró la regla `5402`, de nivel 3, para la ejecución controlada de `/usr/bin/id -u` con `sudo` en `ubuntu-primary`.
- El script `scripts/summarize_detections.py` se añadió con un JSON de ejemplo sanitizado para resumir `DET-001` a `DET-003` sin acceder a Wazuh ni a logs privados.
- La revisión de portafolio confirmó enlaces locales correctos, ejecución esperada del script, ausencia de patrones de IP, MAC o claves privadas y documentación alineada con el estado validado.
- El portafolio incorpora licencia MIT y está preparado para publicación sin incluir secretos, evidencias privadas ni archivos generados por Wazuh.

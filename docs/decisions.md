# Registro de decisiones de arquitectura

Las decisiones se registran aquí para que el laboratorio sea explicable y reproducible.

## ADR-001 — Nodo Wazuh dedicado

- **Estado:** aceptada.
- **Decisión:** usar la laptop secundaria con Ubuntu Server 24.04 LTS como nodo único para Wazuh server, indexer y dashboard.
- **Motivación:** separar los componentes centrales de los endpoints, disponer de memoria suficiente y mantener una arquitectura representativa para un laboratorio pequeño.
- **Consecuencia:** el laboratorio no busca alta disponibilidad; la disponibilidad depende de un solo host.
- **Validación:** el nodo registró 11 GiB de RAM, cuatro CPU y 86 GB libres; supera el objetivo mínimo del laboratorio. La conectividad desde los endpoints sigue pendiente.

## ADR-002 — Endpoints iniciales

- **Estado:** aceptada.
- **Decisión:** monitorear una laptop Ubuntu como endpoint Linux y una VM Windows como segundo endpoint.
- **Motivación:** cubrir fuentes de telemetría Linux y Windows sin ampliar el alcance más de lo necesario.
- **Consecuencia:** las primeras detecciones priorizarán autenticación, FIM e inventario.

## ADR-003 — Alcance de detecciones

- **Estado:** aceptada.
- **Decisión:** documentar pocos escenarios controlados, reproducibles y suficientemente analizados.
- **Motivación:** la profundidad de análisis y la evidencia validada aportan más valor técnico que un volumen alto de alertas.
- **Escenarios iniciales:** autenticaciones fallidas Linux, FIM controlado, inventario de endpoints y eventos de autenticación Windows.

## ADR-004 — Gestión de información sensible

- **Estado:** aceptada.
- **Decisión:** excluir secretos y datos privados del repositorio, y usar placeholders o datos sanitizados en toda evidencia pública.
- **Motivación:** el repositorio debe ser seguro de compartir y demostrar buenas prácticas.

## ADR-005 — Despliegue manual del núcleo de Wazuh

- **Estado:** aceptada.
- **Decisión:** conservar el despliegue manual de indexer, manager y Filebeat realizado en el nodo central en lugar de reiniciar el despliegue con el asistente todo-en-uno.
- **Motivación:** el asistente no completó su fase de servidor por una inconsistencia de usuarios API generados. Los componentes manuales quedaron instalados y validados; el Dashboard se recuperó posteriormente mediante el runbook correspondiente.
- **Consecuencia:** documentar las versiones y los pasos manuales validados tras recuperar el dashboard, sin incluir secretos ni certificados.
- **Actualización:** al cambiar la dirección LAN del nodo, se regeneraron los certificados internos y se actualizaron las referencias de red de Indexer, Manager, Filebeat y Dashboard. El indexer y dashboard se validaron por HTTPS desde la LAN.

## ADR-006 — Firewall de mínimo privilegio en la LAN

- **Estado:** aceptada.
- **Decisión:** habilitar UFW con entrada denegada por defecto y salida permitida. Permitir desde la LAN privada solo SSH (22/TCP), Dashboard (443/TCP), comunicación e inscripción de agentes (1514/TCP y 1515/TCP) y API de inscripción (55000/TCP). Restringir el Indexer (9200/TCP) al propio nodo.
- **Motivación:** reducir la superficie expuesta sin impedir la administración ni el alta de agentes autorizados.
- **Validación:** UFW quedó activo; SSH y Dashboard siguieron accesibles desde la LAN y los cuatro servicios centrales permanecieron activos.

## ADR-007 — Configuración FIM centralizada por grupo de laboratorio

- **Estado:** aceptada.
- **Decisión:** aplicar la política FIM de los ejercicios mediante el grupo de agentes `linux-lab`, en lugar de modificar la configuración base o el grupo `default`.
- **Motivación:** aislar las configuraciones de prueba, facilitar su revisión y evitar que futuros endpoints reciban reglas de laboratorio por accidente.
- **Consecuencia:** cada nueva política requiere validación de sincronización antes de generar eventos; las rutas de prueba deben ser exclusivas y reversibles.
- **Validación:** el agente Ubuntu se sincronizó con el grupo y produjo las alertas FIM esperadas para crear, modificar y eliminar un archivo temporal.

## ADR-008 — Espera de red compatible con NetworkManager Snap

- **Estado:** aceptada y validada.
- **Decisión:** deshabilitar `systemd-networkd-wait-online.service` y usar la unidad local `wazuh-wifi-online.service` para que `network-online.target` espere a que `wlo1` esté `connected`, consultando el NetworkManager instalado como Snap.
- **Motivación:** la Wi-Fi del nodo es administrada por `snap.network-manager.networkmanager.service`, mientras que `systemd-networkd` la reporta como no administrada. La unidad de espera de `systemd-networkd` agotó el tiempo de espera y Wazuh Indexer intentó enlazar su dirección LAN antes de que estuviera disponible.
- **Consecuencia:** el nombre de interfaz `wlo1` queda como dependencia explícita de la unidad local y debe revisarse si cambia el hardware o la configuración de red. La recuperación queda documentada en [04-network-startup-order.md](../installation/04-network-startup-order.md).
- **Validación:** la unidad local quedó habilitada y terminó correctamente con la Wi-Fi conectada. Tras un reinicio controlado, la unidad y Manager, Indexer, Dashboard y Filebeat mostraron `active`; no quedaron unidades fallidas y el agente Ubuntu continuó `Active`.

## ADR-009 — Documentación técnica y prompts locales separados

- **Estado:** aceptada.
- **Decisión:** mantener la documentación versionada centrada en el alcance, la operación y las validaciones del laboratorio; excluir `ai-prompts/` del control de versiones.
- **Motivación:** los prompts son material personal y cambiante, mientras que el repositorio debe conservar una fuente de verdad técnica, neutral y revisable.
- **Consecuencia:** los prompts locales no se publican ni se usan como referencia operativa; `docs/` y `AGENTS.md` mantienen ese rol.
- **Validación:** se retiraron las referencias de orientación profesional y `ai-prompts/` quedó ignorado y sin archivos rastreados.

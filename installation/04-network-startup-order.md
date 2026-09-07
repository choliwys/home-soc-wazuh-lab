# 04 — Espera de red antes de Wazuh Indexer

## Objetivo

Evitar que `wazuh-indexer` intente enlazar la dirección LAN antes de que la Wi-Fi del nodo central esté conectada durante el arranque.

## Diagnóstico registrado

El nodo usa NetworkManager empaquetado como Snap para administrar `wlo1`. La unidad `systemd-networkd-wait-online.service` no administra esa interfaz y agotó su espera durante el arranque. Wazuh Indexer ya declara `Wants=` y `After=` sobre `network-online.target`; el problema era la fuente que determinaba que la red estaba lista.

## Cambio aplicado — 2026-09-07

Se deshabilitó `systemd-networkd-wait-online.service` y se añadió una unidad local, `wazuh-wifi-online.service`, habilitada por `network-online.target`. Su script `/usr/local/sbin/wazuh-wait-for-wifi` consulta `/snap/bin/nmcli` y espera, como máximo, 180 segundos a que `wlo1` esté `connected`.

El cambio no modifica perfiles Wi-Fi, direcciones, firewall ni configuración de Wazuh. Si cambia el nombre de la interfaz inalámbrica, se debe revisar la variable `interface_name` del script antes de reiniciar.

## Prerrequisitos

- Acceso administrativo por consola local o SSH recuperable.
- Confirmar que `wlo1` es la interfaz Wi-Fi del laboratorio mediante `nmcli -t -f DEVICE,STATE device status`.
- Confirmar que NetworkManager Snap está activo mediante `snap services network-manager`.

## Validación actual

Sin reiniciar, se verificó que:

- `systemd-networkd-wait-online.service` quedó `disabled`.
- `wazuh-wifi-online.service` quedó `enabled` y terminó con `active (exited)`.
- `wazuh-manager`, `wazuh-indexer`, `wazuh-dashboard` y `filebeat` permanecieron `active`.

## Validación tras un reinicio planificado — 2026-09-07

Tras confirmar una ventana de mantenimiento y acceso alternativo al nodo, comprobar:

```bash
sudo systemctl is-active wazuh-wifi-online wazuh-manager wazuh-indexer wazuh-dashboard filebeat
sudo systemctl --failed
sudo /var/ossec/bin/agent_control -l
```

Resultado validado: los cinco servicios mostraron `active`, no aparecieron unidades fallidas y el agente Ubuntu continuó `Active` tras el reinicio controlado.

## Reversión

Si la nueva unidad impide alcanzar `network-online.target`, desde consola local o una sesión SSH recuperable:

```bash
sudo systemctl disable --now wazuh-wifi-online.service
sudo systemctl enable systemd-networkd-wait-online.service
sudo systemctl daemon-reload
```

La reversión recupera el comportamiento anterior, que puede volver a agotar el tiempo de espera; conservar la salida sanitizada para investigar antes de un nuevo intento.

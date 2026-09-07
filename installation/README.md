# Installation Runbooks

Esta carpeta contendrá los runbooks reproducibles para preparar e instalar el nodo central Wazuh.

Estado y orden de trabajo:

1. `01-server-prerequisites.md` — sistema base validado; faltan pruebas desde endpoints y reserva DHCP.
2. `02-wazuh-single-node-installation.md` — indexer, manager y Filebeat instalados; el intento inicial con asistente quedó registrado como no completado.
3. `03-dashboard-recovery.md` — recuperación completada y resultado registrado.
4. `../agents/linux-agent.md` — credenciales rotadas, firewall verificado y primer agente Ubuntu incorporado.
5. `04-network-startup-order.md` — corrección reversible de la espera de red para el NetworkManager instalado como Snap; validada tras un reinicio controlado.

No incluir contraseñas, certificados ni archivos generados por el instalador.

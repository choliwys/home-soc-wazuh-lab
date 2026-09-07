# 02 — Wazuh single-node installation

## Objective

Registrar el despliegue inicial del núcleo de Wazuh en `wazuh-lab` y su estado de validación. El dashboard se recupera en el runbook siguiente; no reiniciar esta instalación sin una decisión documentada.

## Scope and safety

- Target: the secondary Ubuntu Server 24.04 LTS laptop, owned by the project owner.
- The documented sizing (4 CPU cores, 11 GiB RAM, and 86 GB free) meets the Wazuh quickstart recommendation for 1–25 agents.
- Perform this runbook from the server console or an SSH session that can be re-established locally.
- Do not commit `wazuh-install-files.tar`, `wazuh-passwords.txt`, certificates, private keys, dashboard passwords, real IP addresses, or screenshots containing them.

Reference: [Wazuh Quickstart](https://documentation.wazuh.com/current/quickstart.html).

## 1. Pre-flight checks

On the central node, confirm the operating system is healthy and Wazuh's download endpoint resolves:

```bash
hostnamectl
systemctl is-system-running
uname -m
free -h
nproc
df -h /
getent ahosts packages.wazuh.com | head
```

Expected outcome:

- `wazuh-lab` on Ubuntu Server 24.04 LTS, 64-bit.
- System state is `running` (or only expected non-critical startup states).
- At least 8 GiB RAM, 4 CPU cores, and 50 GB free.
- DNS resolves `packages.wazuh.com`.

Apply normal operating-system updates if they are pending, then reboot before continuing:

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

## 2. Intento inicial con asistente (registro histórico)

El siguiente procedimiento fue el camino inicial previsto con el asistente oficial. No se completó: la fase del servidor falló porque faltaban usuarios API generados en esa ruta. El núcleo se reconstruyó manualmente; por ello, **no volver a ejecutar este bloque sobre el nodo actual**. Se conserva para explicar el origen del despliegue y como referencia para una reconstrucción futura, previa revisión de la documentación oficial vigente.

After reconnecting, create a root-owned working directory. It will contain installation material that must stay outside this Git repository:

```bash
sudo -i
install -d -m 700 /root/wazuh-install
cd /root/wazuh-install
curl -fL --retry 3 -o wazuh-install.sh https://packages.wazuh.com/4.14/wazuh-install.sh
ls -lh wazuh-install.sh
bash ./wazuh-install.sh -a
```

Wait for the command to finish. The assistant prints the dashboard URL and the generated `admin` password in its final summary. Record that password only in a private password manager; do not paste it into chat, screenshots, or the repository.

## 3. Firewall de LAN (validado)

First inspect whether UFW is enabled:

```bash
sudo ufw status verbose
```

If it is active, preserve SSH access and permit the dashboard and agent ports from the private LAN only. Replace `<LAN_CIDR>` locally, without committing it:

```bash
sudo ufw allow from <LAN_CIDR> to any port 22 proto tcp
sudo ufw allow from <LAN_CIDR> to any port 443 proto tcp
sudo ufw allow from <LAN_CIDR> to any port 1514 proto tcp
sudo ufw allow from <LAN_CIDR> to any port 1515 proto tcp
sudo ufw status numbered
```

Port 1514/TCP receives agent data and 1515/TCP supports automatic enrollment. Keep ports 55000 and 9200 limited to the host unless a later documented use case requires otherwise.

### Resultado registrado — 2026-09-01

UFW está activo con entrada denegada por defecto. Desde la LAN privada se permiten 22/TCP, 443/TCP, 1514/TCP, 1515/TCP y 55000/TCP. El puerto 9200/TCP se limita al propio nodo. Tras aplicar las reglas, SSH, Dashboard y todos los servicios Wazuh se validaron correctamente.

## 4. Estado de validación actual

Run:

```bash
sudo systemctl --no-pager --full status wazuh-manager wazuh-indexer wazuh-dashboard
sudo ss -ltnp | grep -E ':(443|1514|1515|55000|9200)\\b'
```

Validado antes del reinicio:

- `wazuh-indexer` responde.
- `wazuh-manager` inicia correctamente.
- Filebeat lee `/var/ossec/logs/alerts/alerts.json` y conecta al indexer.

Tras la recuperación registrada en [03-dashboard-recovery.md](03-dashboard-recovery.md), los cuatro servicios están activos. Indexer responde por HTTPS y Dashboard responde desde la LAN. Las credenciales iniciales se rotaron, el firewall se verificó y el primer agente Ubuntu se incorporó correctamente.

Versiones validadas durante la recuperación: Wazuh Manager, Indexer y Dashboard `4.14.7-1`; Filebeat `7.10.2-2`.

## 5. Control de actualizaciones (solo tras validación completa)

After the dashboard is working, disable the Wazuh APT repository as recommended by Wazuh. Ubuntu security updates remain available; this only prevents accidental Wazuh package upgrades.

```bash
sudo sed -i 's/^deb /#deb /' /etc/apt/sources.list.d/wazuh.list
sudo apt update
```

## Evidence to record

- Installation date, package versions and validated manual steps, without credentials.
- Confirmation that manager, indexer, and dashboard services are active.
- Confirmation that the dashboard was reached from the primary laptop.
- Sanitized firewall status and the decision for DHCP reservation.

## Exit criteria

- [x] Indexer, manager and Filebeat installed and validated.
- [x] Dashboard was reached from the private LAN.
- [x] Manager, indexer, and dashboard are active.
- [ ] Secrets and installer-generated archives remain outside Git.
- [x] Wazuh APT repository is disabled after validation.

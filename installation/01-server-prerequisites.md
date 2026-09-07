# 01 — Prerequisites for the Wazuh Central Node

## Objective

Confirm that the secondary laptop is ready to host a single-node Wazuh deployment before downloading or installing any Wazuh component.

## Scope and safety

- Target: the secondary laptop owned by the project owner.
- Operating system target: Ubuntu Server 24.04 LTS, 64-bit.
- This runbook only gathers information and applies normal operating-system updates. It does not install Wazuh.
- Keep real IP addresses, hostnames and usernames out of the public repository.

## Requirements to validate

| Requirement | Target for this lab | Result |
| --- | --- | --- |
| Operating system | Ubuntu Server 24.04 LTS, 64-bit | Validated: Ubuntu Server 24.04.4 LTS, x86_64 |
| Memory | 8 GiB recommended; 12 GB available according to ADR-001 | Validated: 11 GiB installed |
| CPU | 4 vCPU/cores recommended for 1–25 agents | Validated: 4 CPU cores |
| Storage | At least 50 GB available for a small deployment with 90 days of indexed data | Validated: 86 GB available on `/` |
| Network | Stable LAN connectivity from both endpoints | Partially validated: Wi-Fi LAN connection active on the central node; endpoint tests pending |
| Addressing | Reserved DHCP lease or documented static LAN address | Pending |

Reference: [Wazuh Quickstart requirements](https://documentation.wazuh.com/current/quickstart.html).

## Information-gathering commands

Run these commands on the future Wazuh node and record only sanitized results in this file or in the installation evidence:

```bash
hostnamectl
uname -m
free -h
nproc
df -h /
ip -brief address
ip route
```

Expected outcome:

- Ubuntu Server 24.04 LTS on a 64-bit architecture.
- At least 8 GiB RAM, four CPU cores where possible, and 50 GB free on the filesystem that will store Wazuh data.
- A reachable private LAN address. Prefer a DHCP reservation in the router instead of publishing the exact address in Git.

## Base operating-system preparation

After reviewing the information above, update the system during a maintenance window:

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

After reconnecting, validate:

```bash
hostnamectl
systemctl is-system-running
```

Expected result: the host reports Ubuntu Server 24.04 LTS and the system is `running` or only shows expected non-critical startup states.

## Connectivity validation

From each future agent endpoint, confirm that it can reach the Wazuh node over the LAN:

```bash
ping -c 4 <WAZUH_MANAGER_IP>
```

Do not proceed with the Wazuh installation if basic LAN connectivity is unreliable.

## Evidence to record

- Date tested.
- Sanitized hardware summary: RAM, CPU count and free disk.
- Confirmation of Ubuntu Server version and 64-bit architecture.
- Confirmation that both endpoints can reach the node.
- Whether address reservation and SSH access are ready.

Do not record the actual IP address, credentials or SSH keys.

## Recorded validation — 2026-08-28

- Ubuntu Server 24.04.4 LTS installed on a 64-bit system.
- Central-node capacity meets the initial lab target: 11 GiB RAM, four CPU cores and 86 GB free on `/`.
- Wi-Fi connectivity is active and SSH service has been enabled successfully.
- Hostname set to the sanitized value `wazuh-lab`; Internet and DNS connectivity were validated after a Wi-Fi change.
- Pending: reserve the DHCP address in the router (or document it privately), and validate reachability from both future agent endpoints.

## Exit criteria

- [ ] All table requirements are marked as validated.
- [x] Ubuntu Server 24.04.4 LTS is installed and reports no pending updates.
- [x] SSH service is enabled and active for administration.
- [ ] Both endpoints can reach the central node through the private LAN.
- [ ] The next runbook, `02-wazuh-single-node-installation.md`, can begin.

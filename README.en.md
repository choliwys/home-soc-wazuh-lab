# Home SOC Lab with Wazuh

[Versión en español](README.md)

A defensive, authorized lab built on Wazuh to practice the day-to-day SOC loop: collect endpoint telemetry, triage alerts, investigate, and document findings. Everything runs on my own hardware and private network. No attacks against third parties, no corporate credentials or data.

> **Note:** the detailed documentation (runbooks, detection cases, incident reports) is written in Spanish. This page summarizes the project and links to it.

## At a glance

- **Stack:** Wazuh `4.14.7` (Manager, Indexer, Dashboard, Filebeat) on a dedicated Ubuntu Server `24.04.4 LTS` node.
- **Endpoint:** Ubuntu agent `ubuntu-primary` (Wazuh Agent `4.14.7`), enrolled and active, centrally configured through the `linux-lab` group.
- **Hardening:** UFW restricted to the lab LAN, HTTPS dashboard, initial credentials rotated, certificates kept out of Git.
- **Output:** 3 reproducible detection cases, 3 sanitized incident reports, 1 dependency-free Python script.

## What it demonstrates

- Linux service administration with `systemd`, boot diagnosis and controlled recovery of the Indexer and Dashboard.
- Wazuh architecture and basic operation: Manager, Indexer, Dashboard, Filebeat and agents.
- Telemetry for file integrity (FIM), SSH and `sudo` on Linux.
- Alert investigation with context, classification of authorized tests, and initial MITRE ATT&CK mapping.
- Reproducible documentation, evidence sanitization and Python automation.

## Architecture

```text
┌──────────────────────────────────────┐
│ wazuh-lab · Ubuntu Server 24.04.4    │
│ Manager · Indexer · Dashboard        │
│ Filebeat · UFW (LAN only)            │
└───────────────────┬──────────────────┘
                    │ Wazuh Agent telemetry
          ┌─────────▼─────────┐
          │ ubuntu-primary    │
          │ Ubuntu endpoint   │
          └───────────────────┘

  Windows endpoint: deferred until I have a suitable personal host
```

Rationale for separating the central node from the endpoint: [architecture/](architecture/).

## Detection cases

| Case | Signal | Wazuh rule(s) | MITRE ATT&CK | Analysis |
| --- | --- | --- | --- | --- |
| [DET-001](detections/DET-001-fim-controlled-change.md) | File created, modified and deleted in an isolated FIM directory | `554`, `550`, `553` | `T1565.001`, `T1070.004`, `T1485` | [INC-001](incident-reports/INC-001-fim-laboratory-exercise.md) |
| [DET-002](detections/DET-002-ssh-invalid-user.md) | SSH attempt with a non-existent user | `5710` | None assigned: a single attempt does not show brute force | [INC-002](incident-reports/INC-002-ssh-invalid-user-laboratory-exercise.md) |
| [DET-003](detections/DET-003-sudo-controlled-command.md) | Controlled command executed with `sudo` | `5402` | `T1548.003` | [INC-003](incident-reports/INC-003-sudo-controlled-command.md) |

All three were controlled tests and were closed with no operational impact. A rule firing is a lead to investigate, not proof of malicious activity. Each incident report states what would change the verdict outside a lab: source, frequency, repeated attempts and later successful logins.

## Automation

[`scripts/summarize_detections.py`](scripts/summarize_detections.py) turns sanitized detection data into a Markdown summary. It needs Python 3.10+, no external packages, no API and no access to the server.

```bash
python3 scripts/summarize_detections.py scripts/data/validated-detections.json
```

See [scripts/README.md](scripts/README.md) for validation, rollback and the input format.

## Repository map

- [installation/](installation/): install, recovery and network startup-order runbooks.
- [agents/](agents/): endpoint enrollment and validation.
- [detections/](detections/): reproducible defensive cases.
- [incident-reports/](incident-reports/): analysis of the observed events.
- [docs/decisions.md](docs/decisions.md): technical decisions and their consequences.
- [docs/status.md](docs/status.md): current operational state and next step.
- [docs/evidence-guidelines.md](docs/evidence-guidelines.md): sanitization rules applied before publishing evidence.

## Scope and safety

- Own equipment and an authorized private lab network only.
- No passwords, agent keys, certificates, tokens, real IPs, private logs, EVTX or PCAP files are versioned.
- Screenshots are cropped and sanitized before being added to `screenshots/`.

## Next steps

1. Document a stable LAN configuration (DHCP reservation) privately.
2. Add a Windows endpoint once I have a host with enough resources.
3. Extend the detection set (for example, repeated failed SSH logins correlated over time).

## License

[MIT](LICENSE).

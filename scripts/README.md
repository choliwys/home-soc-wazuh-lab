# Scripts

Los scripts deben tener un propósito pequeño, documentación de uso, dependencias explícitas y datos de entrada de ejemplo sin información sensible.

## `summarize_detections.py`

Genera un informe Markdown desde una lista JSON de detecciones ya validadas y sanitizadas. No se conecta a Wazuh, no lee logs del servidor y no necesita credenciales.

### Prerrequisitos

- Python 3.10 o superior.
- Un archivo JSON con la estructura de `data/validated-detections.json`.

### Uso

Desde la raíz del repositorio:

```bash
python3 scripts/summarize_detections.py scripts/data/validated-detections.json
```

Para escribir un informe fuera del repositorio:

```bash
python3 scripts/summarize_detections.py \
  scripts/data/validated-detections.json \
  --output /tmp/wazuh-lab-detection-summary.md
```

### Impacto, validación y reversión

- **Impacto:** solo lee el JSON indicado; sin `--output`, escribe el resumen en pantalla.
- **Validación:** el resultado debe contener tres casos, cinco reglas únicas y dos casos con nivel máximo igual o superior a 5.
- **Reversión:** si se usó `--output`, eliminar únicamente el archivo generado fuera del repositorio. El script no modifica Wazuh ni el JSON de entrada.

La validación rechaza campos de riesgo como IP, hostname, usuarios, contraseñas, tokens y `full_log` para evitar introducir evidencia no sanitizada en el informe.

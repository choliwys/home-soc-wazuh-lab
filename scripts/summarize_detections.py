#!/usr/bin/env python3
"""Genera un resumen Markdown a partir de detecciones sanitizadas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
FORBIDDEN_KEYS = {"full_log", "hostname", "ip", "password", "token", "user"}
REQUIRED_CASE_KEYS = {"id", "date", "endpoint", "rules", "max_level", "classification"}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera un resumen Markdown desde datos de detección sanitizados."
    )
    parser.add_argument("input", type=Path, help="Archivo JSON sanitizado de entrada.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Archivo Markdown de salida. Si se omite, se escribe en la salida estándar.",
    )
    return parser.parse_args()


def find_forbidden_data(value: Any, path: str = "$") -> str | None:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                return f"campo no permitido: {path}.{key}"
            issue = find_forbidden_data(nested_value, f"{path}.{key}")
            if issue:
                return issue
    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            issue = find_forbidden_data(nested_value, f"{path}[{index}]")
            if issue:
                return issue
    elif isinstance(value, str) and IPV4_PATTERN.search(value):
        return f"posible dirección IP en {path}"
    return None


def load_cases(input_path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"No existe el archivo de entrada: {input_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON inválido: {error.msg} (línea {error.lineno})") from error

    issue = find_forbidden_data(data)
    if issue:
        raise ValueError(f"La entrada no está sanitizada: {issue}")

    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("La entrada debe ser un objeto JSON con una lista 'cases'.")

    cases = data["cases"]
    if not cases:
        raise ValueError("La lista 'cases' no puede estar vacía.")

    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"El caso {index} debe ser un objeto JSON.")
        missing_keys = REQUIRED_CASE_KEYS - case.keys()
        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            raise ValueError(f"El caso {index} no contiene: {missing}.")
        if not isinstance(case["rules"], list) or not case["rules"]:
            raise ValueError(f"El caso {case['id']} debe tener al menos una regla.")
        if not isinstance(case["max_level"], int):
            raise ValueError(f"El nivel máximo de {case['id']} debe ser un entero.")

    return cases


def render_summary(cases: list[dict[str, Any]]) -> str:
    unique_rules = sorted({rule for case in cases for rule in case["rules"]})
    cases_at_level_five = sum(case["max_level"] >= 5 for case in cases)

    lines = [
        "# Resumen reproducible de detecciones validadas",
        "",
        "Fuente: `scripts/data/validated-detections.json` (datos sanitizados).",
        "",
        "| Caso | Fecha | Endpoint | Reglas Wazuh | Nivel máximo | Clasificación |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for case in cases:
        rules = ", ".join(f"`{rule}`" for rule in case["rules"])
        lines.append(
            f"| {case['id']} | {case['date']} | {case['endpoint']} | {rules} | "
            f"{case['max_level']} | {case['classification']} |"
        )

    lines.extend(
        [
            "",
            "## Métricas",
            "",
            f"- Casos validados: {len(cases)}.",
            f"- Reglas Wazuh únicas: {len(unique_rules)} ({', '.join(unique_rules)}).",
            f"- Casos con nivel máximo igual o superior a 5: {cases_at_level_five}.",
            "- Todos los casos se clasifican como ejercicios controlados del laboratorio.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    arguments = parse_arguments()
    try:
        summary = render_summary(load_cases(arguments.input))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if arguments.output:
        arguments.output.write_text(summary, encoding="utf-8")
    else:
        print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

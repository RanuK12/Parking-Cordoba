#!/usr/bin/env python3
"""Genera un informe de mercado mínimo (placeholder para el portón)."""
from pathlib import Path

out = Path("report/informe_mercado.pdf")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(b"%PDF-1.4\n%%EOF\n")
print(f"Informe generado en {out}")

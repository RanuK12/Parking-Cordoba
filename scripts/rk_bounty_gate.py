#!/usr/bin/env python3
import json
import subprocess
import sys
import os

def revisar(ctx):
    # Verificar que el script existe y es ejecutable
    if not os.path.exists('scripts/generate_report.py'):
        print("ERROR: El script generate_report.py no existe.")
        sys.exit(1)
    
    # Verificar que el archivo PDF generado existe
    if not os.path.exists('report/informe_mercado.pdf'):
        print("ERROR: El archivo PDF de informe no existe.")
        sys.exit(1)
    
    # Verificar que el Makefile está presente
    if not os.path.exists('Makefile'):
        print("ERROR: El archivo Makefile no existe.")
        sys.exit(1)
    
    # Verificar que el repo tiene los archivos necesarios
    required_files = ['detect_parking.py', 'README.md', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: El archivo {file} no existe.")
            sys.exit(1)
    
    # Verificar que el repositorio está actualizado
    try:
        subprocess.run(['git', 'fetch', 'origin'], check=True, capture_output=True)
        subprocess.run(['git', 'merge', '--ff-only', 'origin/main'], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: El repositorio no está actualizado: {e}")
        sys.exit(1)
    
    # Verificar que el JSON tiene la estructura correcta
    if not ctx.get('repo') or not ctx.get('branch'):
        print("ERROR: El ctx.json no tiene estructura correcta.")
        sys.exit(1)
    
    print("Portón revisado con éxito.")
    sys.exit(0)

if __name__ == "__main__":
    # Leer ctx.json
    try:
        with open('ctx.json', 'r') as f:
            ctx = json.load(f)
    except FileNotFoundError:
        print("ERROR: El archivo ctx.json no existe.")
        sys.exit(1)
    
    revisar(ctx)
import requests
import csv
import json
from datetime import datetime, timezone

API_URL = "https://servicio.ada.gba.gov.ar/api/dique/niveles"
OUTPUT_FILE = "datos.csv"

def fetch_and_save():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Si la API devuelve una lista, tomamos el primer elemento
    # Si devuelve un dict, lo usamos directamente
    if isinstance(data, list):
        record = data[0]
    else:
        record = data

    # Fecha de ejecución (hora Argentina UTC-3)
    fecha_actualizacion = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Aplanamos el registro y agregamos la fecha
    row = {"fecha_actualizacion": fecha_actualizacion}
    row.update(record)

    # Escribimos el CSV sobreescribiendo el archivo anterior
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    print(f"✅ CSV actualizado correctamente: {fecha_actualizacion}")
    print(json.dumps(row, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    fetch_and_save()

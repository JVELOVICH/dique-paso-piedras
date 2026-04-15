import requests
import csv
import json
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL = "https://servicio.ada.gba.gov.ar/api/dique/niveles"
OUTPUT_FILE = "datos.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-AR,es;q=0.9",
    "Referer": "https://servicio.ada.gba.gov.ar/",
}

def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_and_save():
    session = create_session()

    print(f"Conectando a {API_URL} ...")
    response = session.get(API_URL, headers=HEADERS, timeout=60)
    response.raise_for_status()
    data = response.json()

    print("Respuesta recibida:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if isinstance(data, list):
        record = data[0]
    else:
        record = data

    fecha_actualizacion = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    row = {"fecha_actualizacion": fecha_actualizacion}
    row.update(record)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    print(f"\n✅ CSV actualizado correctamente: {fecha_actualizacion}")

if __name__ == "__main__":
    fetch_and_save()

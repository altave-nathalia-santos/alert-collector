import argparse
import asyncio
import json
import os
from alert_colletor.features.alert_watcher import AlertWatcher
from alert_colletor.features.alert_downloader import AlertImageDownloader

JSON_FILE = "downloaded_alerts.json"

async def main():
    parser = argparse.ArgumentParser(description="Test AlertWatcher")
    parser.add_argument("--start_date", type=str, required=True, help="Data de início (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, required=True, help="Data de término (YYYY-MM-DD)")
    parser.add_argument("--tenant", type=str, required=True, help="Nome do tenant")
    parser.add_argument("--category", type=str, required=True, help="Categoria do alerta a ser filtrada")
    
    args = parser.parse_args()

    alert_watcher = AlertWatcher(
        start_date=args.start_date,
        end_date=args.end_date,
        selected_category=args.category
    )
    downloader = AlertImageDownloader()

    alerts = await alert_watcher.list_operation_alerts(tenant=args.tenant)

    if not alerts:
        print("Nenhum alerta encontrado para os critérios especificados.")
        return

    print(f"=== {len(alerts)} alertas recuperados ===")

    downloaded_alerts = []

    for alert in alerts:
        image_path = downloader.download_alert_image(alert)
        if image_path:
            downloaded_alerts.append({"id": alert.id, "valuation": alert.valuation})
    
    if downloaded_alerts:
        update_json_file(downloaded_alerts)

def update_json_file(new_alerts):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(new_alerts)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

    print(f"{len(new_alerts)} alertas adicionados ao arquivo {JSON_FILE}")

if __name__ == "__main__":
    asyncio.run(main())

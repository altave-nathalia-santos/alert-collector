import argparse
import asyncio
from alert_colletor.features.alert_watcher import AlertWatcher

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

    alerts = await alert_watcher.list_operation_alerts(tenant=args.tenant)

    if alerts:
        print("\n=== Alertas Recuperados ===")
        for alert in alerts:
            print(f"ID: {alert.id}, Categoria: {alert.categories}, Tenant: {alert.tenant}, Timestamp: {alert.timestamp}, Classificação: {alert.valuation}")
    else:
        print("\nNenhum alerta encontrado para os critérios especificados.")

if __name__ == "__main__":
    asyncio.run(main())

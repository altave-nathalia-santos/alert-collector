import requests
from alert_colletor.features.alert import Alert
from decouple import config
from httpx import AsyncClient


class AlertWatcher:
    BASE_URL = "https://radiance-api.dev.altave.com.br/api/v1/alerts/"

    def __init__(self, start_date: str, end_date: str, selected_category: str) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.selected_category = selected_category
        self.token = None

    def _create_token(self) -> str:
        """Create Harpia Token."""
        url = config("HARPIA_CREATE_TOKEN_URL", cast=str)
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"email": config("HARPIA_EMAIL", cast=str), "password": config("HARPIA_PASSWORD", cast=str)}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("access")

    async def _ensure_token(self) -> None:
        if not self.token:
            self.token = self._create_token()

    def _transform_alerts(self, alerts_page: list[dict]) -> list[Alert]:
        transformed_alerts = []

        for alert in alerts_page:
            categories = alert.get("categories", [])

            if self.selected_category in categories:
                transformed_alerts.append(
                    Alert(
                        id=alert["identifier"],
                        categories=categories,
                        tenant=alert["tenant"]["name"],
                        timestamp=alert["timestamp"],
                        valuation=alert["classification"],
                    )
                )

        return transformed_alerts

    async def list_operation_alerts(self, tenant: str) -> list[Alert]:
        await self._ensure_token()

        params = {
            "tenant": tenant,
            "date_added_after": self.start_date,
            "date_added_before": self.end_date,
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        async with AsyncClient(base_url=self.BASE_URL, headers=headers) as client:
            alerts = []
            page = 1

            while True:
                params["page"] = page
                response = await client.get("/", params=params)

                if response.status_code != 200:
                    raise Exception(f"Error fetching alerts: {response.status_code} - {response.text}")

                data = response.json()
                alerts.extend(self._transform_alerts(data.get("data", [])))

                if page >= data.get("num_pages", 1):
                    break

                page += 1

        return alerts

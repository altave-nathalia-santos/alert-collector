import boto3
import os
from datetime import datetime, timezone
from decouple import config


class AlertImageDownloader:
    def __init__(self):
        """Initialize connection with AWS S3 using credentials from .env."""
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=config("AWS_REGION"),
        )
        self.bucket_name = "harpia-alerts"

    def _generate_image_path(self, alert: dict) -> str:
        tenant = alert["tenant"]["name"]
        
        timestamp = datetime.fromtimestamp(alert["timestamp"] / 1000, tz=timezone.utc)
        year, month, day = timestamp.strftime("%Y-%m-%d").split("-")
        identifier = alert["identifier"]

        return f"{tenant}/{year}/{month}/{day}/{alert['timestamp']}_{identifier}_clean."

    def download_alert_image(self, alert: dict, save_dir: str = "/mnt/d/expro/dynamic_redzones") -> str:
        image_path = self._generate_image_path(alert)
        file_name = f"{alert['identifier']}.jpg"
        local_file_path = os.path.join(save_dir, file_name)

        os.makedirs(save_dir, exist_ok=True)

        try:
            self.s3_client.download_file(self.bucket_name, image_path, local_file_path)
            print(f"Image downloaded successfully: {local_file_path}")
            return local_file_path
        except Exception as e:
            print(f"Error downloading the image: {e}")
            return None

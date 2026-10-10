"""Seu IoT example: read the historical data of a process.

GET {SIOT_API_BASE_URL}/external/v1/processes/{process_uuid}/data
Query params (all optional): device_uuid, start, end (ISO 8601), limit
(default 500, max 2000). Returns the most recent points in chronological order.
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ["SIOT_API_BASE_URL"].rstrip("/")
API_KEY = os.environ["SIOT_API_KEY"]
PROCESS_UUID = os.environ["SIOT_PROCESS_UUID"]
DEVICE_UUID = os.getenv("SIOT_DEVICE_UUID")
VERIFY_TLS = os.getenv("SIOT_VERIFY_TLS", "true").lower() == "true"


def main() -> None:
    params = {"limit": 20}
    if DEVICE_UUID:
        params["device_uuid"] = DEVICE_UUID

    response = requests.get(
        f"{API_BASE_URL}/external/v1/processes/{PROCESS_UUID}/data",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
        verify=VERIFY_TLS,
        timeout=10,
    )
    if response.status_code == 404:
        print("404: process/device is not in this contract's scope")
        return 1
    response.raise_for_status()

    points = response.json()
    print(f"{len(points)} point(s):")
    for point in points:
        print(f"  {point['timestamp']}  {point['data']}")


if __name__ == "__main__":
    sys.exit(main())

"""Seu IoT example: read your API contract's scope.

GET {SIOT_API_BASE_URL}/external/v1/contract with "Authorization: Bearer <API key>"
returns the processes and devices your key can access, already resolved to
names (and units, for Linearization processes).
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ["SIOT_API_BASE_URL"].rstrip("/")
API_KEY = os.environ["SIOT_API_KEY"]
VERIFY_TLS = os.getenv("SIOT_VERIFY_TLS", "true").lower() == "true"


def main() -> None:
    response = requests.get(
        f"{API_BASE_URL}/external/v1/contract",
        headers={"Authorization": f"Bearer {API_KEY}"},
        verify=VERIFY_TLS,
        timeout=10,
    )
    response.raise_for_status()
    contract = response.json()

    print(f"Contract: {contract['name']} (active={contract['is_active']}, expires_at={contract.get('expires_at')})")
    print("Processes:")
    for process in contract["processes"]:
        unit = f" [{process['unit']}]" if process.get("unit") else ""
        print(f"  - {process['name'] or '(removed)'}{unit}  uuid={process['uuid']}")

    if contract["device_uuids"]:
        print("Devices:")
        for device in contract["devices"]:
            print(f"  - {device['name'] or '(removed)'}  uuid={device['uuid']}")
    else:
        print("Devices: all devices of the project")


if __name__ == "__main__":
    sys.exit(main())

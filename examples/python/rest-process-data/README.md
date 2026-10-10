# Python - read process history (REST)

Calls `GET /external/v1/processes/{process_uuid}/data` and prints the latest 20 points. Get the `process_uuid` from the [rest-contract](../rest-contract) example.

## Run

```bash
cp .env.example .env    # fill in SIOT_API_BASE_URL, SIOT_API_KEY and SIOT_PROCESS_UUID
pip install -r requirements.txt
python process_data.py
```

Requires Python 3.10+. A `404` means the process (or device) is not in the contract's scope. See [REST API docs](../../../docs/en/rest-api.md).

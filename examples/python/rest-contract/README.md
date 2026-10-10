# Python - read the contract scope (REST)

Calls `GET /external/v1/contract` and prints the processes and devices your API key can access. The simplest example, and a good first check that your key works.

## Run

```bash
cp .env.example .env    # then fill in SIOT_API_BASE_URL and SIOT_API_KEY
pip install -r requirements.txt
python contract.py
```

Requires Python 3.10+. See [REST API docs](../../../docs/en/rest-api.md).

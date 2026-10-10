# Node.js - REST endpoints

Zero-dependency examples using Node's built-in `fetch` (Node 20.6+ for `--env-file`).

```bash
cp .env.example .env    # fill in SIOT_API_BASE_URL, SIOT_API_KEY (and SIOT_PROCESS_UUID)
npm run contract        # GET /external/v1/contract
npm run data            # GET /external/v1/processes/{uuid}/data
```

See [REST API docs](../../../docs/en/rest-api.md).

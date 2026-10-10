// Seu IoT example: read the historical data of a process.
// GET /external/v1/processes/{process_uuid}/data
// Optional query params: device_uuid, start, end (ISO 8601), limit (default 500, max 2000).

const baseUrl = process.env.SIOT_API_BASE_URL.replace(/\/+$/, "");
const headers = { Authorization: `Bearer ${process.env.SIOT_API_KEY}` };

const params = new URLSearchParams({ limit: "20" });
if (process.env.SIOT_DEVICE_UUID) params.set("device_uuid", process.env.SIOT_DEVICE_UUID);

const url = `${baseUrl}/external/v1/processes/${encodeURIComponent(process.env.SIOT_PROCESS_UUID)}/data?${params}`;
const response = await fetch(url, { headers });
if (response.status === 404) {
  console.error("404: process/device is not in this contract's scope");
  process.exit(1);
}
if (!response.ok) {
  console.error(`HTTP ${response.status}:`, await response.text());
  process.exit(1);
}

const points = await response.json();
console.log(`${points.length} point(s):`);
for (const point of points) console.log(`  ${point.timestamp}  ${point.data}`);

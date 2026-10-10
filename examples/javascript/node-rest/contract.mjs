// Seu IoT example: read your API contract's scope.
// GET /external/v1/contract with "Authorization: Bearer <API key>".

const baseUrl = process.env.SIOT_API_BASE_URL.replace(/\/+$/, "");
const headers = { Authorization: `Bearer ${process.env.SIOT_API_KEY}` };

const response = await fetch(`${baseUrl}/external/v1/contract`, { headers });
if (!response.ok) {
  console.error(`HTTP ${response.status}:`, await response.text());
  process.exit(1);
}
const contract = await response.json();

console.log(`Contract: ${contract.name} (active=${contract.is_active}, expires_at=${contract.expires_at ?? "never"})`);
console.log("Processes:");
for (const p of contract.processes) {
  console.log(`  - ${p.name ?? "(removed)"}${p.unit ? ` [${p.unit}]` : ""}  uuid=${p.uuid}`);
}
if (contract.device_uuids.length) {
  console.log("Devices:");
  for (const d of contract.devices) console.log(`  - ${d.name ?? "(removed)"}  uuid=${d.uuid}`);
} else {
  console.log("Devices: all devices of the project");
}

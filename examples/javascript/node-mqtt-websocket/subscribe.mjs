// Seu IoT example: HTTPS handshake + live subscription over MQTT on WebSocket (mqtt.js).
// 1. GET  /external/v1/contract          -> names/units for readable output
// 2. POST /external/v1/mqtt-credentials  -> username/password/host/ws_port/topics
//    (every call ROTATES the password, invalidating the previous credential)
// 3. Connect via wss, subscribe to every authorized topic, print each message.

import mqtt from "mqtt";

const baseUrl = process.env.SIOT_API_BASE_URL.replace(/\/+$/, "");
const headers = { Authorization: `Bearer ${process.env.SIOT_API_KEY}` };
const useTls = (process.env.SIOT_WS_TLS ?? "true").toLowerCase() === "true";

async function call(path, method = "GET") {
  const response = await fetch(`${baseUrl}${path}`, { method, headers });
  if (!response.ok) throw new Error(`${method} ${path} -> HTTP ${response.status}: ${await response.text()}`);
  return response.json();
}

const contract = await call("/external/v1/contract");
const processes = new Map(contract.processes.map((p) => [p.uuid, p]));
const devices = new Map(contract.devices.map((d) => [d.uuid, d]));
console.log(`[ws] contract scope: ${processes.size} process(es), ${devices.size} device(s)`);

const creds = await call("/external/v1/mqtt-credentials", "POST");
console.log(`[ws] credential issued - username=${creds.username}`);

// The firmware sends "timestamp" as "DD.MM.YYYY HH:MM:SS.microseconds" in UTC (not ISO 8601).
function deviceTime(body) {
  const m = /^(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2})\.(\d+)$/.exec(body?.timestamp ?? "");
  if (!m) return body?.timestamp ?? "unknown";
  const [, day, month, year, hour, minute, second, micro] = m;
  return `${year}-${month}-${day}T${hour}:${minute}:${second}.${micro.slice(0, 3).padEnd(3, "0")}Z`;
}

// Topic format: /{project_id}/{device_uuid}/{process_uuid}/ - payload is JSON with a "data" field.
function describe(topic, payload, receivedAt) {
  const parts = topic.replace(/^\/+|\/+$/g, "").split("/");
  const text = payload.toString("utf-8");
  if (parts.length !== 3) return `[${topic}] ${text}`;
  const [, deviceUuid, processUuid] = parts;
  const process_ = processes.get(processUuid);
  let value;
  let body = {};
  try {
    body = JSON.parse(text);
    value = body.data;
  } catch {
    value = text;
  }
  const unit = process_?.unit ? ` ${process_.unit}` : "";
  return `[data time ${deviceTime(body)} | received ${receivedAt}] Device ${devices.get(deviceUuid)?.name ?? deviceUuid} published ${value}${unit} on process ${process_?.name ?? processUuid}`;
}

const url = `${useTls ? "wss" : "ws"}://${creds.host}:${creds.ws_port}/mqtt`;
console.log(`[ws] connecting to ${url} ...`);
const client = mqtt.connect(url, {
  username: creds.username,
  password: creds.password,
  keepalive: 30,
});

client.on("connect", () => {
  console.log(`[ws] connected - subscribing to ${creds.topics.length} topic(s):`);
  for (const topic of creds.topics) {
    console.log(`  - ${topic}`);
    client.subscribe(topic);
  }
});
client.on("message", (topic, payload) => console.log(describe(topic, payload, new Date().toISOString())));
client.on("error", (err) => console.error("[ws] error:", err.message));
client.on("close", () => console.log("[ws] disconnected"));

process.on("SIGINT", () => {
  console.log("\n[ws] shutting down...");
  client.end(false, {}, () => process.exit(0));
});

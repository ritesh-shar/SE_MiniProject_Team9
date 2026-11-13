/**
 * Automated tests for BBMS Notification Service
 * 
 * Uses Node.js built-in test runner (node:test)
 * # BBMS-F-051 (TC-Adm-02)
 */

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const app = require('./index');

let server;
let baseUrl;

test.before(async () => {
  await new Promise((resolve) => {
    server = http.createServer(app);
    server.listen(0, () => {
      const port = server.address().port;
      baseUrl = `http://127.0.0.1:${port}`;
      resolve();
    });
  });
});

test.after(async () => {
  await new Promise((resolve) => {
    server.close(resolve);
  });
});

test('POST /notify delivers message successfully and returns notification ID', async () => {
  const payload = {
    donorId: 101,
    recipient: 'donor@example.com',
    message: 'You are eligible to donate blood!',
    channel: 'email',
  };

  const response = await fetch(`${baseUrl}/notify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  assert.strictEqual(response.status, 200);
  const data = await response.json();
  assert.strictEqual(data.status, 'delivered');
  assert.strictEqual(data.recipient, 'donor@example.com');
  assert.ok(data.notificationId.startsWith('NOTIF-'));
});

test('POST /notify rejects requests missing recipient or message with 400', async () => {
  const payload = {
    donorId: 102,
    // missing recipient and message
  };

  const response = await fetch(`${baseUrl}/notify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  assert.strictEqual(response.status, 400);
  const data = await response.json();
  assert.strictEqual(data.code, 'INVALID_PAYLOAD');
});

test('GET /health returns healthy status', async () => {
  const response = await fetch(`${baseUrl}/health`);
  assert.strictEqual(response.status, 200);
  const data = await response.json();
  assert.strictEqual(data.status, 'ok');
});

test('GET /outbox returns array of sent notifications', async () => {
  const response = await fetch(`${baseUrl}/outbox`);
  assert.strictEqual(response.status, 200);
  const data = await response.json();
  assert.ok(Array.isArray(data));
});

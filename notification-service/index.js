/**
 * BBMS Donor Notification Microservice
 * 
 * # BBMS-F-051: Reminders to eligible donors through a Node.js notification service.
 * Owner: Rithish P M (PR #1)
 */

const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const OUTBOX_FILE = path.join(__dirname, 'outbox.json');

// Ensure outbox file exists
if (!fs.existsSync(OUTBOX_FILE)) {
  fs.writeFileSync(OUTBOX_FILE, JSON.stringify([]));
}

/**
 * Append a sent message to the outbox log.
 */
function recordToOutbox(entry) {
  try {
    let outbox = [];
    if (fs.existsSync(OUTBOX_FILE)) {
      const data = fs.readFileSync(OUTBOX_FILE, 'utf-8');
      outbox = JSON.parse(data || '[]');
    }
    outbox.push(entry);
    fs.writeFileSync(OUTBOX_FILE, JSON.stringify(outbox, null, 2));
  } catch (err) {
    console.error('Error writing to outbox:', err);
  }
}

/**
 * Send notification with exponential backoff retry.
 */
async function processWithRetry(payload, maxRetries = 3) {
  let attempt = 0;
  let delay = 50; // milliseconds base

  while (attempt < maxRetries) {
    try {
      attempt++;
      // Mock delivery logic: recipient validation check
      if (!payload.recipient) {
        throw new Error('Recipient is required');
      }

      const entry = {
        id: `NOTIF-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
        donorId: payload.donorId || null,
        recipient: payload.recipient,
        channel: payload.channel || 'email',
        message: payload.message,
        timestamp: new Date().toISOString(),
        status: 'delivered',
        attempts: attempt,
      };

      recordToOutbox(entry);
      return { success: true, entry };
    } catch (err) {
      if (attempt >= maxRetries) {
        throw err;
      }
      // Exponential backoff
      await new Promise((resolve) => setTimeout(resolve, delay));
      delay *= 2;
    }
  }
}

// POST /notify - Send notification endpoint
app.post('/notify', async (req, res) => {
  const { recipient, message, donorId, channel } = req.body;

  if (!recipient || !message) {
    return res.status(400).json({
      error: 'Missing required fields: recipient and message are mandatory.',
      code: 'INVALID_PAYLOAD',
    });
  }

  try {
    const result = await processWithRetry({ recipient, message, donorId, channel });
    return res.status(200).json({
      status: 'delivered',
      notificationId: result.entry.id,
      recipient: result.entry.recipient,
      channel: result.entry.channel,
      timestamp: result.entry.timestamp,
    });
  } catch (err) {
    return res.status(500).json({
      error: `Failed to deliver notification after retries: ${err.message}`,
      code: 'DELIVERY_FAILED',
    });
  }
});

// GET /outbox - Read outbox messages
app.get('/outbox', (req, res) => {
  try {
    const data = fs.readFileSync(OUTBOX_FILE, 'utf-8');
    const outbox = JSON.parse(data || '[]');
    res.status(200).json(outbox);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /health - Service health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', service: 'bbms-notification-service' });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`BBMS Notification Service running on port ${PORT}`);
  });
}

module.exports = app;

/**
 * Inventory Alerts Logic
 * 
 * # BBMS-F-021, BBMS-F-022
 */

document.addEventListener('DOMContentLoaded', async () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const logoutLink = document.getElementById('logout-link');
  if (logoutLink) {
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault();
      auth.clear();
      window.location.href = 'index.html';
    });
  }

  const alertBox = document.getElementById('alerts-msg');
  const lowStockGrid = document.getElementById('low-stock-grid');
  const expiringBody = document.getElementById('expiring-table-body');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  async function loadAlerts() {
    // 1. Load Low-Stock Alerts (BBMS-F-022)
    try {
      const data = await apiFetch('/inventory/alerts/low-stock');
      const alerts = data.alerts || [];

      if (alerts.length === 0) {
        lowStockGrid.innerHTML = '<p style="color: #2e7d32; font-weight: bold;">✓ All blood groups are above minimum safety thresholds.</p>';
      } else {
        lowStockGrid.innerHTML = alerts
          .map((a) => `
            <div class="stock-card stock-low">
              <div>
                <div class="stock-blood-group">${a.blood_group}</div>
                <div class="stock-component">All Components Combined</div>
                <div class="stock-count">${a.current_units} unit(s)</div>
              </div>
              <div>
                <span class="badge badge-danger">DEFICIT: -${a.deficit} UNITS</span>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.4rem;">Threshold: ${a.threshold_units} units</div>
              </div>
            </div>
          `)
          .join('');
      }
    } catch (err) {
      lowStockGrid.innerHTML = `<p class="alert-danger">${err.message}</p>`;
    }

    // 2. Load Expiring Units (BBMS-F-021)
    try {
      const data = await apiFetch('/inventory/alerts/expiry?days=5');
      const alerts = data.alerts || [];

      if (alerts.length === 0) {
        expiringBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #2e7d32; font-weight: bold;">✓ No blood units expiring within the next 5 days.</td></tr>';
      } else {
        expiringBody.innerHTML = alerts
          .map((u) => {
            const isCritical = u.days_until_expiry <= 2;
            const badgeClass = isCritical ? 'badge-danger' : 'badge-role';
            const statusText = u.is_expired ? 'EXPIRED' : `${u.days_until_expiry} day(s)`;

            return `
              <tr style="${isCritical ? 'background-color: #fff6f6;' : ''}">
                <td>#${u.donation_id}</td>
                <td><strong>${u.donor_username}</strong></td>
                <td><strong style="color: #c00;">${u.blood_group}</strong></td>
                <td>${u.component}</td>
                <td>${u.quantity} unit(s)</td>
                <td>${u.donation_date}</td>
                <td>${u.expiry_date}</td>
                <td><span class="badge ${badgeClass}">${statusText}</span></td>
              </tr>
            `;
          })
          .join('');
      }
    } catch (err) {
      expiringBody.innerHTML = `<tr><td colspan="8" class="alert-danger">${err.message}</td></tr>`;
    }
  }

  await loadAlerts();
});

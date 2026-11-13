/**
 * Admin Dashboard & Reports Operations
 * 
 * # BBMS-F-050, BBMS-F-051, BBMS-F-052
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

  const alertBox = document.getElementById('admin-alert');
  const remindersBtn = document.getElementById('send-reminders-btn');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  async function loadDashboardData() {
    try {
      const data = await apiFetch('/admin/dashboard');

      // Summary metrics
      document.getElementById('stat-stock-total').textContent = data.summary.total_stock_units || 0;
      document.getElementById('stat-pending-total').textContent = data.summary.pending_requests_count || 0;
      document.getElementById('stat-donations-total').textContent = data.summary.total_donations_count || 0;

      // Pending requests table
      const pendingTable = document.getElementById('admin-pending-table');
      if (data.pending_requests && data.pending_requests.length > 0) {
        pendingTable.innerHTML = data.pending_requests
          .map((r) => `
            <tr>
              <td>#${r.id}</td>
              <td><strong>${r.hospital_name}</strong></td>
              <td>${r.blood_group}</td>
              <td>${r.component}</td>
              <td>${r.quantity} unit(s)</td>
              <td><span class="badge ${r.urgency === 'critical' ? 'badge-danger' : 'badge-role'}">${r.urgency.toUpperCase()}</span></td>
              <td>${new Date(r.created_at).toLocaleDateString()}</td>
            </tr>
          `)
          .join('');
      } else {
        pendingTable.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #888;">No pending requests.</td></tr>';
      }

      // Recent donations table
      const donationsTable = document.getElementById('admin-donations-table');
      if (data.recent_donations && data.recent_donations.length > 0) {
        donationsTable.innerHTML = data.recent_donations
          .map((d) => `
            <tr>
              <td>#${d.id}</td>
              <td>${d.donor_username}</td>
              <td><strong>${d.blood_group}</strong></td>
              <td>${d.component}</td>
              <td>${d.quantity} unit(s)</td>
              <td>${d.donation_date}</td>
            </tr>
          `)
          .join('');
      } else {
        donationsTable.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #888;">No donations recorded yet.</td></tr>';
      }
    } catch (err) {
      showAlert(err.message || 'Error loading dashboard metrics.', true);
    }
  }

  if (remindersBtn) {
    remindersBtn.addEventListener('click', async () => {
      remindersBtn.disabled = true;
      remindersBtn.textContent = '⏳ Dispatching...';
      try {
        const res = await apiFetch('/requests/reminders/send', { method: 'POST' });
        showAlert(res.message);
      } catch (err) {
        showAlert(err.message || 'Error dispatching reminders.', true);
      } finally {
        remindersBtn.disabled = false;
        remindersBtn.textContent = '🔔 Send Donor Reminders';
      }
    });
  }

  await loadDashboardData();
});

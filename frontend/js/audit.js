/**
 * Audit Trail Inspection Frontend
 * 
 * # BBMS-SR-004, BBMS-NF-005
 */

document.addEventListener('DOMContentLoaded', async () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const user = auth.getUser();
  if (!user || user.role !== 'admin') {
    alert('Access restricted to administrators.');
    window.location.href = 'dashboard.html';
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

  const alertBox = document.getElementById('audit-alert');
  const tableBody = document.getElementById('audit-table-body');
  const filterSelect = document.getElementById('event-filter');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  async function loadLogs(eventType = '') {
    try {
      const endpoint = eventType ? `/audit?event_type=${eventType}` : '/audit';
      const logs = await apiFetch(endpoint);

      if (!logs || logs.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #888;">No audit records found.</td></tr>';
        return;
      }

      tableBody.innerHTML = logs
        .map((l) => {
          let badgeClass = 'badge-secondary';
          if (l.event_type === 'LOGIN_SUCCESS') badgeClass = 'badge-success';
          else if (l.event_type === 'LOGIN_FAILED' || l.event_type === 'ACCOUNT_LOCKED') badgeClass = 'badge-danger';
          else if (l.event_type === 'ADMIN_ACTION') badgeClass = 'badge-primary';
          else if (l.event_type === 'STOCK_CHANGE') badgeClass = 'badge-role';

          const formattedTime = new Date(l.timestamp).toLocaleString();
          const extraStr = l.extra_data && Object.keys(l.extra_data).length > 0 ? JSON.stringify(l.extra_data) : '-';

          return `
            <tr>
              <td style="white-space: nowrap; font-size: 0.85rem;">${formattedTime}</td>
              <td><span class="badge ${badgeClass}">${l.event_type}</span></td>
              <td><strong>${l.username || 'Anonymous'}</strong></td>
              <td style="font-family: monospace; font-size: 0.85rem;">${l.ip_address || '-'}</td>
              <td style="font-size: 0.9rem;">${l.description}</td>
              <td style="font-size: 0.8rem; color: #555; max-width: 200px; word-break: break-all;">${extraStr}</td>
            </tr>
          `;
        })
        .join('');
    } catch (err) {
      showAlert(err.message || 'Error loading audit logs.', true);
    }
  }

  if (filterSelect) {
    filterSelect.addEventListener('change', () => {
      loadLogs(filterSelect.value);
    });
  }

  await loadLogs();
});

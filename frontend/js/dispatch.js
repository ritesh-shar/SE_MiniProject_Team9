/**
 * Dispatch Records Tracking Frontend
 * 
 * # BBMS-F-042: Retrieve dispatch manifest by request ID.
 */

document.addEventListener('DOMContentLoaded', () => {
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

  const form = document.getElementById('dispatch-search-form');
  const alertBox = document.getElementById('dispatch-alert');
  const card = document.getElementById('dispatch-card');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      alertBox.style.display = 'none';
      card.style.display = 'none';

      const reqId = document.getElementById('request-id-input').value.trim();
      if (!reqId) return;

      try {
        const d = await apiFetch(`/dispatch/${reqId}`);

        document.getElementById('dispatch-id-badge').textContent = `DISPATCH #${d.dispatch_id}`;
        document.getElementById('disp-timestamp').textContent = new Date(d.dispatched_at).toLocaleString();
        document.getElementById('disp-staff').textContent = d.issued_by_name ? `${d.issued_by_name} (ID: ${d.issued_by_id})` : 'System';
        document.getElementById('disp-hospital').textContent = `${d.recipient_hospital_name} (ID: ${d.recipient_hospital_id})`;
        document.getElementById('disp-req-id').textContent = `#${d.request_id}`;

        const detailsObj = d.details || {};
        document.getElementById('disp-details').textContent =
          `Blood Group: ${detailsObj.blood_group || 'N/A'} | Component: ${detailsObj.component || 'N/A'} | Quantity: ${detailsObj.quantity || 0} unit(s) | Urgency: ${(detailsObj.urgency || 'normal').toUpperCase()}`;

        card.style.display = 'block';
      } catch (err) {
        showAlert(err.message || 'Dispatch record not found or inaccessible.', true);
      }
    });
  }
});

/**
 * Hospital Blood Requests Management
 * 
 * # BBMS-F-031: Hospital submits and tracks blood requests.
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

  const alertBox = document.getElementById('request-alert');
  const form = document.getElementById('blood-request-form');
  const tableBody = document.getElementById('requests-table-body');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  async function loadRequests() {
    try {
      const requests = await apiFetch('/requests');
      if (!requests || requests.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #888;">No blood requests submitted yet.</td></tr>';
        return;
      }

      tableBody.innerHTML = requests
        .map((r) => {
          let badgeClass = 'badge-secondary';
          if (r.status === 'approved') badgeClass = 'badge-success';
          else if (r.status === 'issued') badgeClass = 'badge-primary';
          else if (r.status === 'rejected') badgeClass = 'badge-danger';

          const dateStr = new Date(r.created_at).toLocaleDateString();
          return `
            <tr>
              <td>#${r.id}</td>
              <td><strong>${r.blood_group}</strong></td>
              <td>${r.component}</td>
              <td>${r.quantity} unit(s)</td>
              <td><span class="badge ${r.urgency === 'critical' ? 'badge-danger' : 'badge-role'}">${r.urgency.toUpperCase()}</span></td>
              <td><span class="badge ${badgeClass}">${r.status.toUpperCase()}</span></td>
              <td>${dateStr}</td>
              <td style="font-size: 0.85rem; color: #555;">${r.decision_note || '-'}</td>
            </tr>
          `;
        })
        .join('');
    } catch (err) {
      tableBody.innerHTML = `<tr><td colspan="8" class="alert-danger">${err.message}</td></tr>`;
    }
  }

  // Handle request form submission
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      alertBox.style.display = 'none';

      const payload = {
        blood_group: document.getElementById('blood-group').value,
        component: document.getElementById('component').value,
        quantity: parseInt(document.getElementById('quantity').value, 10),
        urgency: document.getElementById('urgency').value,
      };

      try {
        const result = await apiFetch('/requests', {
          method: 'POST',
          body: JSON.stringify(payload),
        });

        showAlert(`Requisition #${result.requestId} submitted successfully!`);
        form.reset();
        await loadRequests();
      } catch (err) {
        showAlert(err.message || 'Error submitting requisition.', true);
      }
    });
  }

  await loadRequests();
});

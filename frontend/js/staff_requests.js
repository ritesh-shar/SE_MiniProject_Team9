/**
 * Staff Request Approval and Issuance Operations
 * 
 * # BBMS-F-040, BBMS-F-041
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

  const alertBox = document.getElementById('staff-alert');
  const pendingBody = document.getElementById('pending-requests-body');
  const approvedBody = document.getElementById('approved-requests-body');

  function showAlert(msg, isError = false) {
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = 'block';
  }

  async function loadRequests() {
    try {
      const allRequests = await apiFetch('/requests');
      const pending = allRequests.filter((r) => r.status === 'pending');
      const approved = allRequests.filter((r) => r.status === 'approved');

      // 1. Pending Table
      if (pending.length === 0) {
        pendingBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #888;">No pending requests awaiting review.</td></tr>';
      } else {
        pendingBody.innerHTML = pending
          .map((r) => `
            <tr>
              <td>#${r.id}</td>
              <td><strong>${r.hospital_name}</strong></td>
              <td>${r.blood_group}</td>
              <td>${r.component}</td>
              <td>${r.quantity} unit(s)</td>
              <td><span class="badge ${r.urgency === 'critical' ? 'badge-danger' : 'badge-role'}">${r.urgency.toUpperCase()}</span></td>
              <td>${new Date(r.created_at).toLocaleDateString()}</td>
              <td>
                <div style="display: flex; gap: 0.5rem;">
                  <button class="btn btn-primary" style="padding: 0.25rem 0.6rem; font-size: 0.8rem; background-color: #2e7d32;" onclick="reviewRequest(${r.id}, 'approved')">
                    ✓ Approve
                  </button>
                  <button class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.8rem; background-color: #c62828; color: white;" onclick="reviewRequest(${r.id}, 'rejected')">
                    ✕ Reject
                  </button>
                </div>
              </td>
            </tr>
          `)
          .join('');
      }

      // 2. Approved Table
      if (approved.length === 0) {
        approvedBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #888;">No approved requests awaiting issue.</td></tr>';
      } else {
        approvedBody.innerHTML = approved
          .map((r) => `
            <tr>
              <td>#${r.id}</td>
              <td><strong>${r.hospital_name}</strong></td>
              <td>${r.blood_group}</td>
              <td>${r.component}</td>
              <td>${r.quantity} unit(s)</td>
              <td>${r.reviewed_by_name || 'Staff'}</td>
              <td>
                <button class="btn btn-primary" style="padding: 0.25rem 0.75rem; font-size: 0.85rem;" onclick="issueRequest(${r.id})">
                  📦 Issue Blood
                </button>
              </td>
            </tr>
          `)
          .join('');
      }
    } catch (err) {
      showAlert(err.message || 'Error loading requests.', true);
    }
  }

  window.reviewRequest = async (requestId, decision) => {
    let note = '';
    if (decision === 'rejected') {
      note = prompt('Reason for rejection:') || 'Stock unavailable';
    } else {
      note = prompt('Approval notes (optional):') || 'Approved';
    }

    try {
      const res = await apiFetch(`/requests/${requestId}/review`, {
        method: 'POST',
        body: JSON.stringify({ decision, decision_note: note }),
      });
      showAlert(res.message);
      await loadRequests();
    } catch (err) {
      showAlert(err.message || 'Review failed.', true);
    }
  };

  window.issueRequest = async (requestId) => {
    if (!confirm(`Are you sure you want to issue Blood Request #${requestId}? This will deduct inventory units.`)) {
      return;
    }

    try {
      const res = await apiFetch(`/requests/${requestId}/issue`, { method: 'POST' });
      showAlert(`${res.message} (Remaining stock: ${res.remaining_stock} units)`);
      await loadRequests();
    } catch (err) {
      showAlert(err.message || 'Issuance failed.', true);
    }
  };

  await loadRequests();
});

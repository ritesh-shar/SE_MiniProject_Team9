/**
 * BBMS Role-Based Dashboard Logic
 *
 * Shows/hides features based on the logged-in user's role (Donor, Staff, Hospital, Admin).
 */

document.addEventListener('DOMContentLoaded', async () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const user = auth.getUser() || { username: 'User', role: 'donor' };

  // Update header / user info
  const usernameDisplay = document.getElementById('user-display-name');
  const roleBadge = document.getElementById('user-role-badge');
  if (usernameDisplay) usernameDisplay.textContent = user.username;
  if (roleBadge) {
    roleBadge.textContent = user.role.toUpperCase();
  }

  // Handle Logout
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      auth.clear();
      window.location.href = 'index.html';
    });
  }

  // Role-based visibility
  const staffOnlyElements = document.querySelectorAll('.role-staff-only');
  const hospitalStaffElements = document.querySelectorAll('.role-hospital-staff');
  const donorOnlyElements = document.querySelectorAll('.role-donor-only');

  const isStaffOrAdmin = ['staff', 'admin'].includes(user.role);
  const isHospitalOrAbove = ['hospital', 'staff', 'admin'].includes(user.role);
  const isDonor = user.role === 'donor';

  staffOnlyElements.forEach((el) => {
    el.style.display = isStaffOrAdmin ? 'block' : 'none';
  });

  hospitalStaffElements.forEach((el) => {
    el.style.display = isHospitalOrAbove ? 'block' : 'none';
  });

  donorOnlyElements.forEach((el) => {
    el.style.display = isDonor ? 'block' : 'none';
  });

  // Load donation history if on history container
  const historyTable = document.getElementById('donation-history-body');
  if (historyTable) {
    try {
      const history = await apiFetch('/donations/history');
      if (history.length === 0) {
        historyTable.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #888;">No donations recorded yet.</td></tr>';
      } else {
        historyTable.innerHTML = history
          .map(
            (d) => `
          <tr>
            <td>#${d.id}</td>
            <td>${d.donor_username || user.username}</td>
            <td><strong>${d.blood_group}</strong></td>
            <td>${d.component}</td>
            <td>${d.quantity} unit(s)</td>
            <td>${d.donation_date}</td>
          </tr>
        `
          )
          .join('');
      }
    } catch (err) {
      historyTable.innerHTML = `<tr><td colspan="6" class="alert-danger">${err.message}</td></tr>`;
    }
  }
});

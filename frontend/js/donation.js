/**
 * BBMS Blood Donation Recording Logic
 *
 * BBMS-F-010: Staff record donation.
 * BBMS-F-011: 90-day eligibility check feedback.
 * BBMS-F-012: Updated stock display.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const donationForm = document.getElementById('donation-form');
  const alertBox = document.getElementById('alert-box');
  const successCard = document.getElementById('success-card');

  // Pre-fill today's date
  const dateInput = document.getElementById('donationDate');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
  }

  function showAlert(msg, isSuccess = false) {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = `alert ${isSuccess ? 'alert-success' : 'alert-danger'}`;
    alertBox.style.display = 'block';
  }

  function hideAlert() {
    if (!alertBox) return;
    alertBox.style.display = 'none';
  }

  if (donationForm) {
    donationForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();
      if (successCard) successCard.style.display = 'none';

      const payload = {
        donorId: parseInt(donationForm.donorId.value, 10),
        bloodGroup: donationForm.bloodGroup.value,
        component: donationForm.component.value,
        quantity: parseInt(donationForm.quantity.value, 10),
        donationDate: donationForm.donationDate.value,
      };

      try {
        const response = await apiFetch('/donations', {
          method: 'POST',
          body: JSON.stringify(payload),
        });

        showAlert('Donation recorded successfully!', true);

        if (successCard) {
          successCard.style.display = 'block';
          document.getElementById('success-donation-id').textContent = response.donationId;
          document.getElementById('success-updated-stock').textContent = response.updatedStock;
        }

        donationForm.reset();
        if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
      } catch (err) {
        showAlert(err.message || 'Failed to record donation.');
      }
    });
  }
});

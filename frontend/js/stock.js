/**
 * BBMS Blood Inventory Stock View Logic
 *
 * BBMS-F-020: Real-time stock counts by blood group and component.
 * Colour-coded stock levels (red for low stock <= 3 units).
 */

document.addEventListener('DOMContentLoaded', async () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const stockContainer = document.getElementById('stock-container');
  const alertBox = document.getElementById('alert-box');

  function showAlert(msg) {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = 'alert alert-danger';
    alertBox.style.display = 'block';
  }

  try {
    const stockList = await apiFetch('/inventory');

    if (!stockList || stockList.length === 0) {
      stockContainer.innerHTML = '<p style="color: #666;">No inventory records found. Run seed_demo to populate data.</p>';
      return;
    }

    stockContainer.innerHTML = stockList
      .map((item) => {
        const isLow = item.units_available <= 3;
        const lowClass = isLow ? 'stock-low' : '';
        const badge = isLow
          ? '<span class="badge badge-low">Low Stock</span>'
          : '<span class="badge badge-adequate">Adequate</span>';

        return `
          <div class="stock-card ${lowClass}">
            <div>
              <div class="stock-blood-group">${item.blood_group}</div>
              <div class="stock-component">${item.component_display || item.component}</div>
            </div>
            <div>
              <div class="stock-count">${item.units_available} <span style="font-size: 0.9rem; font-weight: normal; color: #666;">units</span></div>
              ${badge}
            </div>
          </div>
        `;
      })
      .join('');
  } catch (err) {
    showAlert(err.message || 'Failed to load inventory stock. Donors do not have permission to view stock.');
  }
});

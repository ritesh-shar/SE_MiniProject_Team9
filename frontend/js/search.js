/**
 * BBMS Blood Search UI Logic
 *
 * BBMS-F-030: Search available blood units by blood group and component.
 * Owner: Ritesh Babu Reddy (PES2UG24CS403) - PR #4
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!auth.isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }

  const searchForm = document.getElementById('search-form');
  const resultsContainer = document.getElementById('search-results');
  const alertBox = document.getElementById('alert-box');

  function showAlert(msg) {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = 'alert alert-danger';
    alertBox.style.display = 'block';
  }

  function hideAlert() {
    if (!alertBox) return;
    alertBox.style.display = 'none';
  }

  if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const bloodGroup = searchForm.bloodGroup.value;
      const component = searchForm.component.value;

      const params = new URLSearchParams();
      if (bloodGroup) params.append('bloodGroup', bloodGroup);
      if (component) params.append('component', component);

      try {
        const results = await apiFetch(`/inventory/search?${params.toString()}`);

        if (!results || results.length === 0) {
          resultsContainer.innerHTML = '<p style="color: #666; margin-top: 1rem;">No matching blood units available in stock.</p>';
          return;
        }

        resultsContainer.innerHTML = `
          <div class="stock-grid" style="margin-top: 1.5rem;">
            ${results
              .map((item) => {
                const isLow = item.units_available <= 3;
                const lowClass = isLow ? 'stock-low' : '';
                const badge = isLow
                  ? '<span class="badge badge-low">Low Stock</span>'
                  : '<span class="badge badge-adequate">In Stock</span>';

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
              .join('')}
          </div>
        `;
      } catch (err) {
        showAlert(err.message || 'Error searching inventory. Make sure you have permission to search.');
      }
    });
  }
});

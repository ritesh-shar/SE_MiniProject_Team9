/**
 * BBMS Authentication UI Logic (Login & Register)
 *
 * BBMS-F-001: Donor registration.
 * BBMS-F-002: User login and JWT retrieval.
 */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const alertBox = document.getElementById('alert-box');

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

  // Handle Login (BBMS-F-002)
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const username = loginForm.username.value.trim();
      const password = loginForm.password.value;

      try {
        const data = await apiFetch('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ username, password }),
        });

        const tokenPayload = auth.parseJwt(data.access);
        const user = {
          username: username,
          role: (tokenPayload && tokenPayload.role) || (tokenPayload && tokenPayload.user_role) || 'donor',
          id: (tokenPayload && tokenPayload.user_id) || null,
        };

        // If the token didn't carry role directly, infer from username or query profile
        if (username.includes('staff')) user.role = 'staff';
        else if (username.includes('hosp')) user.role = 'hospital';
        else if (username.includes('admin')) user.role = 'admin';

        auth.setAuth(data.access, data.refresh, user);
        window.location.href = 'dashboard.html';
      } catch (err) {
        showAlert(err.message || 'Invalid username or password.');
      }
    });
  }

  // Handle Registration (BBMS-F-001)
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const username = registerForm.username.value.trim();
      const email = registerForm.email.value.trim();
      const password = registerForm.password.value;
      const blood_group = registerForm.blood_group.value;
      const phone = registerForm.phone.value.trim();

      try {
        const data = await apiFetch('/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            username,
            email,
            password,
            blood_group,
            phone,
          }),
        });

        showAlert('Registration successful! Redirecting to login...', true);
        setTimeout(() => {
          window.location.href = 'index.html';
        }, 1500);
      } catch (err) {
        showAlert(err.message || 'Registration failed. Please check your details.');
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const passwordToggle = document.querySelector('.password-toggle');
  if (passwordToggle) {
    passwordToggle.addEventListener('click', function () {
      const passwordInput = document.getElementById('password-field');
      const icon = passwordToggle.querySelector('i');
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
      } else {
        passwordInput.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
      }
    });
  }

  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const sidebar = document.getElementById('sidebar');
  if (mobileMenuToggle && sidebar) {
    mobileMenuToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  document.querySelectorAll('.alert-dismissible .btn-close').forEach(function (button) {
    button.addEventListener('click', function () {
      button.closest('.alert').remove();
    });
  });
});

$(document).ready(function () {
  // Function to handle form submission via AJAX
  function handleLogin(event) {
      event.preventDefault(); // Ensure this line is not causing issues

      // Capture form data including the CSRF token
      var formData = {
          email: $('#email').val(),
          password: $('#password').val(),
          csrf_token: $('#csrf_token').val()
      };

      // Set the CSRF token in the headers
      $.ajaxSetup({
          headers: {
              'X-CSRFToken': $('#csrf_token').val()
          }
      });

      // Send the AJAX request
      $.ajax({
          url: '/api/login',
          type: 'POST',
          data: formData,
          success: function (response) {
              if (response.success) {
                  console.log('Login successful');
                  // Redirect
                  window.location.href = '/';

              } else {
                  console.log('Login failed:', response.message);
              }
          },
          error: function (xhr, status, error) {
              console.log('Error during login:', error);
          }
      });
  }

  // Add event listener for form submission
  $('#loginForm').submit(handleLogin);
});

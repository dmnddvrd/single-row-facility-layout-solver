const loginUser = (userData) => {
  $.ajax('/users/login', {
    type: 'post',
    data: userData,
    dataType: 'json',
    success(response) {
      console.log(response);
      window.location.href = '/';
    },
    error(err) {
      console.log(err);
      $('#err-msg').text('Invalid Email and Password combination');
    },
  });
};

$().ready(() => {
  $('#login-btn').click(() => {
    const userData = {
      email: $('#email').val(),
      password: $('#password').val(),
    };
    loginUser(userData);
  });
});

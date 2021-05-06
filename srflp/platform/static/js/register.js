const registerUser = (userData) => {
  $.ajax('/users/create', {
    type: 'post',
    data: userData,
    dataType: 'json',
    success(response) {
      console.log(response);
      window.location.href = '/login';
    },
    error(err) {
      console.log(err);
      $('#err-msg').css('display', 'block');
      $('#err-msg').text(err.responseJSON.error);
    },
  });
};

$(document).ready(() => {
  $('#register-btn').click(() => {
    const user = {
      name: $('#name').val(),
      email: $('#email').val(),
      username: $('#username').val(),
      password: $('#password').val(),
    };
    registerUser(user);
  });
});

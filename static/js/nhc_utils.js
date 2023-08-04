function checkPasswordsMatched(form) {
    var password = form.password.value;
    var password2 = form.password2.value;
    var text = "Ошибка: неверная длина пароля, укажите минимум 5 и максимум 20 символов"
    var text2 = "Ошибка: введенные пароли не совпадают"
    var message = document.getElementById('message');
    var button = document.activeElement.getAttribute('value');

    if (button === 'cancel') {return true;}

    if (password.length < 5 || password.length > 20){
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    }
    if (password !== password2){
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text2;
        message.style.display = 'block'
        return false;
    }else {
        if (button === 'reset'){
            return true
        } else {
            return true;
        }
    }
  }
function checkLogin(form) {
    var login = form.login.value;
    var button = document.activeElement.getAttribute('value');

    if (button === 'cancel') {return true;}
    
    var text = "Ошибка длинны логина (должна быть от 3-х до 15-ти знаков)"
    var message = document.getElementById('message');

    if (login.length < 3 || login.length > 15) {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
      return false;
    }else{
        return checkPasswordsMatched(form);
    }
  }

function checkRole(form) {
    var role = form.role.value;
    var text = "Ошибка: ошибка корректности указанного значения роли"
    var message = document.getElementById('message');

    if (role !== "user" && role !== "superuser"){
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    }else{
        return validate(form);
    }
  }

function checkPassword(form) {
  var password = form.password.value;
  var text = "Ошибка: неверная длина пароля";
  var message = document.getElementById('message');

  if (password.length < 5 || password.length > 20) {
      document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
      document.querySelector('p[id=text_message]').textContent = text;
      message.style.display = 'block';
      return false;
  } else {
      return checkPasswordsMatched(form);
  }
}

function validateEmail(email) {
    var re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    return re.test(String(email).toLowerCase());
}

    // validate email and send form after success validation
function validate(form) {
    var email = form.email.value;
    var text = "Ошибка: ошибка корректности указанного email"
    var message = document.getElementById('message');

    if (email === '') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = 'Введите email';
        message.style.display = 'block'
        return false;
    }

    if (validateEmail(email)) {
        return checkLogin(form);
    } else {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    }
}

$(document).on('click', '.password-control', function(){
    if ($('#password').attr('type') === 'password'){
        $(this).addClass('view');
        $('#password').attr('type', 'text');
    } else {
        $(this).removeClass('view');
        $('#password').attr('type', 'password');
    }
    return false;
});

$(document).on('click', '.password-control2', function(){
    if ($('#password2').attr('type') === 'password'){
        $(this).addClass('view');
        $('#password2').attr('type', 'text');
    } else {
        $(this).removeClass('view');
        $('#password2').attr('type', 'password');
    }
    return false;
});

$(document).on('click', '.current-password-control', function(){
    if ($('#current_password').attr('type') === 'password'){
        $(this).addClass('view');
        $('#current_password').attr('type', 'text');
    } else {
        $(this).removeClass('view');
        $('#current_password').attr('type', 'password');
    }
    return false;
});

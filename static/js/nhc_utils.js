function checkPasswordsMatched(form) {
    var password = form.password.value;
    var password2 = form.password2.value;
    var text = "Ошибка: неверная длинная пароля, укажите минимум 5 и максимум 20 символов"
    var text2 = "Ошибка: введенные пароли не совпадают"
    var message = document.getElementById('message');

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
        return checkLogin(form);
    }
  }
function checkLogin(form) {
    var login = form.login.value;
    
    var text = "Ошибка длинны логина (должна быть от 3-х до 15-ти знаков)"
    var message = document.getElementById('message');

    if (login.length < 3 || login.length > 15) {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
      return false;
    }else{
        return validate(form);
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
        return true;
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

    if (validateEmail(email)) {
        return checkRole(this);
    } else {
        message.style.display = 'block'
        document.querySelector('p[id=text_message]').textContent = text;
        return false;
    }
}
// $(function() {
//     $('#extension').click(
//         function (form) {
//             var reference_point = form.reference_point.value;
//             var period = form.period.value;
//             var text = "Ошибка: выберите срок продления доступа и от какой даты считать";
//
//             if (reference_point === "") {
//                 alert(text);
//                 return false;
//             } else {
//                 if (period === "") {
//                     alert(text);
//                     return false;
//                 } else {
//                     return true;
//                 }
//             }
//         });
// });
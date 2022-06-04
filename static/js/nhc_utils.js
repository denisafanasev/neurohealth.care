function checkPasswordsMatched(form) {
    var password = form.password.value;
    var password2 = form.password2.value;
    var text = "Ошибка: неверная длинная пароля, укажите минимум 5 и максимум 20 символов"
    var text2 = "Ошибка: введенные пароли не совпадают"

    if (password.length < 5 || password.length > 20){
        alert(text);
        return false;
    }
    if (password !== password2){
        alert(text2);
        return false;
    }else {
        return checkLogin(form);
    }
  }
function checkLogin(form) {
    var login = form.login.value;
    var text = "Ошибка: ошибка корректности указанного логина пользователя"

    if (login.length < 3 || login.length > 11) {
      alert(text);
      return false;
    }else{
        return checkRole(form);
    }
  }

function checkRole(form) {
    var role = form.role.value;
    var text = "Ошибка: ошибка корректности указанного значения роли"

    if (role !== "user" && role !== "superuser"){
        alert(text);
        return false;
    }else{
        return true;
    }
  }

function checkPassword(form) {
  var password = form.password.value;
  var text = "Ошибка: неверная длина пароля"

  if (password.length < 5 || password.length > 20) {
    alert(text);
    return false;
  } else {
    return checkPasswordsMatched(form);
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
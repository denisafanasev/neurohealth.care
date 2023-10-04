function checkPasswordsMatched(form) {
    var password = form.password.value;
    var password2 = form.password2.value;
    var text = "Ошибка: неверная длина пароля, укажите минимум 5 и максимум 20 символов"
    var text2 = "Ошибка: введенные пароли не совпадают"
    var message = document.getElementById('message');
    var button = document.activeElement.getAttribute('value');

    if (button === 'cancel') {
        return true;
    }

    if (password.length < 5 || password.length > 20) {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    }
    if (password !== password2) {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text2;
        message.style.display = 'block'
        return false;
    } else {
        if (button === 'reset') {
            return true
        } else {
            return true;
        }
    }
}

function checkLogin(form) {
    var login = form.login.value;
    var button = document.activeElement.getAttribute('value');

    if (button === 'cancel') {
        return true;
    }

    var text = "Ошибка длинны логина (должна быть от 3-х до 15-ти знаков)"
    var message = document.getElementById('message');

    if (login.length < 3 || login.length > 15) {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    } else {
        return true;
    }
}

function checkRole(form) {
    var role = form.role.value;
    var text = "Ошибка: ошибка корректности указанного значения роли"
    var message = document.getElementById('message');

    if (role !== "user" && role !== "superuser") {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    } else {
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
        return true;
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
        return true
    } else {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = text;
        message.style.display = 'block'
        return false;
    }
}

function checkData(form) {
    const role = form.role.value;
    const probationers_number = form.probationers_number.value;
    const user_name = form.user_name.value;
    const message = document.getElementById('message');

    if (role === 'placeholder') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = "Выберите роль пользователю.";
        message.style.display = 'block'
        return false;
    }
    if (probationers_number === 'placeholder') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = "Выберите количество доступных тестируемых для пользователя.";
        message.style.display = 'block'
        return false;
    }
    if (user_name === '') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = "Введите имя пользователя";
        message.style.display = 'block'
        return false;
    }

    return true
}

function checkExtension(form) {
    const period = form.period.value;
    const reference_point = form.reference_point.value;
    const message = document.getElementById('message');

    if (period === 'placeholder') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = "Выберите срок, на который хотите продлить доступ пользователю.";
        message.style.display = 'block'
        return false;
    }

    if (reference_point === 'placeholder') {
        document.querySelector('h3[id=title_message]').textContent = 'Ошибка';
        document.querySelector('p[id=text_message]').textContent = "Выберите начальное время отсчета.";
        message.style.display = 'block'
        return false;
    }

    return true;
}

function checkUserForm(form) {
    if (checkLogin(form) === false) {
        return false
    }

    if (!checkPasswordsMatched(form)) {
        return false
    }

    if (!checkRole(form)) {
        return false
    }

    if (!validate(form)) {
        return false
    }

    if (!checkData(form)) {
        return false
    }

    return checkExtension(form);



}
"""
app configuration
"""

import pathlib

VERSION = "1.1.0"
APP_NAME = "NeuroHealth"

if str(pathlib.Path().resolve()).find("prod")!=-1:
    ENVIRONMENT = "prod"
else:
    ENVIRONMENT = "dev"

# DATA_FOLDER = "../data/"
DATA_FOLDER = "../neurohealth.care.data."+ENVIRONMENT+"/"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"

SECRET_KEY = 'my_secret_key'
SECURITY_PASSWORD_SALT = 'my_security_password_salt'

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# mail accounts
MAIL_DEFAULT_SENDER = 'from@example.com'

# gmail authentication
MAIL_USERNAME = ""
MAIL_PASSWORD = ""

# probationer settings
EDUCATIONAL_INSTITUSION = ["Гимназия", "Массовая школа", "Коррекционная школа", "Домашнее обучение"]

# user settings
PROBATIONERS_NUMBER = [5, 10, 15, 20, 25, 30]
ROLE = ["user", "superuser"]

EDUCATION_MODULE_EXPIRATION_DATE = [{"name_period": "1 месяц", "amount": 1},
                                    {"name_period": "2 месяц", "amount": 2},
                                    {"name_period": "3 месяца", "amount": 3},
                                    {"name_period": "6 месяцев", "amount": 6},
                                    {"name_period": "1 год", "amount": 12}]

REFERENCE_POINT = [{"name_point": "от даты окончания", "value": "end"},
                   {"name_point": "от текущей даты", "value": "today"}]


SUPERUSER_MENU = [
    {"module": "Центр управления", "name": "Пользователи", "endpoint": "user_manager", "icon": "users"},
    {"module": "Центр управления", "name": "Настройки", "endpoint": "age_range_list", "icon": "settings"},
    {"module": "Центр управления", "name": "Домашние задания", "endpoint": "education_home_tasks", "icon": "edit"},
    {"module": "Центр управления", "name": "Обучающие потоки", "endpoint": "learning_streams", "icon": "crop"}
]

EDUCATION_MENU = [
    {"module": "Центр обучения", "name": "Я - НейроМама", "endpoint": "education_list_courses", "icon": "video"}
]

EVOLUTION_MENU = [
    {"module": "Центр развития", "name": "Мои тестируемые", "endpoint": "probationers", "icon": "users"},
    {"module": "Центр развития", "name": "Диагностика", "endpoint": "probes", "icon": "list"},
    {"module": "Центр развития", "name": "Результаты", "endpoint": "results", "icon": "activity"},
    {"module": "Центр развития", "name": "Занятия", "endpoint": "corrections", "icon": "trending-up"}
]

MAIN_MENU = [
    {"module": "", "name": "Рабочий стол", "endpoint": "main_page", "icon": "sliders"}  
]

SETTINGS_MENU = [
    {"name": "Справочник оценочных значений", "endpoint": "estimated_values"},
    {"name": "Справочник диапазонов возрастов", "endpoint": "age_range_list"},
]

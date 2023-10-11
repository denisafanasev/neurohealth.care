"""
app configuration
"""
import yaml
import pathlib

VERSION = "1.3.0"
APP_NAME = "NeuroHealth"

if str(pathlib.Path().resolve()).find("prod")!=-1:
    ENVIRONMENT = "prod"
else:
    ENVIRONMENT = "dev"

# DATA_FOLDER = "../data/"
DATA_FOLDER = "../neurohealth.care.data." + ENVIRONMENT + "/"
CONFIG_FILE_NAME = "config.yaml"

# TODO: надо бы проверить что папка существует и создать ее, если ее нет

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"

SECRET_KEY = 'my_secret_key_'
SECURITY_PASSWORD_SALT = 'my_security_password_salt'

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

LANGUAGES = [
    {
        'lang_code': 'ru',
        'img_name': 'ru.png',
        'title': 'Русский'
    },
    {
        'lang_code': 'en',
        'img_name': 'gb.png',
        'title': 'English'
    }
]
MODELS_FOR_IMPORT_IN_SQL = ['users', 'courses_list', 'modules', 'lessons']

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

FILTERS_HOMEWORK_LIST = {
    'chat_without_homework': 'Чаты без домашних работ',
    'homework_verified': 'Проверенные домашние работы',
    'education_home_tasks': 'Непроверенные домашние работы',
}

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
    {"module": "Центр управления", "name": "Обучающие потоки", "endpoint": "education_streams", "icon": "crop"}
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


AMOUNT_EDUCATION_STREAMS = 5


def ga_id() -> str:
    """
    Возвращает идентификатор GA из системного файла настроек

    Returns:
        String: идентификатор GA
    """    

    ga_id = "G-ХХХХХХХХХХ"

    try:        
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        ga_id = cfg['CONFIG']['ga_id']

    except:
        ga_id = "G-not-found"

    return ga_id

def cdp_id() -> str:
    """
    Возвращает идентификатор CDP из системного файла настроек

    Returns:
        String: идентификатор CDP
    """    

    cdp_id = ''

    try:
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        cdp_id = cfg['CONFIG']['cdp_id']

    except:
        cdp_id = 'not-found'

    return cdp_id


def sentry_dsn() -> str:
    """
    Возвращает идентификатор sentry из системного файла настроек

    Returns:
        String: идентификатор GA
    """   

    sentry_dsn = ""

    try:        
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        sentry_dsn = cfg['CONFIG']['sentry_dsn']

    except:
        sentry_dsn = "not-found"

    return sentry_dsn

def app_support_channel() -> str:
    """
    Возвращает ссылку на канал поддержки пользователей из системного файла настроек

    Returns:
        String: идентификатор GA
    """   

    user_support_channel = ""

    try:        
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        user_support_channel = cfg['CONFIG']['user_support_channel']

    except:
        user_support_channel = "not-found"

    return user_support_channel

def data_adapter() -> str:
    """
    Возвращает идентификатор адаптера данных из системного файла настроек

    Returns:
        String: идентификатор адаптера данных
    """   

    _data_adapter = None

    try:        
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        _data_adapter = cfg['CONFIG']['data_adapter']
    
    except:
        pass

    return _data_adapter

def PostgreSQLDataAdapter_connection_string() -> str:
    """
    Возвращает строку подключения для PostgreSQL адаптера  из системного файла настроек

    Returns:
        String: строка подключения для PostgreSQL адаптера
    """   

    _PostgreSQLDataAdapter_connection_string = None

    try:        
        with open(DATA_FOLDER + CONFIG_FILE_NAME, "r") as f:
            cfg = yaml.safe_load(f)
        
        _PostgreSQLDataAdapter_connection_string = cfg['CONFIG']['PostgreSQLDataAdapter_connection_string']
    
    except:
        pass

    return _PostgreSQLDataAdapter_connection_string

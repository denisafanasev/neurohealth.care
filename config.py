VERSION = "0.0.7"
APP_NAME = "CleverHEALTH"
ENVIRONMENT = "production"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"


SUPERUSER_MENU = [    
    {"module": "Центр управление", "name": "Пользователи", "endpoint": "user_manager", "icon": "users"},
    {"module": "Центр управление", "name": "Настройки", "endpoint": "settings", "icon": "settings"}
]

MAIN_MENU = [

    {"module": "", "name": "Рабочий стол", "endpoint": "main_page", "icon": "sliders"},
    
    {"module": "Центр тестирование", "name": "Коррекция", "endpoint": "corrections", "icon": "trending-up"},
    {"module": "Центр тестирование", "name": "Протоколы", "endpoint": "probes", "icon": "list"},
    {"module": "Центр тестирование", "name": "Результаты", "endpoint": "results", "icon": "activity"},
    {"module": "Центр тестирование", "name": "Тестируемые", "endpoint": "probationers", "icon": "users"},
    
]

SETTINGS_MENU = [
    {"name": "Справочник оценочных значений", "endpoint": "estimated_values"},
    {"name": "Справочник диапазонов возрастов", "endpoint": "age_range_list"}
]
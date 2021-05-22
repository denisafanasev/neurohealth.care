VERSION = "0.0.2"
APP_NAME = "Neuro Health"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"

SUPERUSER_MENU = [    
    {"module": "Центр управление", "name": "Пользователи",
        "endpoint": "user_manager", "icon": "users"},
    {"module": "Центр управление", "name": "Настройки",
        "endpoint": "index", "icon": "settings"}
]

MAIN_MENU = [
    {"module": "", "name": "Рабочий стол", "endpoint": "index", "icon": "sliders"},
    
    {"module": "Центр тестирование", "name": "Испытуемые",
        "endpoint": "index", "icon": "users"},
    {"module": "Центр тестирование", "name": "Испытания",
     "endpoint": "index", "icon": "list"},
     {"module": "Центр тестирование", "name": "Результаты",
        "endpoint": "index", "icon": "trending-up"},

     {"module": "", "name": "Мой профиль", "endpoint": "user_profile", "icon": "user"}
    
]
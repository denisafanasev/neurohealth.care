VERSION = "0.0.2"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"

SUPERUSER_MENU = [
    {"module": "System", "name": "Task manager",
        "endpoint": "index", "icon": "layers"},
    {"module": "System", "name": "Segmentator settings",
        "endpoint": "index", "icon": "settings"},
    {"module": "System", "name": "User manager",
        "endpoint": "user_manager", "icon": "user"}
]

MAIN_MENU = [
    {"module": "", "name": "Рабочий стол", "endpoint": "index", "icon": "sliders"},
    
    {"module": "Тестирование", "name": "Результаты",
        "endpoint": "index", "icon": "trending-up"},
    {"module": "Тестирование", "name": "Дети",
        "endpoint": "index", "icon": "users"},
    {"module": "Тестирование", "name": "Тесты",
     "endpoint": "index", "icon": "list"}
]

VERSION = "0.0.3"
APP_NAME = "Neuro Health"

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
    {"module": "Центр тестирование", "name": "Пробы", "endpoint": "probes", "icon": "list"},
    {"module": "Центр тестирование", "name": "Результаты", "endpoint": "results", "icon": "activity"},
    {"module": "Центр тестирование", "name": "Испытуемые", "endpoint": "probationers", "icon": "users"}
    
]
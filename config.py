"""
app configuration
"""

import pathlib

VERSION = "0.0.9.1"
APP_NAME = "NeuroHealth"

if str(pathlib.Path().resolve()).find("prod")!=-1:
    ENVIRONMENT = "prod"
else:
    ENVIRONMENT = "dev"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"


SUPERUSER_MENU = [
    {"module": "Центр управления", "name": "Пользователи", "endpoint": "user_manager", "icon": "users"},
    {"module": "Центр управления", "name": "Настройки", "endpoint": "age_range_list", "icon": "settings"},
        {"module": "Центр управления", "name": "Домашние задания",
        "endpoint": "education_home_tasks", "icon": "edit"},
]

EDUCATION_MENU = [
    {"module": "Школа нейропсихологии", "name": "Вводный модуль",
        "endpoint": "education_introduction_course", "icon": "monitor"},
    {"module": "Школа нейропсихологии", "name": "Основные модули",
        "endpoint": "education_main_courses", "icon": "video"},
    {"module": "Школа нейропсихологии", "name": "Список курсов",
        "endpoint": "education_list_courses", "icon": "video"}
]

MAIN_MENU = [

    {"module": "", "name": "Рабочий стол", "endpoint": "main_page", "icon": "sliders"},
    
    {"module": "Центр тестирование", "name": "Тестируемые", "endpoint": "probationers", "icon": "users"},
    {"module": "Центр тестирование", "name": "Протоколы", "endpoint": "probes", "icon": "list"},
    {"module": "Центр тестирование", "name": "Результаты", "endpoint": "results", "icon": "activity"},

    {"module": "Центр коррекции", "name": "Коррекция", "endpoint": "corrections", "icon": "trending-up"},
    
]

SETTINGS_MENU = [
    {"name": "Справочник оценочных значений", "endpoint": "estimated_values"},
    {"name": "Справочник диапазонов возрастов", "endpoint": "age_range_list"}
]

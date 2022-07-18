import config


def set_ga_id():
    """
    Возвращает идентификатор GA из файла настройки

    Returns:
        String: идентификатор GA
    """    

    ga_id = "G-ХХХХХХХХХХ"

    try:
        with open(config.DATA_FOLDER + 'ga.id') as f:
            ga_id = f.read().splitlines()
    
    except:
        pass

    return ga_id[0]
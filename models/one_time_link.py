from datetime import datetime
from typing import Union


class OneTimeLink:
    """
    Одноразовая ссылка
    """
    def __init__(self, _id: int = None, _user_id: int = None, _created_date: Union[str, datetime] = '', _link: str = '',
                 _is_active: bool = False, _type: str = ''):

        self.id = _id
        self.user_id = _user_id
        self.created_date = self.get_created_date(_created_date)
        self.link = _link
        self.is_active = _is_active
        self.type = _type

    def get_created_date(self, _created_date: Union[str, datetime]):

        if _created_date == '':
            return datetime.today()
        elif isinstance(_created_date, datetime):
            return _created_date.strftime('%d/%m/%Y')
        else:
            return _created_date

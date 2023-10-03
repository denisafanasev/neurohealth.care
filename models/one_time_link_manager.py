import datetime

import shortuuid
from datetime import datetime

from data_adapters.data_store import DataStore
from error import OneTimeLinkManagerException
from models.one_time_link import OneTimeLink


class OneTimeLinkManager:
    """

    """
    def one_time_link_row_to_one_time_link(self, _data_row: dict) -> OneTimeLink:
        """

        """
        one_time_link = OneTimeLink(_id=_data_row['doc_id'], _user_id=_data_row['user_id'],
                                    _is_active=_data_row['is_active'], _link=_data_row['link'],
                                    _type=_data_row['type'])

        if _data_row.get('created_date') is not None:
            one_time_link.created_date = datetime.strptime(_data_row['created_date'], '%d/%m/%Y')

        return one_time_link

    def created_one_time_link(self, _user_id: int, _type: str) -> OneTimeLink:
        """
        Создает одноразовую ссылку, записывает в БД и возвращает ее
        Args:
            _user_id:
            _type: тип ссылки(для чего она нужна)

        Returns:
            OneTimeLink: данные об одноразовой ссылки
        """

        data_store = DataStore('one_time_links')

        one_time_link_list = [0]
        while one_time_link_list:
            link = shortuuid.uuid()

            one_time_link_list = data_store.get_rows({'link': link})

        one_time_link = OneTimeLink(_user_id=_user_id, _is_active=True,
                                    _link=link, _type=_type)

        one_time_link_data = {
            'user_id': one_time_link.user_id,
            'link': one_time_link.link,
            'type': one_time_link.type,
            'is_active': one_time_link.is_active,
            'created_date': one_time_link.created_date.strftime('%d/%m/%Y')
        }

        data_store.insert_row(one_time_link_data)

        return link

    def get_one_time_link(self, _link) -> OneTimeLink:
        """
        Возвращает данные об одноразовой ссылки
        Args:
            _link: одноразовая ссылка

        Returns:
            OneTimeLink: данные об одноразовой ссылки
        """
        data_store = DataStore('one_time_links')

        one_time_link_list = data_store.get_rows({'link': _link})
        if one_time_link_list:
            one_time_link = self.one_time_link_row_to_one_time_link(one_time_link_list[0])
            if not one_time_link.is_active:
                raise OneTimeLinkManagerException('Данная ссылка уже была использована')

            return one_time_link

    def deactivate_link(self, _id: int) -> None:
        """
        Деактивирует одноразовую ссылку
        Args:
            _id: ID ссылки
        """
        data_store = DataStore('one_time_links')

        data_store.update_row_by_id({'is_active': False}, _id)

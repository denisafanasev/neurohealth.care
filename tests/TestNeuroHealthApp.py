import unittest

from inspect import getsourcefile
import inspect
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

# import utils.ada as ada

import app as tested_app
from data_adapters.data_store import DataStore
from models.user import User
from models.user_manager import UserManager


class TestNeuroHealthApp(unittest.TestCase):

  def setUp(self):
    pass

  # ----------------------------------------------------------------
  # тестирование модуля ada
  def test_size_to_format_view(self):
  
    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'

  def test_size_to_format_view_2(self):

    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'
  
  def test_size_to_format_view_3(self):

    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'

  # ----------------------------------------------------------------
  # тестирование модуля User
  def test_User(self):

    print(inspect.currentframe().f_code.co_name)
    user = User(1, "test", "test", "test", "user")
  
  # ----------------------------------------------------------------
  # тестирование модуля DataStore
  def test_add_row(self):

    print(inspect.currentframe().f_code.co_name)
    data_store = DataStore("test")
    rows = data_store.add_row({"data": "test", "data2": "test2"})

  def test_get_rows(self):

    print(inspect.currentframe().f_code.co_name)
    data_store = DataStore("test")
    rows = data_store.get_rows()
  
  def test_row_by_id(self):

    print(inspect.currentframe().f_code.co_name)
    data_store = DataStore("test")
    rows = data_store.get_row_by_id(0)
  
  def test_get_rows_count(self):

    print(inspect.currentframe().f_code.co_name)
    data_store = DataStore("test")
    rows = data_store.get_rows_count()
  
  # ----------------------------------------------------------------
  # тестирование модуля UserManager

  def test_hash_password(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    assert(user_manager.hash_password("test")) == '098f6bcd4621d373cade4e832627b4f6'
  
  def test_validate_password(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    user_manager.validate_password("admin")
  
  def test_validate_role(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    user_manager.validate_role("user")
  
  def test_validate_login(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    user_manager.validate_login("admin")
  
  def test_is_there_users(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    result = user_manager.is_there_users()
  
  def test_create_user(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    result = user_manager.create_user("test", "test", "test", "test", "test", "user")
  
  def test_get_user(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    user = user_manager.get_user("test", "test")
  
  def test_get_user_by_id(self):

    print(inspect.currentframe().f_code.co_name)
    user_manager = UserManager()
    user = user_manager.get_user_by_id(1)
  
  
if __name__ == "__main__":

    unittest.main()

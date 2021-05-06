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


class TestNeuroHealthApp(unittest.TestCase):

  def setUp(self):
    pass

  # тестирование enbkbns ada
  def test_size_to_format_view(self):
  
    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'

  def test_size_to_format_view_2(self):

    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'
  
  def test_size_to_format_view_3(self):

    print(inspect.currentframe().f_code.co_name)
    assert(tested_app.ada.size_to_format_view(1024)) == '1.0Kb'

if __name__ == "__main__":

    unittest.main()

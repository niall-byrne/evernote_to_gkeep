import pytest
import os
import json
from unittest.mock import patch

from app.gkeep import Keeper

PATH = os.path.dirname(os.path.realpath(__file__))
NOTE_LIST = json.load(open(os.path.join(PATH, 'data', 'index.json')))


class TestWithKeep:

  @classmethod
  def setup_class(cls):
    with open(os.path.join(PATH, 'credentials', 'credentials.json')) as fh:
      cls.credentials = json.load(fh)
    cls.Keeper = Keeper(**cls.credentials)

  @patch('app.gkeep.gkeepapi.Keep.login')
  def test_login(self, login):
    self.__class__.Keeper.login()
    login.assert_called_with(self.__class__.credentials['username'],
                             self.__class__.credentials['password'])

  @pytest.mark.parametrize('note', NOTE_LIST)
  @patch('app.gkeep.gkeepapi.Keep.createNote')
  def test_create_keep_note(self, create_note, note):
    self.__class__.Keeper.create_note(note['title'], note['body'])
    assert create_note.mock_calls[0][1] == (
        note['title'],
        note['body'],
    )

  @pytest.mark.parametrize('note', NOTE_LIST)
  @patch('app.gkeep.gkeepapi.Keep.createLabel')
  def test_create_label(self, create_label, note):
    keep = self.__class__.Keeper
    keep.create_label('test-label')
    assert create_label.mock_calls[0][1] == ('test-label',)

  @classmethod
  def teardown_class(cls):
    pass

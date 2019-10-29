import pytest
import os
import json
from unittest.mock import patch

from click.testing import CliRunner

from main import cli

PATH = os.path.dirname(os.path.realpath(__file__))

NOTE_LIST = json.load(open(os.path.join(PATH, 'data', 'index.json')))

TEST_VALUES = [(['filename'] * 50, 1), (['filename'] * 200, 2),
               (['filename'] * 250, 3)]


class MockTextAttribute:

  def __init__(self, value):
    self.value = value

  @property
  def text(self):
    return self.value


class TestCLI:

  @pytest.mark.parametrize('test_values', TEST_VALUES)
  @patch('main.read_evernote_html')
  @patch('app.gkeep.Keeper.create_note')
  @patch('app.gkeep.gkeepapi.Keep.sync')
  @patch('app.gkeep.gkeepapi.Keep.login')
  @patch('main.glob.glob')
  def test_cli(self, glob, login, sync, create_note, read_note, test_values):

    username = 'me@gmail.com'
    password = 'hello'

    mock_note_data = (MockTextAttribute('mock_title'),
                      MockTextAttribute('mock_text'))

    glob.return_value = test_values[0]
    read_note.return_value = mock_note_data

    runner = CliRunner()
    runner.invoke(cli, [
        '--directory', 'mock_directory', '--username', username, '--password',
        password
    ])

    login.assert_called_with(username, password)
    assert glob.called
    assert len(sync.mock_calls) == test_values[1]
    assert len(read_note.mock_calls) == len(test_values[0])
    assert len(create_note.mock_calls) == len(test_values[0])

    for index, rvalue in enumerate(glob()):
      assert read_note.mock_calls[index][1] == (rvalue,)
      assert create_note.mock_calls[index][1] == (
          'mock_title',
          'mock_text',
      )

  @patch('main.read_evernote_html')
  @patch('app.gkeep.Keeper.create_note')
  @patch('app.gkeep.gkeepapi.Keep.sync')
  @patch('app.gkeep.gkeepapi.Keep.login')
  @patch('main.glob.glob')
  def test_cli_exception(self, glob, login, sync, create_note, read_note):

    username = 'me@gmail.com'
    password = 'hello'

    test_values = (['a'], 1)

    mock_note_data = (MockTextAttribute('mock_title'),
                      MockTextAttribute('mock_text'))

    glob.return_value = test_values[0]
    read_note.return_value = mock_note_data
    create_note.side_effect = Exception('Boom!')

    runner = CliRunner()
    runner.invoke(cli, [
        '--directory', 'mock_directory', '--username', username, '--password',
        password
    ])

    login.assert_called_with(username, password)
    assert glob.called
    assert len(sync.mock_calls) == 0
    assert len(read_note.mock_calls) == 1
    assert len(create_note.mock_calls) == 1

    for index, rvalue in enumerate(glob()):
      assert read_note.mock_calls[index][1] == (rvalue,)
      assert create_note.mock_calls[index][1] == (
          'mock_title',
          'mock_text',
      )

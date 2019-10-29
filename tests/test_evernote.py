import pytest
import os
import json

from app.evernote import read_evernote_html

PATH = os.path.dirname(os.path.realpath(__file__))
NOTE_LIST = json.load(open(os.path.join(PATH, 'data', 'index.json')))


class TestParsingEverNote:

  @pytest.mark.parametrize('note', NOTE_LIST)
  def test_parses_note_title(self, note):
    filename = os.path.join(PATH, 'data', note['filename'])
    title, body = read_evernote_html(filename)
    assert title.text == note['title']
    assert body.text == note['body']

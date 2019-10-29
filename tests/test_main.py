import pytest
import os
import json

from app.evernote import read_evernote_html
from app.gkeep import Keeper

PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(PATH, 'data', 'index.json')) as fh:
  NOTE_LIST = json.load(fh)


class TestParsingEverNote:

  @pytest.mark.parametrize('note', NOTE_LIST)
  def test_parses_note_title(self, note):
    filename = os.path.join(PATH, 'data', note['filename'])
    title, body = read_evernote_html(filename)
    assert title.text == note['title']
    assert body.text == note['body']


class TestIntegrationWithKeep:

  @classmethod
  def setup_class(cls):
    with open(os.path.join(PATH, 'credentials', 'credentials.json')) as fh:
      cls.credentials = json.load(fh)
    cls.Keeper = Keeper(**cls.credentials)

  def test_login(self):
    self.__class__.Keeper.login()
    assert self.__class__.Keeper.success is True

  @pytest.mark.parametrize('note', NOTE_LIST)
  def test_create_keep_note(self, note):
    gnote = self.__class__.Keeper.create_note(note['title'], note['body'])
    self.__class__.Keeper.keep.sync()
    assert gnote.title == note['title']
    assert gnote.text == note['body']
    gnote.delete()
    self.__class__.Keeper.keep.sync()

  @pytest.mark.parametrize('note', NOTE_LIST)
  def test_create_label(self, note):
    keep = self.__class__.Keeper

    label = keep.keep.findLabel('test-label')
    if label is not None:
      keep.keep.deleteLabel('test-label')  # Does not seem to work
      keep.sync()

    keep.create_label('test-label')
    label = keep.keep.findLabel('test-label')

    gnote = keep.create_note(note['title'], note['body'])
    gnote.labels.add(label)
    keep.sync()

    assert gnote.labels.get(label.id) != None

    gnote.delete()
    keep.sync()


  @classmethod
  def teardown_class(cls):
    pass

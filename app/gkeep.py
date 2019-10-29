"""Manages Access to the Google Keep API"""

import gkeepapi


class Keeper:

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.success = None
    self.keep = gkeepapi.Keep()
    self.label = None

  def login(self):
    self.success = self.keep.login(self.username, self.password)

  def create_label(self, name):
    self.label = self.keep.createLabel(name)

  def create_note(self, title, body):
    gnote = self.keep.createNote(title, body)
    return gnote

  def sync(self):
    self.keep.sync()

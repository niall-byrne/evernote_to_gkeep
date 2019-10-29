"""Evernote HTML to GKeep Script"""

# pylint: disable=E1120

import click
import glob
import os
import sys

from app.evernote import read_evernote_html
from app.gkeep import Keeper

BATCH_SIZE = 100


@click.command()
@click.option('--directory', default='import', metavar='PATH')
@click.option('--username', envvar='GKEEP_USERNAME', default='')
@click.option('--password', envvar='GKEEP_PASSWORD', default='')
def cli(directory, username, password):
  """Specify the directory where you have exported your Evernote Notes as
  HTML clippings, and this script will convert them into gKeep notes.

  Example 1)

  \b
  Read all notes in the import folder, and create Google Keep notes:
    main.py --username me@gmail.com --password mypass

  Example 2)

  \b
  Read all notes in the import folder, and create Google Keep notes:
    export GKEEP_USERNAME=me@gmail.com
    export GKEEP_PASSWORD=mypass
    main.py
  """
  files = glob.glob(os.path.join(directory, '*.html'))
  keep = Keeper(username, password)
  keep.login()

  count = 0
  current_batch = BATCH_SIZE

  for fname in files:
    count += 1
    title, text = read_evernote_html(fname)
    print("Importing: %s" % fname)
    try:
      keep.create_note(title.text, text.text)
    except Exception as unknown_exception:  # pylint: disable=W0703
      print("ERROR!")
      print(unknown_exception)
      sys.exit(127)

    if count >= current_batch or count == len(files):
      print("Synchronizing ...")
      keep.sync()
      current_batch = current_batch + BATCH_SIZE


if __name__ == '__main__':
  cli()

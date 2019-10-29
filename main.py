import click
import glob
import os

from app.evernote import read_evernote_html
from app.gkeep import Keeper

BATCH_SIZE = 100


@click.command()
@click.option('--directory', default='import', metavar='PATH')
@click.option('--username', envvar='GKEEP_USERNAME')
@click.option('--password', envvar='GKEEP_PASSWORD')
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

  for fname in files:
    count += 1
    title, text = read_evernote_html(fname)
    print("Importing: %s" % fname)
    print(text.text)
    try:
      keep.create_note(title.text, text.text)
    except Exception as e:
      print(e)
      exit(127)

    if count >= BATCH_SIZE:
      print("Synchronizing ...")
      keep.sync()
      count = 0


if __name__ == '__main__':
    cli()

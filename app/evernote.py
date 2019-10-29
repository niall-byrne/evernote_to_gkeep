"""Manages Notes Exported From Evernote"""

from bs4 import BeautifulSoup


def read_evernote_html(filename):

  with open(filename) as filehandle:
    soup = BeautifulSoup(filehandle, 'html.parser')
    return soup.title, soup.body

import os

from browser import html, document, timer
from .utils import LocalInterpreter
import inspect
from string import ascii_lowercase
import random
import logging
import json

RadiantServer = None


# # ----------------------------------------------------------------------
# def delay(t):
    # """"""
    # def wrap(fn):
        # def inset(*args, **kwargs):
            # print(f'DELAYING: {t}')
            # return timer.set_timeout(lambda: fn(*args, **kwargs), t)
        # return inset
    # return wrap


########################################################################
class RadiantAPI:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, class_, python=None, **kwargs):
        """"""
        if python[0] and python[0] != 'None':
            setattr(self, python[1], LocalInterpreter())

        self.body = document.select_one('body')
        self.head = document.select_one('head')


    # ----------------------------------------------------------------------
    def add_css_file(self, file):
        """"""
        document.select('head')[0] <= html.LINK(
            href=os.path.join('root', file), type='text/css', rel='stylesheet')

    # # ----------------------------------------------------------------------
    # def on_load(self, callback, evt='DOMContentLoaded'):
        # """"""
        # logging.warning('#' * 30)
        # logging.warning('#' * 30)
        # document.addEventListener('load', callback)
        # logging.warning('#' * 30)
        # logging.warning('#' * 30)


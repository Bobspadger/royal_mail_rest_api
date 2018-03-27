# -*- coding: utf-8 -*-

"""Main module."""
import requests
from .errors import NotAuthorised, GeneralError


class RoyalMailBaseClass():
    """
    BASE CLASS FOR SHIPPING
    """
    url = 'https://api.royalmail.net'


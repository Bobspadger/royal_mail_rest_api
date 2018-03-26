# -*- coding: utf-8 -*-

"""Main module."""
import requests
from .errors import NotAuthorised, GeneralError


class RoyalMailBaseClass():
    url = 'https://api.royalmail.net'
    """
    BASE CLASS FOR SHIPPING
    """
    pass

    def _test_error(self, response):
        """
        take requests object
        :param response:
        :return: useful error
        """
        if response.status_code == 401:
            raise NotAuthorised('Got 401 Not authorised')
        if response.status_code == 500:
            raise  GeneralError('Got an http 500 error')


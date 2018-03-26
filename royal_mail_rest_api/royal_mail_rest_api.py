# -*- coding: utf-8 -*-

"""Main module."""
import requests

class NotAuthorised(Exception):
    pass



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
            raise NotAuthorised


class TrackingApi(RoyalMailBaseClass):
    """
    Start class for royal mail shipping api
    """
    summary_url = 'mailPieces/{}/summary'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._create_headers()


    def _create_headers(self):
        self.header = {'X-IBM-Client-Id': self.client_id,
                       'X-IBM-Client-Secret': self.client_secret,
                       'accept': 'application/json'}

    def summary(self, tracking_number):
        """
        takes 13 digit tracking number and requests summary data
        :param tracking_number:
        :return: tracking_summary
        """
        summary_url = self.summary_url.format(tracking_number)
        result = requests.get('{}/{}'.format(self.url, summary_url), headers=self.header)
        self._test_error(result)
        return result.json()







if __name__ == '__main__':
    tracking_api = TrackingApi(CLIENT_ID, CLIENT_SECRET)
    test_tracking = tracking_api.summary('13_digit_tracking_number')

# -*- coding: utf-8 -*-

"""Main module."""
import requests
from .errors import NotAuthorised


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
    pod_url = 'mailPieces/{}/proofOfDelivery'
    history_url = 'mailPieces/{}/history'

    def __init__(self, client_id, client_secret):
        """
        Instantiate, store client_id and secret, build headers
        :param client_id:
        :param client_secret:
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._create_headers()

    def _create_headers(self):
        """
        Create the required headers for interacting with the tracking api
        :return: Nothing
        """
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


    def proof_of_delivery(self, tracking_number):
        """
        recover proof of delivery
        :param tracking_number:
        :return:
        """
        pod_url = self.summary_url.format(tracking_number)
        result = requests.get('{}/{}'.format(self.url, pod_url), headers=self.header)
        self._test_error(result)
        return result.json()


    def history(self, tracking_number):
        """
        Return history for a tracked item
        :param tracking_number:
        :return:
        """
        history_url = self.history_url.format(tracking_number)
        result = requests.get('{}/{}'.format(self.url, history_url), headers=self.header)
        self._test_error(result)
        return result.json()


if __name__ == '__main__':
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    TRACKING_NUMBER = ''
    tracking_api = TrackingApi(CLIENT_ID, CLIENT_SECRET)
    test_tracking = tracking_api.summary('13_digit_tracking_number')
    test_pod = tracking_api.proof_of_delivery(TRACKING_NUMBER)
    history_tracking = tracking_api.history(TRACKING_NUMBER)

    print(test_tracking)
    print(test_pod)
    print(history_tracking)

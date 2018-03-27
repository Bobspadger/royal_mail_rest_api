import requests
from royal_mail_rest_api.api import RoyalMailBaseClass


class ShippingApi(RoyalMailBaseClass):
    token_url = '/shipping/v2/token'

    def __init__(self, client_id, client_secret, username, password):
        """
        authenticate with the Shipping service.
        Password is an SHA1 hashed password. The royal mail develop tools have an html file to do this for you
        https://developer.royalmail.net/node/18564
        https://developer.royalmail.net/sites/developer.royalmail.net/files/rmg_shipping_api_v2_rest_password_generator_0.zip
        :param client_id:
        :param client_secret:
        :param username:
        :param password:
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self._create_headers()


    def _create_headers(self):
        self.header = {'X-IBM-Client-Id': self.client_id,
                       'X-IBM-Client-Secret': self.client_secret,
                       'x-rmg-user-name': self.username,
                       'x-rmg-password': self.password,
                       'accept': 'application/json'}


    def get_token(self):
        """

        Summary
        =======

        Method to get a JWT token

        Description
        -----------

        This method will accept a DMO/NEOPOST user name and password. On successful validation of the user credential it will issue a JWT token to the user which will be valid for 4 hours. On subsequent requests, user will pass the JWT token in the request header.

        :return:
        """


        result = requests.get('{}/{}'.format(self.url, self.token_url), headers=self.header)
        result.raise_for_status()
        result = result.json()
        self.token = result['token']


    def post_domestic(self):
        """

        Summary
        =======

        Operation to create a shipment

        Description
        -----------
        This method will take a domestic shipment request in the body and on successful response, it will return the shipment numbers and item details.
        :return:
        """
        pass


    def put_shipment(self):
        """

        Summary
        =======

        updateShipment

        Description
        -----------

        Update a shipment. Send a shipment request in body. On successful response, it will return shipment number and warnings. Service related information can not be updated, and if passed as part of request, it will be ignored.

        :return:
        """
        pass


    def delete_shipment(self):
        """

        Description

        Delete a shipment. Send a shipment identifier in Url. Successful response will be 200 with no content.

        :return:
        """
        pass


    def put_shipment_label(self):
        """

        Description
        -----------
        This method returns a label for the shipment identifier passed in the url.

        :return:
        """
        pass

    def post_manifest(self):
        """

        Description
        -----------
        This method creates a shipping manifest

        :return:
        """
        pass

    def put_manifest(self):
        """

        Description
        -----------

        This method return a manifest label for a previously manifested shipment.

        :return:
        """
        pass



if __name__ == '__main__':
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    USERNAME = ''
    PASSWORD_HASHED = ''

    shipping_api = ShippingApi(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD_HASHED)
    token = shipping_api.get_token()

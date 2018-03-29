import datetime

class RoyalMailBody():
    def __init__(self, shipment_type):
        self.receipient = None
        self.address = None
        self.service = None
        self.shipping_date = None
        self._check_ship_type(shipment_type)
        self.sender_reference = None
        self.department_reference = None
        self.customer_reference = None
        self.items = []
        self.item_count = len(self.items)
        self.safe_place = None

    def return_domestic_body(self):
        """
        build domestic body from items
        :return:
        """

        domestic_body = {
            'shipmentType': self.shipment_type,
            'service': self.service,
            'shippingDate': self.shipping_date,
            'items': self.items,
            'recipientContact': self.receipient,
            'recipientAddress': self.address,
            'senderReference': self.sender_reference,
            'departmentReference': self.department_reference,
            'customerReference': self.customer_reference,
            'safePlace': self.safe_place
        }

        return domestic_body

    def return_domestic_update_boy(self):
        """
        build domestic body from items
        :return:
        """

        domestic_body = {
            'service': self.service,
            'shippingDate': self.shipping_date,
            'recipientContact': self.receipient,
            'recipientAddress': self.address,
            'senderReference': self.sender_reference,
            'departmentReference': self.department_reference,
            'customerReference': self.customer_reference,
            'safePlace': self.safe_place
        }

        return domestic_body

    def remove_none_values(self, iterable):
        """
        take out values of None by removing the key
        :param iterable:
        :return:
        """

        new_dict = {k: v for k, v in iterable.items() if v is not None}

        return new_dict

    def _check_ship_type(self, shipment_type):
        if shipment_type.lower() != 'delivery':
            # TODO: Find out the other options here!
            raise Exception('Sorry, only delivery supported at the moment')
        else:
            self.shipment_type = shipment_type.lower()


    def add_ship_date(self, date_obj=None):
        """
        take a datetime object and format it to royal mails Y-m-d format
        :param date_obj:
        :return:
        """
        if date_obj is None:
            date_obj = datetime.datetime.today()
        self.shipping_date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')

    def add_service(self, format=None, occurrence=None, offering=None, _type=None, signature=None, enhancements=None):
        if not isinstance(enhancements, list):
            enhancements = [enhancements]

        service = {
            "format": format,
            "occurrence": occurrence,
            "offering": offering,
            "type": _type,
            "signature": signature,
            "enhancements": enhancements
            }

        self.service = service


    def add_receipient_contact(self, name, email, complementary_name=None, telephone=None):
        receipient = {
            "name": name,
            "complementaryName": complementary_name,
            "telephoneNumber": telephone,
            "email": email
        }

        # receipient = self.remove_none_values(receipient)
        self.receipient = receipient


    def add_items(self, number, weight, unit_of_measure):
        items = [{
            "count": number ,
            "weight": {
                "unitOfMeasure": unit_of_measure,
                "value": weight
            },
        }]

        self.items = items


    def add_receipient_address(self, address_line1, post_town, county, postcode, country, building_name=None, building_number=None,
                           address_line2=None, address_line3=None):
        address = {
            "buildingName": building_name,
            "buildingNumber": building_number,
            "addressLine1": address_line1,
            "addressLine2": address_line2,
            "addressLine3": address_line3,
            "postTown": post_town,
            "county": county,
            "postCode": postcode,
            "country": country
        }

        # address = self.remove_none_values(address)
        self.address = address




if __name__ == '__main__':
    from royal_mail_rest_api.get_credentials import return_credentials
    creds = return_credentials()

    body = RoyalMailBody('Delivery')


    body.add_ship_date(None)
    body.add_service('P', 1, 'TPN', 'T', True,  ['14'])
    body.customer_reference = 'D123456'
    body.department_reference = 'Q123456'
    body.sender_reference = 'A123456'
    body.add_items(1, 100, 'g')
    body.add_receipient_contact('Joe Bloggs', 'joe.bloggs@royalmail.com', None, '07970810000')
    body.add_receipient_address('Broadgate Circle', 'London', None, 'EC1A 1BB', country='GB', building_number='1', address_line2='Add line 2', address_line3='Add line 3', building_name='My building')


    my_rm_body = body.return_domestic_body()
    import json

    print(json.dumps(my_rm_body))

    print(my_rm_body)

    from royal_mail_rest_api.shipping import ShippingApi
    CLIENT_ID = creds['royal_mail']['CLIENT_ID']
    CLIENT_SECRET = creds['royal_mail']['CLIENT_SECRET']
    USERNAME = creds['royal_mail']['USERNAME']
    PASSWORD_HASHED = creds['royal_mail']['PASSWORD_HASHED']
    my_shipping = ShippingApi(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD_HASHED)
    my_shipping.get_token()


    post_shipping = my_shipping.post_domestic(my_rm_body)
    tracking_ref= post_shipping['completedShipments'][0]['shipmentItems'][0]['shipmentNumber']
    label = my_shipping.put_shipment_label(tracking_ref)

    # new_data = {
    #     'recipientContact': {
    #         'name': 'Alex Hellier'
    #     }
    # }

    body.add_receipient_contact('Alex Hellier', 'alex@me.com', 'Alex S Hellier', '123455')
    new_data = body.return_domestic_update_boy()
    change_name = my_shipping.put_shipment(tracking_ref, new_data)
    new_label = my_shipping.put_shipment_label(tracking_ref)

    print(tracking_ref)
    # delete_shipping = my_shipping.delete_shipment(post_shipping['completedShipments'][0]['shipmentItems'][0]['shipmentNumber'])
    # print(delete_shipping)
    # manifest_info = {'yourReference': '123'}
    # manifest_data = my_shipping.post_manifest(manifest_info)
    # print(manifest_data)
    # manifest_label = my_shipping.put_manifest(manifest_batch_number=5)
    # print(manifest_label)

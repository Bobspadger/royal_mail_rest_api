import datetime

class RoyalMailBody():
    def __init__(self):
        self.items = [{
            "offlineShipment": [
                {
                    "number": "1",
                    "itemID": "221228314918912",
                    "status": "new"
                }
            ],
            "count": 1,
            "weight": {
                "unitOfMeasure": "g",
                "value": 100
            }
        }
    ]
        self.receipient = None
        self.address = None
        self.service = None
        self.shipping_date = None
        self.shipment_type = None
        self.sender_reference = None
        self.department_reference = None
        self.customer_reference = None
        self.item_count = len(self.items)


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
            'receipientContact': self.receipient,
            'receipientAddress': self.address,
            'senderReference': self.sender_reference,
            'departmentReference': self.department_reference,
            'customerReference': self.customer_reference,
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

    def add_ship_type(self, shipment_type):
        if shipment_type != 'delivery':
            # TODO: Find out the other options here!
            raise Exception('Sorry, only delivery supported at the moment')
        self.shipment_type = shipment_type


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

        receipient = self.remove_none_values(receipient)
        self.receipient = receipient


    def add_items(self, number, item_id, status):
        item = {
            "number": number ,
            "itemID": item_id,
            "status": status
        }

        self.items.append(item)


    def add_receipient_address(self, address_line1, post_town, county, postcode, building_name=None, building_number=None,
                           address_line2=None, address_line3=None):
        address = {
            "buildingName": building_name,
            "buildingNumber": building_number,
            "addressLine1": address_line1,
            "addressLine2": address_line2,
            "addressLine3": address_line3,
            "postTown": post_town,
            "county": county,
            "postCode": postcode
        }

        address = self.remove_none_values(address)
        self.address = address




if __name__ == '__main__':
    body = RoyalMailBody()
    body.add_ship_type('delivery')
    # body.add_items(1, '123', 'ok')
    # body.add_items(2, '134', 'ok')
    body.add_ship_date(None)
    body.add_service('P', None, 'TPN', 'T', None,  ['12', '13', '14'])
    body.customer_reference = 'D123456'
    body.department_reference = 'Q123456'
    body.sender_reference = 'A123456'
    body.add_receipient_contact('Alex Hellier', 'alex@absolutemusic.co.uk', None, '07970810000')
    body.add_receipient_address('855 Ringwood Road', 'Bournemouth', 'Dorset', 'BH10 6JJ', building_number='5')


    my_rm_body = body.return_domestic_body()
    import json

    print(json.dumps(my_rm_body))

    print(my_rm_body)

    from royal_mail_rest_api.shipping import ShippingApi
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    USERNAME = ''
    PASSWORD_HASHED = ''
    my_shipping = ShippingApi(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD_HASHED)
    my_shipping.get_token()
    post_shipping = my_shipping.post_domestic(my_rm_body)

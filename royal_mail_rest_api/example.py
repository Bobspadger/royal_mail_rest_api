import json
from royal_mail_rest_api.tools import RoyalMailBody
from royal_mail_rest_api.shipping import ShippingApi
from royal_mail_rest_api.get_credentials import return_credentials

if __name__ == '__main__':

    creds = return_credentials()

    body = RoyalMailBody('Delivery')
    body.add_ship_date(None)
    body.add_service('P', 1, 'TPN', 'T', True,  ['14'])
    body.customer_reference = 'D123456'
    body.department_reference = 'Q123456'
    body.sender_reference = 'A123456'
    body.add_items(1, 100, 'g')
    body.add_receipient_contact('Joe Bloggs', 'joe.bloggs@royalmail.com', None, '07970810000')
    body.add_receipient_address('Broadgate Circle', 'London', None, 'EC1A 1BB', country='GB', building_number='1',
                                address_line2='Add line 2', address_line3='Add line 3', building_name='My building')

    my_rm_body = body.return_domestic_body()


    print(json.dumps(my_rm_body))

    print(my_rm_body)


    CLIENT_ID = creds['royal_mail']['CLIENT_ID']
    CLIENT_SECRET = creds['royal_mail']['CLIENT_SECRET']
    USERNAME = creds['royal_mail']['USERNAME']
    PASSWORD_HASHED = creds['royal_mail']['PASSWORD_HASHED']
    my_shipping = ShippingApi(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD_HASHED)
    my_shipping.get_token()

    post_shipping = my_shipping.post_domestic(my_rm_body)
    tracking_ref = post_shipping['completedShipments'][0]['shipmentItems'][0]['shipmentNumber']
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

    # print(tracking_ref)
    # delete_shipping = my_shipping.delete_shipment(tracking_ref)

    # print(delete_shipping)
    # manifest_info = {'yourReference': '123'}
    # manifest_data = my_shipping.post_manifest(manifest_info)
    # print(manifest_data)
    # manifest_label = my_shipping.put_manifest(manifest_batch_number=5)
    # print(manifest_label)

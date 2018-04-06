#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `royal_mail_rest_api` package."""
import pytest
from royal_mail_rest_api.tools import RoyalMailBody

def test_add_services():
    body = RoyalMailBody('delivery')
    with pytest.raises(ValueError):
        assert body.add_service_format()
        assert body.add_service_type()
        assert body.add_service_offering()
    with pytest.raises(KeyError):
        assert body.add_service_format('does not exist')
        assert body.add_service_type('does not exist')
        assert body.add_service_offering('does not exist')

    body.add_service_format('inland_parcel')
    body.add_service_type('royal_mail_24')
    body.add_service_offering('royal_mail_tracked_24')

    assert body.service_format == 'P'
    assert body.service_type == '1'
    assert body.service_offering =='TPN'

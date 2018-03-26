#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `royal_mail_rest_api` package."""

import pytest

from click.testing import CliRunner

from royal_mail_rest_api import *
from royal_mail_rest_api import cli
from royal_mail_rest_api.errors import *


@pytest.fixture
def http_response(status_code):
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    class response_mock():
        status_code = status_code

    return response_mock()

def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'royal_mail_rest_api.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_500_error(http_resonse):
    """
    Test a response.status_code 500 rasies GeneralError
    :param http_resonse:
    :return:
    """
    with pytest.raises(NotAuthorised):
        RoyalMailBaseClass._test_error(http_response(500))

def test_401_error(http_response):
    """
    test 401 raises not authed
    :param http_response:
    :return:
    """
    with pytest.raises(NotAuthorised):
        RoyalMailBaseClass._test_error(http_response(401))


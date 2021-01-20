""" Utils to assist UKFast Billing testing. """
import os
import pytest

from UKFastAPI.Billing.billing import Billing
import UKFastAPI.Billing.config as config
from UKFastAPI.config import UKF_API_KEY

# pylint:disable=missing-function-docstring


@pytest.fixture
def billing(request):
    return request.param()


def get_billing():
    api_key = os.getenv(UKF_API_KEY)
    billing_key = api_key if api_key else os.getenv(config.BILLING_AUTH)
    return Billing(billing_key)


def get_valid_card_details():
    return {
        'name': 'John Doe',
        'address': '123 Fake Street',
        'postcode': 'M123Q',
        'card_number': '4012888888881881',
        'card_type': 'visa',
        'valid_from': '01/20',
        'expiry': '01/30'
    }


@pytest.fixture
def clear_billing_cards():
    for card in get_billing().cards.list(all=True):
        if not card.primary_card:
            card.delete()

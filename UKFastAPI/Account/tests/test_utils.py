""" Utils to assist SafeDNS testing. """
import os
import pytest

from UKFastAPI.Account.account import Account
import UKFastAPI.Account.config as config
from UKFastAPI.config import UKF_API_KEY

# pylint:disable=missing-function-docstring


@pytest.fixture
def account(request):
    return request.param()


def get_account():
    api_key = os.getenv(UKF_API_KEY)
    account_key = api_key if api_key else os.getenv(config.ACCOUNT_AUTH)
    return Account(account_key)

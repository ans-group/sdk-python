""" Utils to assist SafeDNS testing. """
import os
import string
import random
import pytest

from UKFastAPI.SafeDNS.safedns import SafeDns, config
from UKFastAPI.config import UKF_API_KEY

# pylint:disable=missing-function-docstring


@pytest.fixture
def parent(request):
    return request.param()


@pytest.fixture
def safedns(request):
    return request.param()


@pytest.fixture
def clear_safedns():
    """ Clean the SafeDNS environment. """
    delete_all_zones()
    delete_all_templates()


def generate_zone_name(limit=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(limit)) + '.com'


def get_safedns():
    api_key = os.getenv(UKF_API_KEY)
    safedns_key = api_key if api_key else os.getenv(config.SAFEDNS_AUTH)
    return SafeDns(safedns_key)


def delete_all_zones():
    safedns_ = get_safedns()
    zones = safedns_.zones.list()
    for zone in zones:
        zone.delete()


def delete_all_templates():
    safedns_ = get_safedns()
    templates = safedns_.templates.list()
    for template in templates:
        template.delete()


def create_zone():
    return get_safedns().zones.create(name=generate_zone_name())


def create_template():
    return get_safedns().templates.create(name=generate_zone_name(), default=False)

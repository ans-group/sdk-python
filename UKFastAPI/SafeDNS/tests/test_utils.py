""" Utils to assist SafeDNS testing. """
import os
import random
import string

import pytest
from UKFastAPI.config import UKF_API_KEY
from UKFastAPI.SafeDNS.safedns import SafeDns, config
from UKFastAPI.SafeDNS.tests import config as testconfig
from UKFastAPI.utils import generate_vcr_decorator

# pylint:disable=missing-function-docstring

vcr_decorator = generate_vcr_decorator('UKFastAPI/SafeDNS/tests/cassettes')

generated_zone_names = [
    'okbrqvvbeq.com',
    'ysricezcuj.com',
    'wkuddzatav.com',
    'offmhoiwfs.com',
    'gkfulmmers.com',
    'yasrywmquh.com',
    'pbdlkpidjs.com',
    'jxunfsihnv.com',
    'xzghgrrltj.com',
    'vytmqjezzk.com',
    'fbjhhgvlkf.com',
    'apdodmwwjv.com',
    'wqmnhrxzkn.com',
    'vtobahpngu.com',
    'efbtuhosim.com',
    'xgupnmtvyv.com',
    'axbeklzgys.com',
    'wblhkuljrl.com',
    'zeawfuvldo.com',
    'gllacggkbe.com',
]


@pytest.fixture
@vcr_decorator
def parent(request):
    return request.param()


@pytest.fixture
@vcr_decorator
def safedns(request):
    return request.param()


@pytest.fixture
def clear_safedns():
    """ Clean the SafeDNS environment. """
    # Only uncommen when creating cassettes.
    # delete_all_zones()
    # delete_all_templates()


def generate_zone_name(limit=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(limit)) + '.com'


def get_zone_names(index=0):
    return generated_zone_names[index]


@vcr_decorator
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
    return get_safedns().zones.create(name=get_zone_names())


def create_template():
    return get_safedns().templates.create(name=get_zone_names(), default=False)


def create_simple_record(obj, name=None):
    """ Helper function to create Records. """
    return obj.records.create(
        name=name if name else testconfig.TEST_RECORD_NAME + obj.name,
        type=testconfig.TEST_RECORD_TYPE,
        content=name if name else testconfig.TEST_RECORD_CONTENT + obj.name,
        ttl=testconfig.TEST_RECORD_TTL,
        priority=testconfig.TEST_RECORD_PRIORITY
    )

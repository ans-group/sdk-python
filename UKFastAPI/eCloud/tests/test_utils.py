""" Utils to assist UKFast eCloud testing. """
import datetime
import os
import random
import string
import time
import functools

from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

import pytest

import UKFastAPI.eCloud.config as config
import UKFastAPI.eCloud.tests.config as testconfig
from UKFastAPI.config import UKF_API_KEY
from UKFastAPI.eCloud.ecloud import eCloud
from UKFastAPI import exceptions
# pylint:disable=missing-function-docstring


@pytest.fixture
def parent(request):
    return request.param()


@pytest.fixture
def ecloud(request):
    return request.param()


@pytest.fixture
def clear():
    clear_ecloud()


def get_ecloud_v1():
    return get_ecloud(version=1)


def get_ecloud(version=2):
    api_key = os.getenv(UKF_API_KEY)
    key = api_key if api_key else os.getenv(config.ECLOUD_AUTH)
    return eCloud(key, version=version)


def create_vpc():
    vpc = get_ecloud().vpcs.create(region_id=testconfig.TEST_REGION_ID)
    return vpc


def create_router():
    return get_ecloud().routers.create(
        name=testconfig.TEST_ROUTER_NAME,
        vpc_id=create_vpc().id,
    )


def create_network():
    ecloud_ = get_ecloud()
    router = create_router()
    network = ecloud_.networks.create(
        name=testconfig.TEST_NETWORK_NAME,
        router_id=router.id,
        subnet=testconfig.TEST_SUBNET)
    return wait_until_complete(functools.partial(ecloud_.networks.get, network.id))


def create_instance():
    vpc = create_vpc()
    network = create_network()

    appliance = get_ecloud().appliances.get(testconfig.TEST_APPLIANCE_ID)
    instance = get_ecloud().instances.create(
        vpc_id=vpc.id,
        appliance_id=appliance.id,
        network_id=network.id,
        vcpu_cores=testconfig.TEST_CPU,
        ram_capacity=testconfig.TEST_RAM)

    return instance


def create_dhcp():
    ecloud_ = get_ecloud()
    dhcp = ecloud_.dhcps.create(vpc_id=create_vpc().id)
    return wait_until_complete(functools.partial(ecloud_.dhcps.get, dhcp.id))


def create_floatingip():
    return get_ecloud().floating_ips.create(vpc_id=create_vpc().id)


def create_firewall_policy():
    return get_ecloud().firewall_policies.create(
        router_id=create_router().id,
        sequence=testconfig.TEST_POLICY_SEQUENCE)


def create_firewall_rule():
    return get_ecloud().firewall_rules.create(
        sequence=1,
        firewall_policy_id=create_firewall_policy().id,
        source=testconfig.TEST_RULE_SOURCE,
        destination=testconfig.TEST_RULE_DEST,
        action=testconfig.TEST_RULE_ACTION,
        direction=testconfig.TEST_RULE_DIRECTION,
        enabled=True)


def create_firewall_rule_port():
    return get_ecloud().firewall_rule_ports.create(
        firewall_rule_id=create_firewall_rule().id,
        protocol=testconfig.TEST_RULE_PROTOCOL)


def clear_ecloud():
    fail_limit = 5
    fail_sleep = 5

    ecloud_ = get_ecloud()
    funcs = [
        functools.partial(ecloud_.instances.list, all=True),
        functools.partial(ecloud_.networks.list, all=True),
        functools.partial(ecloud_.firewall_rules.list, all=True),
        functools.partial(ecloud_.firewall_policies.list, all=True),
        functools.partial(ecloud_.routers.list, all=True),
        functools.partial(ecloud_.vpcs.list, all=True),
    ]

    for list_func in funcs:
        fail_count = 0

        while True:
            error_flag = False
            for obj in list_func():
                # ================DEBUG================
                # Just here whilst eCloud fixes the VMs that are stuck and can't be deleted.
                if datetime.datetime.fromisoformat(
                        obj.created_at).replace(
                        tzinfo=None) + datetime.timedelta(
                        days=7) < datetime.datetime.now():
                    print('Skipping stuck object {}'.format(obj.id))
                    continue
                # ================DEBUG================
                try:
                    obj.delete()
                except exceptions.UKFastAPIException as exception:
                    print('Failed to delete {} created at {} due to "{}"'.format(
                        obj.id, obj.created_at, exception))
                    error_flag = True

            if error_flag:
                fail_count += 1
                time.sleep(fail_sleep)

            if fail_count >= fail_limit or not error_flag:
                break

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for instance in get_ecloud().instances.list(all=True):
    #             instance.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for network in get_ecloud().networks.list(all=True):
    #             network.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for firewall_rule in get_ecloud().firewall_rules.list(all=True):
    #             firewall_rule.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for firewall_policy in get_ecloud().firewall_policies.list(all=True):
    #             firewall_policy.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for router in get_ecloud().routers.list(all=True):
    #             router.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)

    # fail_count = 0
    # while fail_count > fail_limit:
    #     try:
    #         for vpc in get_ecloud().vpcs.list(all=True):
    #             vpc.delete()
    #     except exceptions.UKFastAPIException:
    #         time.sleep(fail_sleep)


def generate_string(limit=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(limit))


def get_region(index=0):
    return get_ecloud().regions.list()[index]


def wait_until_complete(func):
    while func().sync.lower() != 'complete':
        time.sleep(3)
    return func()


EMOJI_RANGES_UNICODE = {
    6: [
        ('\U0001F300', '\U0001F320'),
        ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'),
        ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'),
        ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'),
        ('\U0001F400', '\U0001F43E'),
        ('\U0001F440', ),
        ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'),
        ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'),
        ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')
    ],
    7: [
        ('\U0001F300', '\U0001F32C'),
        ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'),
        ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'),
        ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ],
    8: [
        ('\U0001F300', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ]
}


def random_emoji(unicode_version=6):
    if EMOJI_RANGES_UNICODE.get(unicode_version):
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    point = randrange(weight_distr[-1])

    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    point_in_range = point
    if emoji_range_idx != 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji, '(No name found for this codepoint)').capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return (emoji, emoji_codepoint, emoji_name)

# ================== V1 Utils ==================


@pytest.fixture
def clear_vms():
    clear_all_vms()


def clear_all_vms():
    for vm in get_ecloud(version=1).vms.list(all=True):
        try:
            vm.delete()
        except exceptions.UKFastAPIException:
            pass

    start_time = datetime.datetime.now()
    buffer = datetime.timedelta(seconds=30)
    while get_ecloud(version=1).vms.list() and start_time + buffer > datetime.datetime.now():
        time.sleep(1)


def generate_vm_name(limit=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(limit))


def create_simple_vm():
    return get_ecloud(version=1).vms.create(
        name=generate_vm_name(),
        environment=testconfig.TEST_ENVIRONMENT,
        appliance_id=testconfig.TEST_APPLIANCE_ID,
        cpu=testconfig.TEST_CPU,
        ram=testconfig.TEST_RAM_V1,
        hdd=testconfig.TEST_HDD,
        pod_id=testconfig.TEST_POD_ID
    )


def wait_for_vm(vm, timeout=testconfig.BUFFER_TIME, status='Complete'):
    start_time = datetime.datetime.now()
    buffer_time = datetime.timedelta(seconds=timeout)
    while get_ecloud(version=1).vms.get(vm.id).status != status:
        if start_time + buffer_time < datetime.datetime.now():
            raise Exception(
                'VM was not ready within the given time frame of {} seconds.'.format(timeout))
        time.sleep(3)


def wait_for_vm_deletion(vm, timeout=testconfig.BUFFER_TIME):
    start_time = datetime.datetime.now()
    buffer_time = datetime.timedelta(seconds=timeout)
    while start_time + buffer_time > datetime.datetime.now():
        try:
            get_ecloud(version=1).vms.get(vm.id)
        except exceptions.UKFastAPIException:
            return
        time.sleep(3)
    raise Exception(
        'VM was not deleted within the given time frame of {} seconds.'.format(timeout))

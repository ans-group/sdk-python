""" Tests for the eCloud Firewall Policies implementation. """
import sys
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_router, generate_string, get_ecloud, clear, clear_ecloud, ecloud,
    wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestFirewallPolicies():
    """ Test class for the eCloud Firewall Policies module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_firewall_policy_create(self, ecloud):
        """ Tests Firewall Policy creation using the minimum required values. """
        assert create_firewall_policy()

    def test_firewall_policy_create_optionals(self, ecloud):
        """ Tests Firewall Policy creation using all optional values. """
        assert ecloud.firewall_policies.create(
            router_id=create_router().id,
            sequence=config.TEST_POLICY_SEQUENCE,
            name=generate_string(50))

    def test_firewall_policy_create_long_name(self, ecloud):
        """ Tests Firewall Policy creation using all optional values. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_policies.create(
                router_id=create_router().id,
                sequence=config.TEST_POLICY_SEQUENCE,
                name=generate_string(1000))

    def test_firewall_policy_create_invalid_router(self, ecloud):
        """ Tests Firewall Policy creation using an invalid router id. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_policies.create(
                router_id='rtr-1234567z', sequence=config.TEST_POLICY_SEQUENCE)

    def test_firewall_policy_create_max_sequence(self, ecloud):
        """ Tests Firewall Policy creation using a large squence value. """
        assert ecloud.firewall_policies.create(router_id=create_router().id, sequence=sys.maxsize)

    def test_firewall_policy_get(self, ecloud):
        """ Tests Firewall Policy retrieval. """
        policy = create_firewall_policy()
        assert ecloud.firewall_policies.get(policy.id)

    def test_firewall_policy_update(self, ecloud):
        """ Tests Firewall Policy updated. """
        policy = create_firewall_policy()

        new_name = 'test policy'
        new_sequence = 2

        policy.name = new_name
        policy.sequence = new_sequence

        policy.save()
        policy = ecloud.firewall_policies.get(policy.id)

        assert policy.name == new_name
        assert policy.sequence == new_sequence

    def test_firewall_policy_update_long_name(self, ecloud):
        """ Tests Firewall Policy updated. """
        policy = create_firewall_policy()

        new_name = 'test policy'
        new_sequence = 2

        policy.name = new_name
        policy.sequence = new_sequence

        policy.save()
        policy = ecloud.firewall_policies.get(policy.id)

        assert policy.name == new_name
        assert policy.sequence == new_sequence

    def test_firewall_policy_delete(self, ecloud):
        """ Tests Firewall Policy deletion. """
        policy = create_firewall_policy()
        policy.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_policies.get(policy.id)

    def test_firewall_policy_list(self, ecloud):
        """ Tests Firewall Policy listing. """
        limit = 5
        for _ in range(limit):
            create_firewall_policy()
        assert len(ecloud.firewall_policies.list()) == limit

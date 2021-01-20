""" Tests for the eCloud Firewall Rules implementation. """
import sys
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_router, generate_string, get_ecloud, clear,
    clear_ecloud, ecloud, wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestFirewallRules():
    """ Test class for the eCloud Firewall Rules module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_firewall_rule_create(self, ecloud):
        """ Tests Firewall Rule creation using the minimum required values. """
        assert ecloud.firewall_rules.create(
            sequence=1,
            firewall_policy_id=create_firewall_policy().id,
            source=config.TEST_RULE_SOURCE,
            destination=config.TEST_RULE_DEST,
            action=config.TEST_RULE_ACTION,
            direction=config.TEST_RULE_DIRECTION,
            enabled=True)

    def test_firewall_rule_create_max_sequence(self, ecloud):
        """ Tests Firewall Rule creation using the minimum required values. """
        assert ecloud.firewall_rules.create(
            sequence=sys.maxsize,
            firewall_policy_id=create_firewall_policy().id,
            source=config.TEST_RULE_SOURCE,
            destination=config.TEST_RULE_DEST,
            action=config.TEST_RULE_ACTION,
            direction=config.TEST_RULE_DIRECTION,
            enabled=True)

    def test_firewall_rule_create_invalid_policy(self, ecloud):
        """ Tests Firewall Rule creation with an invalid policy id. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rules.create(
                sequence=1,
                firewall_policy_id='pol-1234567z',
                source=config.TEST_RULE_SOURCE,
                destination=config.TEST_RULE_DEST,
                action=config.TEST_RULE_ACTION,
                direction=config.TEST_RULE_DIRECTION,
                enabled=True)

    def test_firewall_rule_create_invalid_source(self, ecloud):
        """ Tests Firewall Rule creation with an invalid source. """
        assert ecloud.firewall_rules.create(
            sequence=1,
            firewall_policy_id=create_firewall_policy().id,
            source='',
            destination=config.TEST_RULE_DEST,
            action=config.TEST_RULE_ACTION,
            direction=config.TEST_RULE_DIRECTION,
            enabled=True)

    def test_firewall_rule_create_invalid_destination(self, ecloud):
        """ Tests Firewall Rule creation with an invalid destination. """
        assert ecloud.firewall_rules.create(
            sequence=1,
            firewall_policy_id=create_firewall_policy().id,
            source='',
            destination='',
            action=config.TEST_RULE_ACTION,
            direction=config.TEST_RULE_DIRECTION,
            enabled=True)
        print()

    def test_firewall_rule_create_invalid_action(self, ecloud):
        """ Tests Firewall Rule creation with an invalid action. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rules.create(
                sequence=1,
                firewall_policy_id=create_firewall_policy().id,
                source=config.TEST_RULE_SOURCE,
                destination=config.TEST_RULE_DEST,
                action='',
                direction=config.TEST_RULE_DIRECTION,
                enabled=True)

    def test_firewall_rule_create_invalid_direction(self, ecloud):
        """ Tests Firewall Rule creation with an invalid direction. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rules.create(
                sequence=1,
                firewall_policy_id=create_firewall_policy().id,
                source=config.TEST_RULE_SOURCE,
                destination=config.TEST_RULE_DEST,
                action=config.TEST_RULE_ACTION,
                direction='',
                enabled=True)

    def test_firewall_rule_create_optionals(self, ecloud):
        """ Tests Firewall Rule creation using all optional values. """
        assert ecloud.firewall_rules.create(
            sequence=1,
            firewall_policy_id=create_firewall_policy().id,
            source=config.TEST_RULE_SOURCE,
            destination=config.TEST_RULE_DEST,
            action=config.TEST_RULE_ACTION,
            direction=config.TEST_RULE_DIRECTION,
            enabled=True,
            ports=[{"protocol": "TCP", "source": "443", "destination": "443"}])

    def test_firewall_rule_get(self, ecloud):
        """ Tests Firewall Rule retrieval. """
        assert ecloud.firewall_rules.get(create_firewall_rule().id)

    def test_firewall_rule_update(self, ecloud):
        """ Tests Firewall Rule updates. """
        pytest.skip('https://gitlab.devops.ukfast.co.uk/ukfast/api.ukfast/ecloud/-/issues/595')
        rule = create_firewall_rule()

        new_name = 'test name'
        new_sequence = 2
        new_firewall_policy = create_firewall_policy().id
        new_source = '5.5.5.5'
        new_destination = '6.6.6.6'
        new_action = 'DROP'
        new_direction = 'OUT'
        new_ports = [{"protocol": "TCP", "source": "443", "destination": "443"}]

        rule.name = new_name
        rule.sequence = new_sequence
        rule.firewall_policy_id = new_firewall_policy
        rule.source = new_source
        rule.destination = new_destination
        rule.action = new_action
        rule.direction = new_direction
        rule.ports = new_ports

        rule.save()
        rule = ecloud.firewall_rules.get(rule.id)

        assert rule.name == new_name
        assert rule.sequence == new_sequence
        assert rule.firewall_policy_id == new_firewall_policy
        assert rule.source == new_source
        assert rule.destination == new_destination
        assert rule.action == new_action
        assert rule.direction == new_direction
        assert rule.ports == new_ports

    def test_firewall_rule_delete(self, ecloud):
        """ Tests Firewall Rule retrieval. """
        rule = create_firewall_rule()
        rule.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rules.get(rule.id)

    def test_firewall_rule_list(self, ecloud):
        """ Tests Firewall Rule listing. """
        limit = 5
        for _ in range(limit):
            create_firewall_rule()
        assert len(ecloud.firewall_rules.list()) == limit

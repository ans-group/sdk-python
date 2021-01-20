""" Tests for the eCloud Firewall Rule Ports implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_firewall_rule_port, create_router,
    generate_string, get_ecloud, clear, clear_ecloud, ecloud, wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestFirewallRulePorts():
    """ Test class for the eCloud Firewall Rule Ports module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_firewall_rule_port_create(self, ecloud):
        """ Tests Firewall Rule Port creation using the minimum required values. """
        assert ecloud.firewall_rule_ports.create(
            firewall_rule_id=create_firewall_rule().id,
            protocol='TCP')

    def test_firewall_rule_port_create_optionals(self, ecloud):
        """ Tests Firewall Rule Port creation using all optional values. """
        assert ecloud.firewall_rule_ports.create(
            firewall_rule_id=create_firewall_rule().id,
            protocol='TCP',
            source='1.1.1.1',
            destination='2.2.2.2')

    def test_firewall_rule_port_create_invalid_rule(self, ecloud):
        """ Tests Firewall Rule Port creation using all optional values. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rule_ports.create(
                firewall_rule_id='fwp-1234567z',
                protocol='TCP',
                source='1.1.1.1',
                destination='2.2.2.2')

    def test_firewall_rule_port_create_invalid_protocol(self, ecloud):
        """ Tests Firewall Rule Port creation using all optional values. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rule_ports.create(
                firewall_rule_id=create_firewall_rule().id,
                protocol='',
                source='1.1.1.1',
                destination='2.2.2.2')

    def test_firewall_rule_port_create_invalid_source(self, ecloud):
        """ Tests Firewall Rule Port creation using all optional values. """
        pytest.skip('https://gitlab.devops.ukfast.co.uk/ukfast/api.ukfast/ecloud/-/issues/594')
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rule_ports.create(
                firewall_rule_id=create_firewall_rule().id,
                protocol='TCP',
                source='',
                destination='')

    def test_firewall_rule_port_get(self, ecloud):
        """ Tests Firewall Rule Port retrieval. """
        assert ecloud.firewall_rule_ports.get(create_firewall_rule_port().id)

    def test_firewall_rule_port_get_invalid(self, ecloud):
        """ Tests Firewall Rule Port retrieval with invalid id. """
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rule_ports.get('frp-1234567z')

    def test_firewall_rule_port_update(self, ecloud):
        """ Tests Firewall Rule Port updating. """
        port = create_firewall_rule_port()
        new_firewall_rule_id = create_firewall_rule().id
        new_protocol = 'UDP'
        new_source = '5.5.5.5'
        new_dest = '6.6.6.6'

        port.firewall_rule_id = new_firewall_rule_id
        port.protocol = new_protocol
        port.source = new_source
        port.destination = new_dest

        port.save()
        port = ecloud.firewall_rule_ports.get(port.id)

        assert port.firewall_rule_id == new_firewall_rule_id
        assert port.protocol == new_protocol
        assert port.source == new_source
        assert port.destination == new_dest

    def test_firewall_rule_port_delete(self, ecloud):
        """ Tests Firewall Rule Port delete. """
        port = create_firewall_rule_port()
        port.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.firewall_rule_ports.get(port.id)

    def test_firewall_rule_port_list(self, ecloud):
        """ Tests Firewall Rule Port listing. """
        limit = 5
        for _ in range(limit):
            create_firewall_rule_port()
        assert len(ecloud.firewall_rule_ports.list()) == limit

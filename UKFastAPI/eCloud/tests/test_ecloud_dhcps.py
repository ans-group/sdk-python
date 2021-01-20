""" Tests for the eCloud Dhcps implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (clear, clear_ecloud,
                                               create_dhcp, create_instance,
                                               create_network, create_router,
                                               create_vpc, ecloud,
                                               generate_string, get_ecloud)
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestDhcps():
    """ Test class for the eCloud Dhcps module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_dhcp_create(self, ecloud):
        """ Tests Dhcp creation using the minimum required values. """
        assert create_dhcp()

    def test_dhcp_create_invalid_vcp(self, ecloud):
        """ Tests Dhcp creation using an invalid vcp id. """
        with pytest.raises(UKFastAPIException):
            ecloud.dhcps.create(vpc_id='vcp-1234567z')

    def test_dhcp_get(self, ecloud):
        """ Tests Dhcp retrieval. """
        assert ecloud.dhcps.get(create_dhcp().id)

    def test_dhcp_get_invalid_id(self, ecloud):
        """ Tests Dhcp retrieval. """
        with pytest.raises(UKFastAPIException):
            ecloud.dhcps.get('dhcp-1234567z')

    def test_dhcp_update(self, ecloud):
        """ Tests Dhcp update. """
        dhcp = create_dhcp()

        new_vpc_id = create_vpc().id
        dhcp.vpc_id = new_vpc_id
        dhcp.save()

        dhcp = ecloud.dhcps.get(dhcp.id)
        assert dhcp.vpc_id == new_vpc_id

    def test_dhcp_update_invalid_id(self, ecloud):
        """ Tests Dhcp update with an invalid vpc id. """
        dhcp = create_dhcp()

        dhcp.vpc_id = 'vpc-1234567z'
        with pytest.raises(UKFastAPIException):
            dhcp.save()

    def test_dhcp_delete(self, ecloud):
        """ Tests Dhcp delete. """
        dhcp = create_dhcp()
        dhcp.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.dhcps.get(dhcp.id)

    def test_dhcp_list(self, ecloud):
        """ Tests Dhcp listing. """
        limit = 5
        for _ in range(limit):
            create_dhcp()
        assert len(ecloud.dhcps.list()) == limit

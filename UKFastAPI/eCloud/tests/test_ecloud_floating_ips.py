""" Tests for the eCloud Floating IPs implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (clear, clear_ecloud,
                                               create_floatingip, create_vpc,
                                               ecloud, get_ecloud,
                                               wait_until_complete)
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestFloatingIps():
    """ Test class for the eCloud Floating IPs module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_floatingip_create(self, ecloud):
        """ Tests Floating IP creation using the minimum required values. """
        assert create_floatingip()

    def test_floatingip_create_invalid_vpc(self, ecloud):
        """ Tests Floating IP creation using an invalid vpc id. """
        with pytest.raises(UKFastAPIException):
            ecloud.floating_ips.create(vpc_id='vpc-1234567z')

    def test_floatingip_get(self, ecloud):
        """ Tests Floating IP retrieval. """
        floatingip = create_floatingip()
        assert ecloud.floating_ips.get(floatingip.id)

    def test_floatingip_update(self, ecloud):
        """ Tests Floating IP updates. """
        floatingip = create_floatingip()

        new_name = 'test name'
        new_vpcid = create_vpc().id

        floatingip.name = new_name
        floatingip.vpc_id = new_vpcid

        floatingip.save()
        floatingip = ecloud.floating_ips.get(floatingip.id)

        assert floatingip.name == new_name

        pytest.skip('https://gitlab.devops.ukfast.co.uk/ukfast/api.ukfast/ecloud/-/issues/588')
        assert floatingip.vpc_id == new_vpcid

    def test_floatingip_delete(self, ecloud):
        """ Tests Floating IP delete. """
        floatingip = create_floatingip()
        floatingip.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.floating_ips.get(floatingip.id)

    def test_floatingip_list(self, ecloud):
        """ Tests Floating IP listing. """
        limit = 5
        for _ in range(limit):
            create_floatingip()
        assert len(ecloud.floating_ips.list()) == limit

    def test_floatingip_assign(self, ecloud):
        """ Tests Floating IP assign functionality. """
        pytest.skip('Need to figure out where to get a nic from.')
        floatingip = create_floatingip()
        floatingip.assign()

    def test_floatingip_unassign(self, ecloud):
        """ Tests Floating IP unassign functionality. """
        pytest.skip('Cannot unassign a nic until we figure out how to add one.')
        create_floatingip().unassign()

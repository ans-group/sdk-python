""" Tests for the eCloud Support implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_firewall_rule_port, create_instance,
    create_router, create_vpc, generate_string, get_ecloud, clear, clear_ecloud, ecloud,
    wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestSupport():
    """ Test class for the eCloud Support module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_support_create(self, ecloud):
        """ Tests Support creation. """
        pytest.skip('Skipping until we can bypass the `Payment Required` error.')
        assert ecloud.support.create(vpc_id=create_vpc().id)

    def test_support_get(self, ecloud):
        """ Tests Support retrieval. """
        pytest.skip('Skipping until we can bypass the `Payment Required` error.')
        support = ecloud.support.create(vpc_id=create_vpc().id)
        ecloud.support.get(support.id)

    def test_support_update(self, ecloud):
        """ Tests Support update. """
        pytest.skip('Skipping until we can bypass the `Payment Required` error.')
        support = ecloud.support.create(vpc_id=create_vpc().id)
        new_vpc_id = create_vpc().id
        support.vpc_id = new_vpc_id
        support.save()
        support = ecloud.support.get(support.id)
        assert support.vpc_id == new_vpc_id

    def test_support_delete(self, ecloud):
        """ Tests Support delete. """
        pytest.skip('Skipping until we can bypass the `Payment Required` error.')
        support = ecloud.support.create(vpc_id=create_vpc().id)
        support.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.support.get(support.id)

    def test_support_list(self, ecloud):
        """ Tests Support listing. """
        pytest.skip('Skipping until we can bypass the `Payment Required` error.')
        limit = 5
        for _ in range(limit):
            ecloud.support.create(vpc_id=create_vpc().id)
        assert len(ecloud.support.list()) == limit

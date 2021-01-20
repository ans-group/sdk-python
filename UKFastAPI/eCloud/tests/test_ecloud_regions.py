""" Tests for the eCloud Regions implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_firewall_rule_port, create_router,
    generate_string, get_ecloud, clear, clear_ecloud, ecloud, wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestRegions():
    """ Test class for the eCloud Regions module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_regions_get(self, ecloud):
        """ Tests Regions retrieval. """
        assert ecloud.regions.get(ecloud.regions.list()[0].id)

    def test_regions_list(self, ecloud):
        """ Tests Regions listing. """
        assert ecloud.regions.list()

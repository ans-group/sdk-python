""" Tests for the eCloud Volumes implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_firewall_rule_port, create_instance,
    create_router, generate_string, get_ecloud, clear, clear_ecloud, ecloud, wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestVolumes():
    """ Test class for the eCloud Volumes module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_volumes_get(self, ecloud):
        """ Tests Volumes retrieval. """
        create_instance()

""" Tests for the eCloud Instances implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_vpc, get_ecloud, clear, clear_ecloud, create_instance, ecloud, create_network)
from UKFastAPI.eCloud.tests import config


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestInstances():
    """ Test class for the eCloud Instances module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_instance_create(self, ecloud):
        """ Tests Instance creation using the minimum required values. """
        assert get_ecloud().instances.create(
            vpc_id=create_vpc().id,
            appliance_id=get_ecloud().appliances.get(config.TEST_APPLIANCE_ID).id,
            network_id=create_network().id,
            vcpu_cores=config.TEST_CPU,
            ram_capacity=config.TEST_RAM)

    def test_instance_create_optionals(self, ecloud):
        """ Tests Instance creation using the minimum required values. """
        assert get_ecloud().instances.create(
            vpc_id=create_vpc().id,
            appliance_id=get_ecloud().appliances.get(config.TEST_APPLIANCE_ID).id,
            network_id=create_network().id,
            vcpu_cores=config.TEST_CPU,
            ram_capacity=config.TEST_RAM)

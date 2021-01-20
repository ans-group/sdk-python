""" Tests for the eCloud implementations that are too small to stick in their own file. """
import pytest

# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    get_ecloud_v1, ecloud, clear_vms, clear_all_vms, generate_vm_name, create_simple_vm,
    wait_for_vm, wait_for_vm_deletion)


@pytest.mark.parametrize('ecloud', [get_ecloud_v1], indirect=True)
@pytest.mark.usefixtures('clear_vms')
class TestMisc():
    """ Test class for the eCloud Virtual Machine module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_all_vms()

    def test_appliance_list(self, ecloud):
        """ Test Appliance objects can be listed. """
        assert ecloud.appliances.list()

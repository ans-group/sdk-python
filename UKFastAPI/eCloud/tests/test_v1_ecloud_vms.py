""" Tests for the eCloud Virtual Machines implementation. """
import time

import pytest
from UKFastAPI.eCloud.tests.config import TEST_ENVIRONMENT
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (clear_all_vms, clear_vms,
                                               create_simple_vm, ecloud,
                                               generate_vm_name, get_ecloud_v1,
                                               wait_for_vm,
                                               wait_for_vm_deletion)
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud_v1], indirect=True)
@pytest.mark.usefixtures('clear_vms')
class TestVms():
    """ Test class for the eCloud Virtual Machine module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_all_vms()

    def test_vm_create(self, ecloud):
        """ Tests Virtual Machine creation using the minimum required values. """
        assert create_simple_vm()

    def test_vm_get(self, ecloud):
        """ Tests Virtual Machine retrieval. """
        vm = create_simple_vm()
        assert ecloud.vms.get(vm.id)

    def test_vm_list(self, ecloud):
        """ Tests Virtual Machine listing. """
        limit = 5
        for _ in range(limit):
            create_simple_vm()
        assert len(ecloud.vms.list()) == limit

    def test_vm_delete(self, ecloud):
        """ Tests Virtual Machine deletion. """
        vm = create_simple_vm()
        vm.delete()
        wait_for_vm_deletion(vm)
        with pytest.raises(UKFastAPIException):
            ecloud.vms.get(vm.id)

    def test_vm_update(self, ecloud):
        """ Tests Virtual Machine updates. """
        vm = create_simple_vm()
        assert vm

        wait_for_vm(vm)

        new_name = generate_vm_name()
        new_cpu = 2
        new_ram = 2

        vm.name = new_name
        vm.cpu = new_cpu
        vm.ram = new_ram

        vm.save()

        # We can actually be too quick here, leading
        # to query the vm before it has updated its properties.
        time.sleep(10)
        vm = ecloud.vms.get(vm.id)

        assert vm.name == new_name
        assert vm.cpu == new_cpu
        assert vm.ram == new_ram

    def test_vm_clone(self, ecloud):
        """ Tests Virtual Machine cloning. """
        if TEST_ENVIRONMENT.lower() != 'private':
            pytest.skip('Private eCloud only.')

        vm = create_simple_vm()
        clone_id = vm.clone(name='{}_clone'.format(vm.name))
        assert ecloud.vms.get(clone_id)

    def test_vm_clone_template(self, ecloud):
        """ Tests Virtual Machine template cloning. """
        if TEST_ENVIRONMENT.lower() != 'private':
            pytest.skip('Private eCloud only.')
        vm = create_simple_vm()
        template_id = vm.clone(name='{}_template'.format(vm.name))
        assert ecloud.vms.get(template_id)

    def test_vm_power_actions(self, ecloud):
        """ Tests Virtual Machine power tests. """
        vm = create_simple_vm()
        wait_for_vm(vm)

        vm = ecloud.vms.get(vm.id)
        assert vm.power_status.lower() == 'online'

        vm.power_off()
        time.sleep(5)
        vm = ecloud.vms.get(vm.id)
        assert vm.power_status.lower() == 'offline'

        vm.power_on()
        time.sleep(5)
        vm = ecloud.vms.get(vm.id)
        assert vm.power_status.lower() == 'online'

        vm.power_restart()
        time.sleep(20)

        vm.power_shutdown()
        time.sleep(5)

        vm.power_reset()
        time.sleep(5)

""" Tests for the eCloud Tags implementation. """
import time

import pytest
from UKFastAPI.eCloud.tests.config import TEST_TAG_KEY, TEST_TAG_VALUE
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (clear_all_vms, clear_vms,
                                               create_simple_vm, ecloud,
                                               generate_vm_name, get_ecloud_v1,
                                               parent, wait_for_vm,
                                               wait_for_vm_deletion)
from UKFastAPI.exceptions import UKFastAPIException


# @pytest.mark.parametrize('parent', [create_simple_vm], indirect=True)
@pytest.mark.parametrize('parent', [create_simple_vm], indirect=True)
@pytest.mark.usefixtures('clear_vms')
class TestVms():
    """ Test class for the eCloud Virtual Machine module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_all_vms()

    def test_tag_create(self, parent):
        """ Tests Tag creation using the minimum required values. """
        assert parent.tags.create(key=TEST_TAG_KEY, value=TEST_TAG_VALUE)

    def test_tag_get(self, parent):
        """ Tests Tag retrieval. """
        parent.tags.create(key=TEST_TAG_KEY, value=TEST_TAG_VALUE)
        assert parent.tags.get(TEST_TAG_KEY)

    def test_tag_update(self, parent):
        """ Tests Tag retrieval. """
        tag = parent.tags.create(key=TEST_TAG_KEY, value=TEST_TAG_VALUE)

        new_value = 'newvalue'
        tag.value = new_value

        tag.save()
        time.sleep(5)
        tag = parent.tags.get(tag.key)

        assert tag.value == new_value

    def test_vm_delete(self, parent):
        """ Tests Tag deletion. """
        tag = parent.tags.create(key=TEST_TAG_KEY, value=TEST_TAG_VALUE)
        tag.delete()
        with pytest.raises(UKFastAPIException):
            parent.tags.get(tag.key)

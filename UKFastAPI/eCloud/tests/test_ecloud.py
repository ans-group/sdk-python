""" Tests for the eCloud module implementation. """
import pytest
from UKFastAPI.exceptions import UKFastAPIException
from UKFastAPI.eCloud.ecloud import eCloud

# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    get_ecloud, ecloud
)


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
class TestEcloud():
    """ Test class for the eCloud module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def test_ecloud_auth_invalid(self, ecloud):
        """ Tests eCloud module when given and invalid authentication token. """
        with pytest.raises(UKFastAPIException):
            eCloud('invalid-token').auth_test()

    def test_ecloud_auth(self, ecloud):
        """ Tests eCloud module when given and valid authentication token. """
        assert ecloud.auth_test()

""" Tests for SafeDNS Settings """
# pylint:disable=unused-import, redefined-outer-name, no-self-use
import pytest
from UKFastAPI.SafeDNS.tests.test_utils import safedns, get_safedns, vcr_decorator
from UKFastAPI.utils import decorate_funcs


@pytest.mark.parametrize('safedns', [get_safedns], indirect=True)
@decorate_funcs(vcr_decorator)
class TestSettings():
    # pylint:disable=too-few-public-methods
    """ Test class for the SafeDNS Settings module. """

    def test_settings(self, safedns):
        """ Test we can get the SafeDNS settings values. """
        assert safedns.settings

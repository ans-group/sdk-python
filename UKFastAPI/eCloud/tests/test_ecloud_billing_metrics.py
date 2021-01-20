""" Tests for the eCloud Billing Metrics implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_firewall_policy, create_firewall_rule, create_firewall_rule_port, create_router,
    generate_string, get_ecloud, clear, clear_ecloud, ecloud, wait_until_complete)
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestBillingMetrics():
    """ Test class for the eCloud Billing Metrics module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_billing_metrics_get(self, ecloud):
        """ Tests Billing Metrics retrieval. """
        pytest.skip('Skipping until we can get billing metrics assigned to a test account.')
        assert ecloud.billing_metrics.get(ecloud.billing_metrics.list()[0].id)

    def test_billing_metrics_list(self, ecloud):
        """ Tests Billing Metrics listing. """
        pytest.skip('Skipping until we can get billing metrics assigned to a test account.')
        assert ecloud.billing_metrics.list()

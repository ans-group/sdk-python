""" Tests for the Account implementation. """
import pytest
from UKFastAPI.Account.account import Account
from UKFastAPI.exceptions import UKFastAPIException

# pylint:disable = unused-import
from UKFastAPI.Account.tests.test_utils import get_account, account


@pytest.mark.parametrize('account', [get_account], indirect=True)
class TestAccount():
    """ Test class for the Account module. """
    # pylint:disable = no-self-use, redefined-outer-name

    def test_account_auth_blank(self, account):
        # pylint:disable = unused-argument
        """ Tests Account module when given no authentication token. """
        with pytest.raises(UKFastAPIException):
            Account()

    def test_account_auth_invalid(self, account):
        # pylint:disable = unused-argument
        """ Tests Account module when given and invalid authentication token. """
        with pytest.raises(UKFastAPIException):
            Account('invalid-token').auth_test()

    def test_account_auth_valid(self, account):
        """ Tests Account module when given and valid authentication token. """
        assert account.auth_test()

    def test_details(self, account):
        """ Ensure the UKFast Account Details can be accessed. """
        assert account.details

    def test_contacts(self, account):
        """ Tests that UKFast Account Contacts can be retrieved. """
        contacts = account.contacts.list()
        assert contacts
        contact = account.contacts.get(contacts[0].id)
        assert contact

    def test_credits(self, account):
        """ Tests that UKFast Account Credits can be retrieved. """
        assert account.credits

    def test_invoices(self, account):
        """ Tests that UKFast Account Invoices can be retrieved. """
        invoices = account.invoices.list()
        assert isinstance(invoices, list)

        if not invoices:
            pytest.skip('No Invoices linked to account. Cannot continue with Invoice testing.')

        # assert invoices
        # invoice = account.invoices.get(invoices[0].id)
        # assert invoice

    def test_invoice_queries(self, account):
        """ Tests that UKFast Account Invoice Queries can be retrieved. """
        account.invoice_queries.list()
        pytest.skip('No Invoices linked to account. Cannot continue with Invoice testing.')

    def test_products(self, account):
        """ Tests that UKFast Account Products can be retrieved. """
        assert account.products

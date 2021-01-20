""" Tests for the Billing implementation. """
import random
import string
import pytest
from UKFastAPI.Billing.billing import Billing
from UKFastAPI.exceptions import UKFastAPIException

# pylint:disable = unused-import
from UKFastAPI.Billing.tests.test_utils import (
    get_billing, billing, get_valid_card_details, clear_billing_cards
)


@pytest.mark.parametrize('billing', [get_billing], indirect=True)
class TestBilling():
    """ Test class for the Billing module. """
    # pylint:disable = no-self-use, redefined-outer-name

    def test_billing_auth_blank(self, billing):
        # pylint:disable = unused-argument
        """ Tests Billing module when given no authentication token. """
        with pytest.raises(UKFastAPIException):
            Billing()

    def test_billing_auth_invalid(self, billing):
        # pylint:disable = unused-argument
        """ Tests Billing module when given and invalid authentication token. """
        with pytest.raises(UKFastAPIException):
            Billing('invalid-token').auth_test()

    def test_billing_auth_valid(self, billing):
        """ Tests Billing module when given and valid authentication token. """
        assert billing.auth_test()

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_create_minimum(self, billing):
        """ Tests Card creation using the minimum required values. """
        card = billing.cards.create(
            **get_valid_card_details()
        )

        assert card.name == get_valid_card_details()['name']
        assert card.address == get_valid_card_details()['address']
        assert card.postcode == get_valid_card_details()['postcode']
        assert card.card_number[-4] == get_valid_card_details()['card_number'][-4]
        assert card.card_type.lower() == get_valid_card_details()['card_type'].lower()
        assert card.valid_from == get_valid_card_details()['valid_from']
        assert card.expiry == get_valid_card_details()['expiry']

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_create_optionals(self, billing):
        """ Test Card creation with the full optional set of values. """
        friendly_name = 'my card'
        issue_number = 23
        primary_card = False

        card = billing.cards.create(
            **{
                **get_valid_card_details(),
                **{
                    'friendly_name': friendly_name,
                    'issue_number': issue_number,
                    'primary_card': primary_card
                }
            }
        )

        assert card.friendly_name == friendly_name
        # assert card.issue_number == issue_number
        assert card.primary_card == primary_card

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_create_empty(self, billing):
        """ Tests Card creation using empty values. """
        with pytest.raises(UKFastAPIException):
            billing.cards.create(**{key: '' for key in get_valid_card_details()})

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_create_long_name(self, billing):
        """ Tests Card creation using empty values. """
        limit = 101
        details = get_valid_card_details()
        details['name'] = ''.join(random.choice(string.ascii_lowercase) for i in range(limit))
        with pytest.raises(UKFastAPIException):
            billing.cards.create(**details)

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_get(self, billing):
        """ Test Card retreival. """
        card = billing.cards.create(**get_valid_card_details())
        assert billing.cards.get(card.id)

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_get_invalid_id(self, billing):
        """ Test getting a Card that does not exist. """
        with pytest.raises(UKFastAPIException):
            billing.cards.get(0)

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_update(self, billing):
        """ Test updating a Card. """
        card = billing.cards.create(**get_valid_card_details())

        updated_name = 'new name'
        updated_address = '123 new address'
        updated_postcode = 'M465L'
        updated_card_number = '4111111111111111'
        updated_card_type = 'Visa'
        updated_valid_from = '01/20'
        updated_expiry = '01/21'
        updated_friendly_name = 'hello'
        updated_issue_number = 1
        updated_primary_card = False

        card.name = updated_name
        card.address = updated_address
        card.postcode = updated_postcode
        card.card_number = updated_card_number
        card.card_type = updated_card_type
        card.valid_from = updated_valid_from
        card.expiry = updated_expiry
        card.friendly_name = updated_friendly_name
        card.issue_number = updated_issue_number
        card.primary_card = updated_primary_card

        card.save()
        card = billing.cards.get(card.id)

        assert card.name == updated_name
        assert card.address == updated_address
        assert card.postcode == updated_postcode
        assert card.card_number[-4:] == updated_card_number[-4:]
        assert card.card_type == updated_card_type
        assert card.valid_from == updated_valid_from
        assert card.expiry == updated_expiry
        assert card.friendly_name == updated_friendly_name
        # assert card.issue_number == updated_issue_number
        assert card.primary_card == updated_primary_card

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_delete(self, billing):
        """ Ensures a Record can be deleted. """
        card = billing.cards.create(**get_valid_card_details())
        card.delete()
        with pytest.raises(UKFastAPIException):
            billing.cards.get(card.id)

    @pytest.mark.usefixtures('clear_billing_cards')
    def test_card_list(self, billing):
        """ Ensures Card objects can be listed. """
        limit = 10
        current_amt = len(billing.cards.list())
        for _ in range(limit):
            billing.cards.create(**get_valid_card_details())
        assert len(billing.cards.list(all=True)) == limit + current_amt

    def test_cloud_costs(self, billing):
        """ Tests that UKFast Billing Cloud Costs can be retrieved. """
        assert billing.cloud_costs

    def test_direct_debit(self, billing):
        """ Tests that UKFast Billing Direct Debit can be retrieved. """
        assert billing.direct_debit

    def test_invoices(self, billing):
        """ Tests that UKFast Billing Invoices can be retrieved. """
        invoices = billing.invoices.list()
        assert isinstance(invoices, list)

        if not invoices:
            pytest.skip('No Invoices linked to account. Cannot continue with Invoice testing.')

        # assert invoices
        # invoice = billing.invoices.get(invoices[0].id)
        # assert invoice

    def test_invoice_queries(self, billing):
        """ Tests that UKFast Billing Invoice Queries can be retrieved. """
        billing.invoice_queries.list()
        pytest.skip('No Invoices linked to account. Cannot continue with Invoice testing.')

    def test_payments(self, billing):
        """ Tests that UKFast Billing Payment can be retrieved. """
        assert billing.payments

    def test_recurring_costs(self, billing):
        """ Tests that UKFast Billing Payment can be retrieved. """
        assert billing.recurring_costs

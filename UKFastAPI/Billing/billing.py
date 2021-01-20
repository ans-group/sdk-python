""" The Billing implementation. """
from UKFastAPI.base import (BaseApi, IBareObject, ICreateable, IDeleteable,
                            IManagedObject, IManager, IUpdateable)
from UKFastAPI.Billing import config

# pylint:disable=too-few-public-methods,too-many-ancestors


class Billing(BaseApi):
    """ Billing class representing the UKFast Billing object. """
    # pylint:disable=too-many-instance-attributes

    def __init__(self, auth=None):
        super().__init__(auth)
        self._base = super()
        self._url = config.BASE_URL
        self.cards = CardManager(self._base, Card, config.CARDS_URL)
        self.cloud_costs = CloudCosts(self._base, config.CLOUD_COSTS_URL)
        self.direct_debit = DirectDebit(self._base, config.DIRECT_DEBIT_URL)
        self.invoices = InvoiceManager(self._base, Invoice, config.INVOICE_URL)
        self.invoice_queries = InvoiceQueryManager(
            self._base, InvoiceQuery, config.INVOICE_QUERIES_URL)
        self.payments = PaymentManager(self._base, Payment, config.PAYMENTS_URL)
        self.recurring_costs = RecurringCostManager(
            self._base, RecurringCost, config.RECURRING_COSTS_URL)


class Card(IManagedObject, IUpdateable, IDeleteable):
    """ Card class representing SafeDNS Zone objects. """


class CardManager(IManager, ICreateable):
    # pylint:disable=too-many-ancestors
    """ Manager class for Card objects. """


class CloudCosts(IBareObject):
    """ Details class representing the UKFast Billing Cloud Costs object. """


class DirectDebit(IBareObject):
    """ Details class representing the UKFast Billing Direct Debit object. """


class Invoice(IManagedObject):
    """ Invoice class representing Invoices within a SafeDNS Account object. """


class InvoiceManager(IManager):
    """ Manager class for Invoice objects. """


class InvoiceQuery(IManagedObject):
    """ InvoiceQuery class representing Invoice Queries within a SafeDNS Account object. """


class InvoiceQueryManager(IManager):
    # TODO: InvoiceQuery has a create request (post) to create invoice queries.
    """ Manager class for Invoice objects. """


class Payment(IManagedObject):
    """ Contact class representing Payments within a UKFast Billing object. """


class PaymentManager(IManager):
    """ Manager class for Payments objects. """


class RecurringCost(IManagedObject):
    """ Contact class representing a Recurring Cost within a UKFast Billing object. """


class RecurringCostManager(IManager):
    """ Manager class for Recurring Cost objects. """

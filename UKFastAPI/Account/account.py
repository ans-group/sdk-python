""" The Account implementation. """
from UKFastAPI.base import BaseApi, IBareObject, IManager, IManagedObject
from UKFastAPI.Account import config

# pylint:disable=too-few-public-methods


class Account(BaseApi):
    """ Account class representing the UKFast Account object. """
    # pylint:disable=too-many-instance-attributes

    def __init__(self, auth=None):
        super().__init__(auth)
        self._base = super()
        self._url = config.BASE_URL
        self.details = Details(self._base, config.DETAILS_URL)
        self.contacts = ContactsManager(self._base, Contact, config.CONTACTS_URL)
        self.credits = Credits(self._base, config.CREDITS_URL)
        self.invoices = InvoiceManager(self._base, Invoice, config.INVOICES_URL)
        self.invoice_queries = InvoiceQueryManager(
            self._base, InvoiceQuery, config.INVOICEQUERIES_URL)
        self.products = Products(self._base, config.PRODUCTS_URL)


class Details(IBareObject):
    """ Details class representing the UKFast Account Details object. """


class Contact(IManagedObject):
    """ Contact class representing Contacts within a UKFast Account object. """


class ContactsManager(IManager):
    """ Manager class for Contact objects. """


class Credits(IBareObject):
    """ Credits class representing Credits within a UKFast Account object. """


class Invoice(IManagedObject):
    """ Invoice class representing Invoices within a UKFast Account object. """


class InvoiceManager(IManager):
    """ Manager class for Invoice objects. """


class InvoiceQuery(IManagedObject):
    """ InvoiceQuery class representing Invoice Queries within a UKFast Account object. """


class InvoiceQueryManager(IManager):
    """ Manager class for Invoice objects. """


class Products(IBareObject):
    """ InvoiceQuery class representing Invoice Queries within a UKFast Account object. """

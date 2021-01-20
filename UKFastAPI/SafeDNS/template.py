""" The Template and TemplateManager implementations. """
from UKFastAPI.base import IManager, IManagedObject, ICreateable, IUpdateable, IDeleteable
from UKFastAPI.SafeDNS.record import RecordManager, Record
from UKFastAPI.SafeDNS import config

# pylint:disable=too-many-ancestors,too-few-public-methods


class Template(IManagedObject, IUpdateable, IDeleteable):
    """ Template class representing SafeDNS Template objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.records = RecordManager(self._base, Record, config.TEMPLATE_RECORD_URL.format(self.id))


class TemplateManager(IManager, ICreateable):
    """ Manager class for Template objects. """

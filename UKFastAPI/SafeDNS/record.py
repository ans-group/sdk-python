""" The Record and RecordManager implementations. """
from UKFastAPI.base import IManager, IManagedObject, ICreateable, IUpdateable, IDeleteable

# pylint:disable=too-many-ancestors


class Record(IManagedObject, IUpdateable, IDeleteable):
    """ Record class representing Records within a SafeDNS Zone object. """


class RecordManager(IManager, ICreateable):
    """ Manager class for Record objects. """

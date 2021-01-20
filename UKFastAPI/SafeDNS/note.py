""" The Note and NoteManager implementations. """
from UKFastAPI.base import IManager, IManagedObject, ICreateable, IUpdateable, IDeleteable
from UKFastAPI.SafeDNS import config
from UKFastAPI import exceptions


class Note(IManagedObject):
    """ Note class representing Notes within a SafeDNS Zone object. """


class NoteManager(IManager, ICreateable):
    """ Manager class for Note objects. """

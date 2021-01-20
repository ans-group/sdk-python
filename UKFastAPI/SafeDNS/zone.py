""" The Zone and ZoneManager implementations. """
from UKFastAPI.base import IManagedObject, IManager, ICreateable, IDeleteable, IUpdateable
from UKFastAPI import exceptions
from UKFastAPI.SafeDNS import config
from UKFastAPI.SafeDNS.note import NoteManager, Note
from UKFastAPI.SafeDNS.record import RecordManager, Record


class Zone(IManagedObject, IUpdateable, IDeleteable):
    """ Zone class representing SafeDNS Zone objects. """
    _identifier = 'name'

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.records = RecordManager(self._base, Record, config.RECORD_URL.format(self.name))
        self.notes = NoteManager(self._base, Note, config.NOTE_URL.format(self.name))


class ZoneManager(IManager, ICreateable):
    # pylint:disable=too-many-ancestors
    """ Manager class for Zone objects. """

    def get(self, identifier, **kwargs):
        if identifier == '':
            raise exceptions.UKFastSDKException('Zone name must be provided.')
        return super().get(identifier, **kwargs)

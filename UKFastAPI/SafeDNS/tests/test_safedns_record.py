""" Tests for SafeDNS Records """
import pytest
# pylint:disable=unused-import, redefined-outer-name, no-self-use
from UKFastAPI.SafeDNS.tests.test_utils import (
    safedns, parent, clear_safedns, create_zone, create_template, generate_zone_name)
from UKFastAPI.SafeDNS.tests import config
from UKFastAPI import exceptions
from UKFastAPI.SafeDNS.template import Template
from UKFastAPI.config import DEFAULT_PER_PAGE


@pytest.mark.parametrize('parent', [create_zone, create_template], indirect=True)
@pytest.mark.usefixtures('clear_safedns')
class TestRecords():
    """ Test class for the Record module. """

    def create_simple_record(self, obj, name=None):
        """ Helper function to create Records. """
        return obj.records.create(
            name=name if name else config.TEST_RECORD_NAME + obj.name,
            type=config.TEST_RECORD_TYPE,
            content=name if name else config.TEST_RECORD_CONTENT + obj.name,
            ttl=config.TEST_RECORD_TTL,
            priority=config.TEST_RECORD_PRIORITY
        )

    def test_record_create(self, parent):
        """ Tests a Record can be created within a Zone or Template. """
        assert self.create_simple_record(parent)

    def test_record_create_long_name(self, parent):
        """ Ensures a Record cannot be created with an overly long name within a Zone. """
        if isinstance(parent, Template):
            pytest.skip('There is no limit on the name for a Template.')

        with pytest.raises(exceptions.UKFastAPIException):
            self.create_simple_record(
                parent,
                '{}.{}'.format(
                    generate_zone_name(100),
                    parent.name
                )
            )

    def test_record_create_empty_name(self, parent):
        """ Ensures a Record cannot be created with a blank name. """
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.create(
                name='',
                type=config.TEST_RECORD_TYPE,
                content=config.TEST_RECORD_CONTENT + parent.name,
                priority=config.TEST_RECORD_PRIORITY
            )

    def test_record_get(self, parent):
        """ Tests a Record can be retrieved from within a Zone or Template. """
        assert parent.records.get(self.create_simple_record(parent).id)

    def test_record_get_invalid_id(self, parent):
        """ Tests getting a Note with invalid _identifiers. """
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.get(0)
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.get('abc')

    def test_record_update(self, parent):
        """ Ensures a Record can be updated within a Zone or Template. """
        record = self.create_simple_record(parent)

        new_name = 'test2.' + parent.name
        new_type = config.TEST_RECORD_TYPE
        new_content = 'mx2' + record.name
        new_ttl = 86300
        new_priority = 20

        record.name = new_name
        record.type = new_type
        record.content = new_content
        record.ttl = new_ttl
        record.priority = new_priority

        record.save()
        record = parent.records.get(record.id)

        assert record.name == new_name
        assert record.type == new_type
        assert record.content == new_content
        assert record.ttl == new_ttl
        assert record.priority == new_priority

    def test_record_update_id(self, parent):
        """ Ensures a Record cannot have an id updated. """
        record = self.create_simple_record(parent)
        with pytest.raises(exceptions.UKFastSDKException):
            record.id = 0

    def test_record_delete(self, parent):
        """ Ensures a Record can be deleted. """
        record = self.create_simple_record(parent)
        record.delete()
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.get(record.id)

    def test_record_list(self, parent):
        """ Test listing all zones. """
        list_limit = 30

        current_len = len(parent.records.list(all=True))
        if current_len < list_limit:
            for _ in range(list_limit - current_len):
                assert self.create_simple_record(parent)

        assert len(parent.records.list(all=True)) == list_limit

    def test_pagination(self, parent):
        """ Tests the pagination functionality. """
        list_limit = 10

        current_len = len(parent.records.list(all=True))
        if current_len < list_limit:
            for _ in range(list_limit - current_len):
                assert self.create_simple_record(parent)

        per_page_limit = 3
        assert len(parent.records.list()) == DEFAULT_PER_PAGE
        assert len(parent.records.list(page=2)) == DEFAULT_PER_PAGE
        assert len(parent.records.list(per_page=per_page_limit)) == per_page_limit

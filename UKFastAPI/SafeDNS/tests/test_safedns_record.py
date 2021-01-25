""" Tests for SafeDNS Records """
import pytest
from UKFastAPI import exceptions
from UKFastAPI.config import DEFAULT_PER_PAGE
from UKFastAPI.SafeDNS.template import Template
from UKFastAPI.SafeDNS.tests import config
# pylint:disable=unused-import, redefined-outer-name, no-self-use
from UKFastAPI.SafeDNS.tests.test_utils import (clear_safedns,
                                                create_simple_record,
                                                create_template, create_zone,
                                                generate_zone_name, get_zone_names, parent,
                                                safedns, vcr_decorator)
from UKFastAPI.utils import decorate_funcs


@pytest.mark.parametrize('parent', [create_zone, create_template], indirect=True)
@pytest.mark.usefixtures('clear_safedns')
@decorate_funcs(vcr_decorator)
class TestRecords():
    """ Test class for the Record module. """

    def test_record_create(self, parent):
        """ Tests a Record can be created within a Zone or Template. """
        assert create_simple_record(parent)

    def test_record_get(self, parent):
        """ Tests a Record can be retrieved from within a Zone or Template. """
        assert parent.records.get(create_simple_record(parent).id)

    def test_record_get_invalid_id(self, parent):
        """ Tests getting a Note with invalid _identifiers. """
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.get(0)
        with pytest.raises(exceptions.UKFastAPIException):
            parent.records.get('abc')

    def test_record_update(self, parent):
        """ Ensures a Record can be updated within a Zone or Template. """
        record = create_simple_record(parent)

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

    def test_record_update_id(self, parent):
        """ Ensures a Record cannot have an id updated. """
        record = create_simple_record(parent)
        with pytest.raises(exceptions.UKFastSDKException):
            record.id = 0

    def test_record_delete(self, parent):
        """ Ensures a Record can be deleted. """
        record = create_simple_record(parent)
        record.delete()

    def test_record_list(self, parent):
        """ Test listing all zones. """
        pytest.skip('This test is a pain to get working with VCR.')
        list_limit = 10

        current_len = len(parent.records.list(all=True))
        if current_len < list_limit:
            for x in range(list_limit - current_len):
                assert create_simple_record(parent, name=get_zone_names(index=x).split('.')[
                    0] + '.' + parent.name)

        assert len(parent.records.list(all=True)) == list_limit

    def test_pagination(self, parent):
        pytest.skip('Can\'t reliably test pagination with VCR in place.')
        """ Tests the pagination functionality. """
        list_limit = 10

        current_len = len(parent.records.list(all=True))
        if current_len < list_limit:
            for x in range(list_limit - current_len):
                assert create_simple_record(
                    parent,
                    name=get_zone_names(index=x).split('.')[0] + '.' + parent.name
                )

        per_page_limit = 3
        assert len(parent.records.list()) == DEFAULT_PER_PAGE
        assert len(parent.records.list(page=2)) == DEFAULT_PER_PAGE
        assert len(parent.records.list(per_page=per_page_limit)) == per_page_limit

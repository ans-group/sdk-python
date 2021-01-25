""" Tests for SafeDNS Templates """
import pytest
from UKFastAPI import exceptions
from UKFastAPI.utils import decorate_funcs
# pylint:disable=unused-import, redefined-outer-name, no-self-use
from UKFastAPI.SafeDNS.tests.test_utils import (
    get_zone_names, safedns, clear_safedns, generate_zone_name, get_safedns, create_template,
    create_zone, vcr_decorator)


@pytest.mark.parametrize('safedns', [get_safedns], indirect=True)
@pytest.mark.usefixtures('clear_safedns')
@decorate_funcs(vcr_decorator)
class TestTemplates():
    """ Test class for the Template module. """

    def test_template_create(self, safedns):
        """ Test creating a single valid Template. """
        name = 'lskyzzkxde.com'
        template = safedns.templates.create(
            name=name,
            default=True
        )
        assert template
        assert template.name == name
        assert template.default

    def test_template_create_duplicate(self, safedns):
        """ Test creating two Templates with the same name. """
        name = get_zone_names()
        assert safedns.templates.create(name=name, default=False)
        with pytest.raises(exceptions.UKFastAPIException):
            safedns.templates.create(name=name, default=False)

    def test_template_create_empty_name(self, safedns):
        """ Test creating a Templates without a name. """
        with pytest.raises(exceptions.UKFastAPIException):
            safedns.templates.create(name='', default=False)

    def test_template_get(self, safedns):
        """ Test creating and getting a valid Templates. """
        name = get_zone_names()
        template = safedns.templates.create(name=name, default=False)
        assert template
        assert safedns.templates.get(template.id)

    def test_template_get_invalid_id(self, safedns):
        """ Test getting a Template that does not exist. """
        with pytest.raises(exceptions.UKFastAPIException):
            safedns.templates.get(0)

    def test_template_update(self, safedns):
        """ Test we can update a Template description. """
        template = safedns.templates.create(name='zvvvmqgjkbjrsto.com', default=False)
        new_name = 'qwarnvwiqicfwb.com'
        template.name = new_name
        template.default = True
        template.save()

    def test_template_delete(self, safedns):
        """ Ensure that we can delete a Template. """
        template = safedns.templates.create(name=get_zone_names(), default=False)
        template.delete()

    def test_template_list(self, safedns):
        """ Test listing all Templates. """
        list_limit = 10
        assert len(safedns.templates.list(all=True)) == 0
        for x in range(list_limit):
            safedns.templates.create(name=get_zone_names(index=x), default=False)
        assert len(safedns.templates.list(all=True)) == list_limit

""" Tests for SafeDNS Zones """
# pylint:disable=unused-import, redefined-outer-name, no-self-use
import pytest
from UKFastAPI import exceptions
from UKFastAPI.SafeDNS.tests import config
from UKFastAPI.utils import decorate_funcs
from UKFastAPI.SafeDNS.tests.test_utils import (
    get_zone_names, safedns, clear_safedns, generate_zone_name, get_safedns, vcr_decorator)


@pytest.mark.parametrize('safedns', [get_safedns], indirect=True)
@pytest.mark.usefixtures('clear_safedns')
@decorate_funcs(vcr_decorator)
class TestZones():
    """ Test class for the Zone module. """

    def test_zone_create(self, safedns):
        """ Test creating a single valid Zone. """
        name = config.TEST_ZONE_NAME
        zone = safedns.zones.create(
            name=name,
            description=config.TEST_DESCRIPTION
        )
        assert zone
        assert zone.name == name
        assert zone.description == config.TEST_DESCRIPTION

    def test_zone_create_empty_name(self, safedns):
        """ Test creating a Zone without a name. """
        with pytest.raises(exceptions.UKFastAPIException):
            safedns.zones.create(name='')

    def test_zone_get(self, safedns):
        """ Test creating and getting a valid Zone. """
        name = config.TEST_ZONE_NAME
        assert safedns.zones.create(name=name, description=config.TEST_DESCRIPTION)
        assert safedns.zones.get(name)

    def test_zone_get_invalid_name(self, safedns):
        """ Test getting a Zone that does not exist. """
        with pytest.raises(exceptions.UKFastAPIException):
            safedns.zones.get(get_zone_names())

    def test_zone_get_empty_name(self, safedns):
        """ Ensure that a type error gets raised if no Zone name is provided. """
        with pytest.raises(exceptions.UKFastSDKException):
            safedns.zones.get('')

    def test_zone_update(self, safedns):
        """ Test we can update a Zone description. """
        zone = safedns.zones.create(name=get_zone_names(), description=config.TEST_DESCRIPTION)
        new_description = config.TEST_DESCRIPTION[::-1]
        zone.description = new_description
        zone.save()

    def test_zone_update_name(self, safedns):
        """ Ensure that we cannot update a Zone name. """
        name = get_zone_names()
        zone = safedns.zones.create(name=name, description=config.TEST_DESCRIPTION)
        with pytest.raises(exceptions.UKFastSDKException):
            zone.name = name[::-1]

    def test_zone_delete(self, safedns):
        """ Ensure that we can delete a Zone. """
        zone = safedns.zones.create(name=get_zone_names(), description=config.TEST_DESCRIPTION)
        zone.delete()

    def test_zone_list(self, safedns):
        """ Test listing all zones. """
        list_limit = 5
        assert len(safedns.zones.list(all=True)) == 0
        for x in range(list_limit):
            safedns.zones.create(name=get_zone_names(index=x))
        assert len(safedns.zones.list()) == list_limit

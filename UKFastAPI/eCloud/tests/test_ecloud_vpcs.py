""" Tests for the eCloud Virtual Private Clouds implementation. """
import pytest
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    create_vpc, get_ecloud, clear, clear_ecloud, ecloud, random_emoji, generate_string, get_region)
from UKFastAPI.eCloud.tests import config
from UKFastAPI import exceptions


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestVpcs():
    """ Test class for the eCloud Virtual Private Cloud module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_vpc_create(self, ecloud):
        """ Tests Virtual Private Cloud creation using the minimum required values. """
        assert ecloud.vpcs.create(region_id=get_region().id)

    def test_vpc_create_optionals(self, ecloud):
        """ Tests VPC creation using all the optional args. """
        region = get_region()
        vpc = ecloud.vpcs.create(name=config.TEST_VPC_NAME, region_id=region.id)
        assert vpc.name == config.TEST_VPC_NAME
        assert vpc.region_id == region.id

    def test_vpc_create_long_name(self, ecloud):
        """ Tests Virtual Private Cloud creation using the minimum required values. """
        limit = 1000
        name = generate_string(limit)
        assert ecloud.vpcs.create(name=name, region_id=get_region().id)

    def test_vpc_create_emoji_name(self, ecloud):
        """ Tests Virtual Private Cloud creation using the minimum required values. """
        limit = 100
        name = [random_emoji()[0] for _ in range(limit)]
        with pytest.raises(exceptions.UKFastAPIException):
            ecloud.vpcs.create(name=name, region_id=get_region().id)

    def test_vpc_create_invalid_region(self, ecloud):
        """ Attempt to create a VPC using an invalid region id. """
        with pytest.raises(exceptions.UKFastAPIException):
            ecloud.vpcs.create(name=config.TEST_VPC_NAME, region_id='reg-foo')

    def test_vpc_get(self, ecloud):
        """ Test VPC retrieval. """
        vpc = ecloud.vpcs.create(region_id=get_region().id)
        assert ecloud.vpcs.get(vpc.id)

    def test_vpc_get_invalid(self, ecloud):
        """ Attempt to retrieval a VPC with an invalid region id. """
        with pytest.raises(exceptions.UKFastAPIException):
            ecloud.vpcs.create(region_id='vpc-foo')

    def test_vpc_update(self, ecloud):
        """ Test VPC updates. """
        vpc = ecloud.vpcs.create(name=config.TEST_VPC_NAME, region_id=get_region().id)
        new_name = generate_string()
        vpc.name = new_name
        vpc.save()
        vpc = ecloud.vpcs.get(vpc.id)
        assert vpc.name == new_name

    def test_vpc_update_emoji(self, ecloud):
        """ Attempt to update a VPC name using an emoji symbol. """
        vpc = ecloud.vpcs.create(name=config.TEST_VPC_NAME, region_id=get_region().id)
        new_name = [random_emoji()[0] for _ in range(10)]
        vpc.name = new_name
        with pytest.raises(exceptions.UKFastAPIException):
            vpc.save()

    def test_vpc_delete(self, ecloud):
        """ Test VPC deletion. """
        vpc = ecloud.vpcs.create(name=config.TEST_VPC_NAME, region_id=get_region().id)
        vpc.delete()
        with pytest.raises(exceptions.UKFastAPIException):
            ecloud.vpcs.get(vpc.id)

    def test_vpc_list(self, ecloud):
        """ Tests VPC listing. """
        limit = 5
        for _ in range(limit):
            create_vpc()
        assert len(ecloud.vpcs.list()) == limit

""" Tests for the eCloud Routers implementation. """
from functools import partial
import pytest
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    clear,
    clear_ecloud, create_router, create_vpc,
    ecloud,
    get_ecloud,
    generate_string, wait_until_complete
)


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestRouters():
    """ Test class for the eCloud Routers module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_routers_create(self, ecloud):
        """ Tests Router creation using the minimum required values. """
        assert create_router()

    def test_routers_create_invalid_vpc(self, ecloud):
        """ Tests Router creation using an invalid vpc id. """
        with pytest.raises(UKFastAPIException):
            ecloud.routers.create(
                name=config.TEST_ROUTER_NAME,
                vpc_id='vpc-1234567z',
            )

    def test_routers_create_long_name(self, ecloud):
        """ Tests Routers creation using an overly long name. """
        assert ecloud.routers.create(
            name=generate_string(1000),
            vpc_id=create_vpc().id
        )

    def test_routers_create_empty_name(self, ecloud):
        """ Tests Routers creation using an empty name. """
        assert ecloud.routers.create(
            name='',
            vpc_id=create_vpc().id
        )

    def test_routers_get(self, ecloud):
        """ Tests Router retrieval. """
        router = create_router()
        assert ecloud.routers.get(router.id)

    def test_routers_get_invalid_id(self, ecloud):
        """ Tests Router retrieval. """
        with pytest.raises(UKFastAPIException):
            assert ecloud.routers.get('rtr-1234567z')

    def test_routers_update(self, ecloud):
        """ Tests Router updating. """
        router = wait_until_complete(partial(ecloud.routers.get, create_router().id))

        new_name = create_router().name
        new_vpcid = create_vpc().id

        router.name = new_name
        router.vpc_id = new_vpcid

        router.save()
        router = ecloud.routers.get(router.id)

        assert router.name == new_name
        assert router.vpc_id == new_vpcid

    def test_routers_update_invalid_vpc(self, ecloud):
        """ Tests Router updating. """
        router = wait_until_complete(partial(ecloud.routers.get, create_router().id))
        router.vpc_id = 'rtr-1234567z'
        with pytest.raises(UKFastAPIException):
            router.save()

    def test_routers_delete(self, ecloud):
        """ Tests Router delete. """
        router = create_router()
        router.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.routers.get(router.id)

    def test_routers_list(self, ecloud):
        """ Tests Router listing. """
        limit = 5
        for _ in range(limit):
            create_router()
        assert len(ecloud.routers.list()) == limit

    def test_routers_get_firewall_rules(self, ecloud):
        """ Tests Router firewall rules retrieval. """
        pytest.skip('https://gitlab.devops.ukfast.co.uk/ukfast/api.ukfast/ecloud/-/issues/592')
        assert create_router().firewall_rules.list()

    def test_routers_get_networks(self, ecloud):
        """ Tests Router networks retrieval. """
        assert isinstance(create_router().networks.list(), list)

    def test_routers_get_vpns(self, ecloud):
        """ Tests Router networks retrieval. """
        assert isinstance(create_router().vpns.list(), list)

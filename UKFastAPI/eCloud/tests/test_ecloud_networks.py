""" Tests for the eCloud Networks implementation. """
import pytest
from UKFastAPI.eCloud.tests import config
from UKFastAPI.exceptions import UKFastAPIException
# pylint:disable = unused-import
from UKFastAPI.eCloud.tests.test_utils import (
    clear,
    clear_ecloud,
    create_instance,
    create_network,
    create_router,
    ecloud,
    generate_string,
    get_ecloud, wait_until_complete
)


@pytest.mark.parametrize('ecloud', [get_ecloud], indirect=True)
@pytest.mark.usefixtures('clear')
class TestNetworks():
    """ Test class for the eCloud Networks module. """
    # pylint:disable=no-self-use,redefined-outer-name,unused-argument

    def teardown_class(self):
        # pylint:disable=missing-function-docstring
        clear_ecloud()

    def test_network_create(self, ecloud):
        """ Tests Network creation using the minimum required values. """
        assert ecloud.networks.create(
            name=config.TEST_NETWORK_NAME,
            router_id=create_router().id,
            subnet=config.TEST_SUBNET)

    def test_network_create_long_name(self, ecloud):
        """ Tests Network creation using an overly long name. """
        assert ecloud.networks.create(
            name=generate_string(1000),
            router_id=create_router().id,
            subnet=config.TEST_SUBNET)

    def test_network_create_invalid_router(self, ecloud):
        """ Tests Network creation using an invalid router id. """
        with pytest.raises(UKFastAPIException):
            ecloud.networks.create(
                name=config.TEST_NETWORK_NAME,
                router_id='rtr-jofdskljdfs',
                subnet=config.TEST_SUBNET)

    def test_network_create_invalid_subnet(self, ecloud):
        """ Tests Network creation using an invalid subnet. """
        with pytest.raises(UKFastAPIException):
            ecloud.networks.create(
                name=config.TEST_NETWORK_NAME,
                router_id=create_router().id,
                subnet='0.0.0.0')

    def test_network_get(self, ecloud):
        """ Tests Network retrieval. """
        network = create_network()
        assert ecloud.networks.get(network.id)

    def test_network_get_invalid_id(self, ecloud):
        """ Tests Network retrieval with invalid network id. """
        with pytest.raises(UKFastAPIException):
            ecloud.networks.get('net-1234567z')

    def test_network_update(self, ecloud):
        """ Tests Network update. """
        network = create_network()

        router = create_router()

        new_name = generate_string(50)
        new_router_id = router.id
        new_subnet = '10.10.10.10/26'

        network.name = new_name
        network.router_id = new_router_id
        network.subnet = new_subnet

        network.save()
        network = ecloud.networks.get(network.id)

        assert network.name == new_name
        assert network.router_id == new_router_id
        assert network.subnet == new_subnet

    def test_network_update_invalid_router(self, ecloud):
        """ Tests Network update with an invalid router id. """
        network = create_network()
        network.router_id = 'rtr-1234567z'
        with pytest.raises(UKFastAPIException):
            network.save()

    def test_network_update_invalid_subnet(self, ecloud):
        """ Tests Network update with an invalid subnet. """
        network = create_network()
        network.router_id = '1.1.1.1/0'
        with pytest.raises(UKFastAPIException):
            network.save()

    def test_network_delete(self, ecloud):
        """ Tests Network update with an invalid subnet. """
        network = create_network()
        network.delete()
        with pytest.raises(UKFastAPIException):
            ecloud.networks.get(network.id)

    def test_network_nics(self, ecloud):
        """ Tests Network nics property. """
        network = create_network()
        assert isinstance(network.nics, list)

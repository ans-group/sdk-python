""" The SafeDNS implementation. """
from UKFastAPI.base import BaseApi
from UKFastAPI.SafeDNS import config
from UKFastAPI.SafeDNS.zone import ZoneManager, Zone
from UKFastAPI.SafeDNS.template import TemplateManager, Template
from UKFastAPI.SafeDNS.settings import Settings


class SafeDns(BaseApi):
    """ The base SafeDNS class, used to reach SafeDNS Zones and Templates. """

    def __init__(self, auth=None):
        super().__init__(auth)
        self._base = super()
        self._url = config.BASE_URL
        self.zones = ZoneManager(self._base, Zone, config.ZONE_URL)
        self.templates = TemplateManager(self._base, Template, config.TEMPLATE_URL)
        self.settings = Settings(self._base, config.SETTINGS_URL)

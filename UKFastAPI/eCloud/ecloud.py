""" eCloud implementation. """
from UKFastAPI.base import (BaseApi, IBareObject, ICreateable, IDeleteable,
                            IIdentifierOnlyManager, IGettable, IManagedObject,
                            IManager, IUpdateable, Actions, IObjectCreator)
from UKFastAPI.eCloud import config

# pylint:disable=too-few-public-methods,too-many-ancestors,too-many-instance-attributes


class eCloud(BaseApi):
    """ eCloud class representing the UKFast eCloud object. """

    def __init__(self, auth=None, version=2):
        super().__init__(auth)
        self._base = super()
        if version == 2:
            self.init_v2()
        if version == 1:
            self.init_v1()

    def init_v1(self):
        """ Initialises a v1 eCloud object. """
        self._url = config.BASE_V1_URL
        self.vms = VirtualMachineManager(self._base, VirtualMachine, config.VMS_URL)
        self.solutions = SolutionManager(self._base, Solution, config.SOLUTION_URL)
        self.sites = SiteManager(self._base, Site, config.SITE_URL)
        self.hosts = HostManager(self._base, Host, config.HOST_URL)
        self.datastores = DatastoreManager(self._base, Datastore, config.DATASTORES_URL)
        self.firewalls = FirewallManager(self._base, Firewall, config.FIREWALLS_URL)
        self.pods = PodManager(self._base, Pod, config.PODS_URL)
        self.credits = Credits(self._base, config.CREDITS_URL)
        self.appliances = ApplianceManager(self._base, Appliance, config.APPLIANCE_V1_URL)
        self.active_directory = ActiveDirectoryDomainManager(
            self._base, ActiveDirectoryDomain, config.ACTIVE_DIRECTORY_URL)

    def init_v2(self):
        """ Initialises a v2 eCloud object. """
        self._url = config.BASE_V2_URL
        self.vpcs = VirtualPrivateCloudManager(self._base, VirtualPrivateCloud, config.VPC_URL)
        self.networks = NetworkManager(self._base, Network, config.NETWORK_URL)
        self.dhcps = DhcpManager(self._base, Dhcp, config.DHCP_URL)
        self.instances = InstanceManager(self._base, Instance, config.INSTANCES_URL)
        self.floating_ips = FloatingIpManager(self._base, FloatingIp, config.FLOATING_IP_URL)
        self.firewall_rules = FirewallRuleManager(
            self._base, FirewallRule, config.FIREWALL_RULE_URL)
        self.firewall_policies = FirewallPolicyManager(
            self._base, FirewallPolicy, config.FIREWALL_POLICY_URL)
        self.firewall_rule_ports = FirewallRulePortManager(
            self._base, FirewallRulePort, config.FIREWALL_RULE_PORT_URL)
        self.regions = RegionManager(self._base, Region, config.REGIONS_URL)
        self.routers = RouterManager(self._base, Router, config.ROUTER_URL)
        self.nics = NicManager(self._base, Nic, config.NIC_URL)
        self.volumes = VolumeManager(self._base, Volume, config.VOLUME_URL)
        self.support = SupportManager(self._base, Support, config.SUPPORT_URL)
        self.billing_metrics = BillingMetricManager(
            self._base, BillingMetric, config.BILLING_METRIC_URL)
        self.appliances = ApplianceManager(self._base, Appliance, config.APPLIANCE_URL)
        self.availability_zones = AvailabilityZoneManager(
            self._base, AvailabilityZone, config.AVAILABILITY_ZONE_URL)


class Appliance(IManagedObject):
    """ Appliance class representing UKFast eCloud Appliance objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.parameters = ApplianceParameters(self._base, self._create_url('parameters'))


class ApplianceManager(IManager):
    """ Manager class for UKFast eCloud Appliance objects. """


class ApplianceParameters(IBareObject):
    """ Appliance Parameters class representing UKFast eCloud Appliance Parameter objects. """


class AvailabilityZone(IManagedObject):
    """ Class representing UKFast eCloud AvailabilityZone objects. """


class AvailabilityZoneManager(IManager):
    """ Manager class for UKFastCloud AvailabilityZoneManager object. """


class BillingMetric(IManagedObject):
    """ Class representing UKFast eCloud BillingMetric objects. """


class BillingMetricManager(IManager):
    """ Manager class for UKFastCloud BillingMetric object. """


class Credentials(IBareObject):
    """ Class representing UKFast eCloud Credentials objects. """


class Dhcp(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Dhcp objects. """


class DhcpManager(IManager, ICreateable):
    """ Manager class for UKFastCloud Dhcp object. """


class FloatingIp(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud FloatingIp objects. """

    def assign(self, **kwargs):
        """ Assign a NIC. """
        self. _action(Actions.POST, self._create_url('assign'), **kwargs)

    def unassign(self, **kwargs):
        """ Unassign a NIC. """
        self._action(Actions.POST, self._create_url('unassign'), **kwargs)


class FloatingIpManager(IManager, ICreateable):
    """ Manager class for UKFastCloud FloatingIp object. """


class FirewallPolicy(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud FirewallPolicy objects. """


class FirewallPolicyManager(IManager, ICreateable):
    """ Manager class for UKFastCloud FirewallPolicy object. """


class FirewallRule(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud FirewallRule objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.ports = IIdentifierOnlyManager(manager._base, self._create_url('ports')).list()


class FirewallRuleManager(IManager, ICreateable):
    """ Manager class for UKFastCloud FirewallRule object. """


class FirewallRulePort(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud FirewallRulePort objects. """


class FirewallRulePortManager(IManager, ICreateable):
    """ Manager class for UKFastCloud FirewallRulePort object. """


class Instance(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Instance objects. """
    # pylint:disable=protected-access

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.credentials = Credentials(self._base, self._create_url('credentials'))
        self.volumes = IIdentifierOnlyManager(manager._base, self._create_url('volumes')).list()
        self.nics = IIdentifierOnlyManager(manager._base, self._create_url('nics')).list()

    def power_on(self):
        """ Immediately powers on the instance. """
        self._base._action(Actions.PUT, self._create_url('power-on'))

    def power_off(self):
        """ Immediately powers off the instance. """
        self._base._action(Actions.PUT, self._create_url('power-off'))

    def power_reset(self):
        """ Resets power to the instance. """
        self._base._action(Actions.PUT, self._create_url('power-reset'))

    def power_shutdown(self):
        """ Attempt to gracefully shutdown the instance. """
        self._base._action(Actions.PUT, self._create_url('power-shutdown'))

    def power_restart(self):
        """ Attempt to gracefully restart the instance. """
        self._base._action(Actions.PUT, self._create_url('power-restart'))

    def lock(self):
        """ Lock an instance to changes. """
        self._base._action(Actions.PUT, self._create_url('lock'))

    def unlock(self):
        """ Unlock an instance to changes. """
        self._base._action(Actions.PUT, self._create_url('unlock'))


class InstanceManager(IManager, ICreateable):
    """ Manager class for UKFast eCloud Instance objects. """


class Network(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Network objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.nics = IIdentifierOnlyManager(manager._base, self._create_url('nics')).list()


class NetworkManager(IManager, ICreateable):
    """ Manager class for UKFast eCloud Network objects. """


class Nic(IManagedObject):
    """ Class representing UKFast eCloud Nic objects. """


class NicManager(IManager):
    """ Manager class for UKFast eCloud Nic objects. """


class Region(IManagedObject):
    """ Class representing UKFast eCloud Region objects. """


class RegionManager(IManager):
    """ Manager class for UKFast eCloud Instance objects. """


class Router(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Router objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.firewall_rules = IIdentifierOnlyManager(
            manager._base, self._create_url('firewall-rules'))
        self.networks = IIdentifierOnlyManager(manager._base, self._create_url('networks'))
        self.vpns = IIdentifierOnlyManager(manager._base, self._create_url('vpns'))

    def configure_default_policies(self, **kwargs):
        """ Configure the default firewall policies for the router. """
        # pylint:disable=protected-access
        self._base._action(Actions.POST, self._create_url('configure-default-policies'), **kwargs)


class RouterManager(IManager, ICreateable):
    """ Manager class for UKFast eCloud Router objects. """


class Support(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Support objects. """


class SupportManager(IManager, ICreateable):
    """ Manager class for UKFast eCloud Support objects. """


class Volume(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Volume objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.instances = IIdentifierOnlyManager(manager._base, self._create_url('instances'))


class VolumeManager(IManager, IGettable):
    """ Manager class for UKFast eCloud Volume objects. """


class VirtualPrivateCloud(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud VirtualPrivateCloud objects. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.volumes = IIdentifierOnlyManager(manager._base, self._create_url('volumes')).list()
        self.instances = IIdentifierOnlyManager(manager._base, self._create_url('instances')).list()

    def deploy_defaults(self, **kwargs):
        """ Deploy the VirtualPrivateCloud defaults. """
        # pylint:disable=protected-access
        self._base._action(Actions.POST, self._create_url('deploy-defaults'), **kwargs)


class VirtualPrivateCloudManager(IManager, ICreateable):
    """ Manager class for UKFast eCloud VirtualPrivateCloud objects. """


# ============= V1 STUFF =============
class VirtualMachine(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud VirtualManchine object. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.tags = TagManager(manager._base, Tag, self._create_url('tags'))

    def clone(self, **kwargs):
        """ Clone a Virtual Machine. """
        # pylint:disable=protected-access
        data = self._action(Actions.POST, config.CLONE_URL, **kwargs)
        return IObjectCreator._create_object(self, data)

    def clone_to_template(self, **kwargs):
        """ Create a template with the exact specifications as a specified virtual machine. """
        self._action(Actions.POST, config.CLONE_TEMPLATE_URL, **kwargs)

    def power_on(self, **kwargs):
        """ Power on the virtual machine. """
        self._action(Actions.PUT, config.POWER_ON_URL, **kwargs)

    def power_off(self, **kwargs):
        """ Power off the virtual machine. """
        self._action(Actions.PUT, config.POWER_OFF_URL, **kwargs)

    def power_reset(self, **kwargs):
        """ Power off the virtual machine then power on. """
        self._action(Actions.PUT, config.POWER_RESET_URL, **kwargs)

    def power_shutdown(self, **kwargs):
        """ Shut down the virtual machine. """
        self._action(Actions.PUT, config.POWER_SHUTDOWN_URL, **kwargs)

    def power_restart(self, **kwargs):
        """ Shut down the virtual machine then power on. """
        self._action(Actions.PUT, config.POWER_RESTART_URL, **kwargs)


class VirtualMachineManager(IManager, ICreateable):
    """ Manager class for VirtualMachine objects. """


class Solution(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Solution object. """

    def __init__(self, manager, data):
        super().__init__(manager, data)

        self.vms = IIdentifierOnlyManager(manager._base, self._create_url('vms')).list()
        self.hosts = IIdentifierOnlyManager(manager._base, self._create_url('hosts')).list()
        self.datastores = IIdentifierOnlyManager(
            manager._base, self._create_url('datastores')).list()
        self.sites = IIdentifierOnlyManager(manager._base, self._create_url('sites')).list()
        self.networks = IIdentifierOnlyManager(manager._base, self._create_url('networks')).list()
        self.firewalls = IIdentifierOnlyManager(manager._base, self._create_url('firewalls')).list()

        self.tags = TagManager(manager._base, Tag, self._create_url('tags'))
        self.templates = TemplateManager(manager._base, Template, self._create_url('templates'))


class SolutionManager(IManager, ICreateable):
    """ Manager class for Solution objects. """


class Tag(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Tag object. """
    _identifier = 'key'


class TagManager(IManager, ICreateable):
    """ Manager class for Tag objects. """

    def create(self, **kwargs):
        self._create(self._url, **kwargs)
        return super()._get(super()._create_url(kwargs.get('key')))


class Template(IManagedObject, IDeleteable):
    """ Class representing UKFast eCloud Template object. """
    _identifier = 'name'


class TemplateManager(IManager):
    """ Manager class for Template objects. """


class Site(IManagedObject):
    """ Class representing UKFast eCloud Site object. """


class SiteManager(IManager):
    """ Manager class for Site objects. """


class Host(IManagedObject):
    """ Class representing UKFast eCloud Host object. """


class HostManager(IManager):
    """ Manager class for Host objects. """


class Datastore(IManagedObject):
    """ Class representing UKFast eCloud Datastore object. """


class DatastoreManager(IManager):
    """ Manager class for Datastore objects. """


class Firewall(IManagedObject):
    """ Class representing UKFast eCloud Firewall object. """

    def __init__(self, manager, data):
        super().__init__(manager, data)
        self.config = IIdentifierOnlyManager(manager._base, self._create_url('config')).list()


class FirewallManager(IManager):
    """ Manager class for Firewall objects. """


class Pod(IManagedObject, IUpdateable, IDeleteable):
    """ Class representing UKFast eCloud Pod object. """

    def __init__(self, manager, data):
        super().__init__(manager, data)

        self.appliances = IIdentifierOnlyManager(
            manager._base, self._create_url('appliances')).list()
        self.gpu_profiles = GpuProfileManager(
            manager._base, GpuProfile, self._create_url('gpu-profiles'))
        self.templates = TemplateManager(manager._base, Template, self._create_url('templates'))


class PodManager(IManager):
    """ Manager class for Pod objects. """


class Credits(IBareObject):
    """ Class representing UKFast eCloud Credits object. """


class ActiveDirectoryDomain(IManagedObject):
    """ Class representing UKFast eCloud ActiveDirectory object. """


class ActiveDirectoryDomainManager(IManager):
    """ Manager class for ActiveDirectory objects. """


class GpuProfile(IManagedObject):
    """ Class representing UKFast eCloud GpuProfile object. """


class GpuProfileManager(IManager):
    """ Manager class for GpuProfile objects. """

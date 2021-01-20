""" eCloud config values. """

ECLOUD_AUTH = 'BILLING_AUTH'
BASE_V2_URL = '/ecloud/v2'
BASE_V1_URL = '/ecloud/v1'

INSTANCES_URL = BASE_V2_URL + '/instances'
REGIONS_URL = BASE_V2_URL + '/regions'
# APPLIANCE_URL = BASE_V2_URL + '/appliances'
APPLIANCE_URL = '/ecloud/v1/appliances'
VPC_URL = BASE_V2_URL + '/vpcs'
ROUTER_URL = BASE_V2_URL + '/routers'
AVAILABILITY_ZONE_URL = BASE_V2_URL + '/availability-zones'
NETWORK_URL = BASE_V2_URL + '/networks'
DHCP_URL = BASE_V2_URL + '/dhcps'
FLOATING_IP_URL = BASE_V2_URL + '/floating-ips'
FIREWALL_RULE_URL = BASE_V2_URL + '/firewall-rules'
FIREWALL_POLICY_URL = BASE_V2_URL + '/firewall-policies'
FIREWALL_RULE_PORT_URL = BASE_V2_URL + '/firewall-rule-ports'
NIC_URL = BASE_V2_URL + '/nics'
VOLUME_URL = BASE_V2_URL + '/volumes'
SUPPORT_URL = BASE_V2_URL + '/support'
BILLING_METRIC_URL = BASE_V2_URL + '/billing-metrics'


VMS_URL = BASE_V1_URL + '/vms'  # OLD
CLONE_URL = '/clone'  # OLD
CLONE_TEMPLATE_URL = '/clone-to-template'  # OLD
POWER_ON_URL = '/power-on'  # OLD
POWER_OFF_URL = '/power-off'  # OLD
POWER_RESET_URL = '/power-reset'  # OLD
POWER_SHUTDOWN_URL = '/power-shutdown'  # OLD
POWER_RESTART_URL = '/power-restart'  # OLD

SOLUTION_URL = BASE_V1_URL + '/solutions'
SITE_URL = BASE_V1_URL + '/sites'
HOST_URL = BASE_V1_URL + '/hosts'
DATASTORES_URL = BASE_V1_URL + '/datastores'
FIREWALLS_URL = BASE_V1_URL + '/firewalls'
PODS_URL = BASE_V1_URL + '/pods'
CREDITS_URL = BASE_V1_URL + '/credits'
APPLIANCE_V1_URL = BASE_V1_URL + '/appliances'
ACTIVE_DIRECTORY_URL = BASE_V1_URL + '/active-directory/domains'

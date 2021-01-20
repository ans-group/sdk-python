""" Config values for testing. """
TEST_CPU = 1
TEST_RAM = 1024
TEST_RAM_V1 = 1
TEST_HDD = 20
TEST_POD_ID = 14
TEST_ENVIRONMENT = 'Public'
# TEST_ENVIRONMENT = 'Private'

TEST_APPLIANCE_ID = '628fba2b-2336-4ecb-9bf3-befe46b87798'
TEST_REGION_ID = 'reg-b49ar89h'
TEST_ROUTER_NAME = 'test router'
TEST_NETWORK_NAME = 'test network'
TEST_SUBNET = '10.8.0.0/24'
TEST_VPC_NAME = 'test vpc'
TEST_POLICY_SEQUENCE = 1
TEST_RULE_SOURCE = '1.1.1.1'
TEST_RULE_DEST = '2.2.2.2'
TEST_RULE_ACTION = 'ALLOW'
TEST_RULE_DIRECTION = 'IN_OUT'
TEST_RULE_PROTOCOL = 'TCP'

TEST_TAG_KEY = 'key1'
TEST_TAG_VALUE = 'value1'

# The amount of seconds we will wait for a VM status to
# change to 'Complete' before failing the test.
BUFFER_TIME = 240

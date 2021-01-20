""" SafeDNS config values """

SAFEDNS_AUTH = 'SAFEDNS_AUTH'
BASE_URL = '/safedns/v1'
ZONE_URL = BASE_URL + '/zones'
TEMPLATE_URL = BASE_URL + '/templates'
RECORD_URL = ZONE_URL + '/{}/records'
TEMPLATE_RECORD_URL = TEMPLATE_URL + '/{}/records'
NOTE_URL = ZONE_URL + '/{}/notes'
SETTINGS_URL = BASE_URL + '/settings'

MAX_TEMPLATE_NAME = 255
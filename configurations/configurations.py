import configparser
import os

from . import secrets

global credential, debugger_credential, agency_client_credential


def load_config_by_usertype(user_type='admin'):
    global credential, debugger_credential, agency_client_credential
    if "JENKINS_URL" in os.environ:
        credential = secrets.get_credential_by_user_type(user_type)
        debugger_credential = secrets.get_debugger_credential()
        agency_client_credential = secrets.get_credential_by_user_type('agency-client')
    config = configparser.RawConfigParser()
    config.read(['global.ini', 'local.ini', 'local_generated.ini'])
    if "JENKINS_URL" in os.environ:
        for key in credential.keys():
            config['credential'][key.replace('_', '-')] = \
                credential[key]
        for key_2 in debugger_credential.keys():
            if (key_2 == "debugging_password") or (key_2 == "debugging_username"):
                config['debugger_credentials'][key_2.replace('_', '-')] = debugger_credential[key_2]
        for key_3 in agency_client_credential.keys():
            config['credential']['agency-client-' + key_3.replace('_', '-')] = \
                agency_client_credential[key_3]
    return config

import os
import time
from functools import lru_cache

import hvac
import pymysql
from sshtunnel import SSHTunnelForwarder

from configurations import configurations, generic_modules

config = configurations.load_config_by_usertype()

ssh_service = None


def is_jenkins():
    return os.environ.get('JENKINS_HOME') is not None


def set_tunnel(service):
    global ssh_service
    ssh_service = SSHTunnelForwarder(
        config['mysql-hosts']['ssh-host'],
        ssh_username=config['mysql']['ssh-user'],
        remote_bind_address=(
            config['mysql-hosts']['{}'.format(service)], 3306)
    )
    ssh_service.start()
    print('Setting up SSH tunnel on port {}'.format(
        ssh_service.local_bind_port))
    return ssh_service.local_bind_port


def destroy_tunnel():
    global ssh_service
    ssh_service.stop()


def connection_test(connection):
    connected = False
    try:
        with connection.cursor() as cursor:
            sql_select_query = 'SELECT VERSION()'
            cursor.execute(sql_select_query)
            connection.commit()
            result = cursor.fetchone()
            if len(result.keys()):
                print('Connection Success')
                connected = True
                return connected
    except Exception as e:
        return connected


@lru_cache(maxsize=1)
def mysql_connection_test():
    stage = connection_test(get_mysql_client())
    return stage


@lru_cache(maxsize=1)
def get_mysql_credentials(audiences_db=False):
    if "JENKINS_URL" in os.environ:
        client = hvac.Client(url=config['vault']['url'])
        client.auth.approle.login(os.environ['APPROLE_ROLE_ID'], os.environ['APPROLE_SECRET_ID'])
        if audiences_db:
            secret_version_response = client.secrets.kv.v2.read_secret_version(
                mount_point=config['vault']['mount-point'],
                path=config['vault']['audiences_mysql_path'],
            )
            mysql_credentials = {
                'username': secret_version_response['data']['data']['user_name'],
                'password': secret_version_response['data']['data']['user_pass']
            }
        else:
            secret_version_response = client.secrets.kv.v2.read_secret_version(
                mount_point=config['vault']['mount-point'],
                path=config['vault']['mysql-path'],
            )
            mysql_credentials = {
                'username': secret_version_response['data']['data']['user_name'],
                'password': secret_version_response['data']['data']['user_pass']
            }
    else:
        if audiences_db:
            mysql_credentials = {
                'username': config['mysql_credentials_audiences_db']['username'],
                'password': config['mysql_credentials_audiences_db']['password']
            }
        else:
            mysql_credentials = {
                'username': config['mysql_credentials']['username'],
                'password': config['mysql_credentials']['password']
            }
    return mysql_credentials


def get_mysql_client():
    mysql_credentials = get_mysql_credentials()
    connection = pymysql.connect(
        host=config['mysql-hosts']['stage-mysql-host'],
        user=mysql_credentials['username'],
        password=mysql_credentials['password'],
        db=config['mysql']['db'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_mysql_client_for_audiences_db():
    mysql_credentials = get_mysql_credentials(audiences_db=True)
    connection = pymysql.connect(host=config['mysql-hosts']['audiences-master-mysql-host'],
                                 user=mysql_credentials['username'],
                                 password=mysql_credentials['password'],
                                 db=config['mysql']['audiences_db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

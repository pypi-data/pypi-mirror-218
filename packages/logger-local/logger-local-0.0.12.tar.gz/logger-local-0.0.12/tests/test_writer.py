# TODO: Should convert this file to Python Unit Test
import pymysql
import os

import sys
package_dir = "."
sys.path.append(package_dir)

# TODO: This is too long, let's shorten it.
from LoggerLocalPythonPackage.MessageSeverity import MessageSeverity
from Local_Logger import Local_Logger
import pytest
locallgr=Local_Logger()
ID = 5000001
# ID = 1

# Connect to the datbaase to validat that the log was inserted
def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        host=os.getenv('RDS_HOSTNAME'),
        database='logger' #os.getenv('RDS_DB_NAME')
    )
@pytest.mark.test
def test_log():
    object_to_insert_1 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 33,
        'longitude': 35,
        'user_id': ID,
        'profile_id': ID,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'log from python -object_1',
        'component_id': ID,
        'variable_id': ID,
        'variable_value_old': 'variable_value_old-python',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
    }
    locallgr.info(object=object_to_insert_1)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_1['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value
@pytest.mark.test
def test_error():
    object_to_insert_2 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 33,
        'longitude': 35,
        'user_id': ID,
        'profile_id': ID,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'payload from python -object_2',
        'component_id': ID,
    }
    locallgr.error(object=object_to_insert_2)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_2['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
@pytest.mark.test
def test_verbose():
    object_to_insert_3 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 33,
        'longitude': 35,
        'variable_id': ID,
        'variable_value_old': 'variable_value_old-python-object_3',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
    }
    locallgr.verbose(object=object_to_insert_3)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE variable_value_old = '{object_to_insert_3['variable_value_old']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Verbose.value
@pytest.mark.test
def test_warn():
    object_to_insert_4 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 33,
        'longitude': 35,
        'user_id': ID,
        'profile_id': ID,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'payload from python -object_4',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
    }
    locallgr.warn(object=object_to_insert_4)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_4['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Warning.value
@pytest.mark.test
def test_add_message():
    # option to insert only message
    message = 'only message error from python'
    locallgr.error(message)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{message}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
@pytest.mark.test
def test_debug():
    object_to_insert_5 = {
        'payload': 'just payload & activity_id - python',
        'activity_id': ID
    }
    locallgr.debug(object=object_to_insert_5)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_5['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Debug.value

if __name__ == "__main__":
    test_log()
    test_error()
    test_verbose()
    test_add_message()
    test_warn()
    test_debug()





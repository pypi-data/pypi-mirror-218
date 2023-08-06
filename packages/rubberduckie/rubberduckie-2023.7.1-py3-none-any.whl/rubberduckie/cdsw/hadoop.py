import os
import warnings
from impala.dbapi import connect
from impala.util import as_pandas

DEBUG = True
if DEBUG:
    print('DB tools are loaded!')


def prepare_connection(host: str):
    """Prepare connection to IDP (Hadoop) in CDSW
    Colin Li @ 2023-05
    Args:
        host (str): "impala" or "hive"

    Returns:
        impala.dbapi.connect: connection to IDP
    """
    CONN = None
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            if host == 'impala':
                CONN = connect(
                    host=os.getenv('IMPALA_HOST'),
                    port=os.getenv('IMPALA_PORT'),
                    database='default',
                    use_ssl=True,
                    ca_cert=None,
                    auth_mechanism='GSSAPI',
                    user='impala',
                    password='',
                    kerberos_service_name='impala')
            elif host == 'hive':
                CONN = connect(
                    host=os.getenv('HIVE_HOST'),
                    port=os.getenv('HIVE_PORT'),
                    database='default',
                    use_ssl=True,
                    ca_cert=None,
                    auth_mechanism='GSSAPI',
                    user='hive',
                    password='',
                    kerberos_service_name='hive')
    except TypeError:
        warnings.warn("Update password for Hadoop Authentication in CDSW!")
        warnings.warn("Run this in CDSW ONLY!")
        return None
    return CONN


def execute_db_query(conn, query: str):
    """Execute databass query
    Colin Li @ 2023-05
    Args:
        conn (impala.dbapi.connect): connection
        query (str): can be either a string (query) or file path of a sql file
    """
    if os.path.isfile(query) and query[-4:] == '.sql':
        query_path = query
        with open(query_path, 'r') as f:
            query = f.read()
        print(f'Executing task {query_path}')
    tasks = query.split(';')
    for i, t in enumerate(tasks):
        if t.replace(' ', '').replace('\n', '') == '':
            continue
        else:
            print(f'Executing subtask {i+1}')
            cursor = conn.cursor()
            cursor.execute(t)
    print(f'Task is completed!')


def extract_db_data(conn, query: str):
    """Extract data from database as pandas dataframe
    Colin Li @ 2023-05

    Args:
        conn (impala.dbapi.connect): connection
        query (str): can be either a string (query) or file path of a sql file

    Returns:
        pandas.DataFrame: Pandas dataframe containing database data
    """
    if os.path.isfile(query) and query[-4:] == '.sql':
        query_path = query
        with open(query_path, 'r') as f:
            query = f.read()
        print(f'Executing task {query_path}')
    cursor = conn.cursor()
    cursor.execute(query)
    df = as_pandas(cursor)
    return df


if __name__ == "__main__":
    pass

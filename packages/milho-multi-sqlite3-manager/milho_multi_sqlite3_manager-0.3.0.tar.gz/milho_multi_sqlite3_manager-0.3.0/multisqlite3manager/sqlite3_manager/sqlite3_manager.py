import sqlalchemy
import dataclasses
import sqlglot
import os 
import glob
import pandas
import typing
import pandas as pd

MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY = "MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH"
MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT = os.getenv(MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY)

@dataclasses.dataclass
class _Database:
    """
        A class to represent a database.
        :param db_name: The database name.
        :param filename: The database filename.
    """
    db_name: str
    filename: str

@dataclasses.dataclass
class _Sqlite3Wrapper:
    """
        A class to represent a wrapper of various sqlite3 databases.
        :param databases: A list of _Database objects.
        :param database_folder_path: The path of the folder that stores the database files
    """
    databases: list[_Database]
    database_folder_path: str

def _create_sqlite3_wrapper(database_folder_path: str) -> _Sqlite3Wrapper:
    """
        Create a _Sqlite3Wrapper object.
        :param database_folder_path: The folder path where the sqlite3 database files are located.
        :return: A _Sqlite3Wrapper object.
    """

    if not os.path.isdir(database_folder_path):
        raise NotADirectoryError(f"The folder path {database_folder_path} is not a directory.")

    files = glob.glob(f'{database_folder_path}/*') 
    files = [file for file in files if os.path.isfile(file)]

    if len(files) == 0:
        raise FileNotFoundError(f"The folder path {database_folder_path} does not contain any sqlite3 database file.")

    databases = []

    for file in files:
        db_name, _ = os.path.splitext(os.path.basename(file))
        databases.append(_Database(db_name, file))

    return _Sqlite3Wrapper(databases, database_folder_path)

def _create_connection_with_attached_databases(databases: typing.List[_Database]) -> sqlalchemy.engine.base.Connection:
    """
        Create a connection with attached databases.
        :param databases: A list of _Database objects.
        :return: A sqlalchemy.engine.base.Engine object.
    """

    from sqlalchemy import text
    
    if len(databases) == 0:
        raise ValueError("The databases list is empty.")

    engine = sqlalchemy.create_engine('sqlite://', echo=False)

    conn = engine.connect()
    for db in databases:
        conn.execute(text(f"ATTACH DATABASE '{db.filename}' AS {db.db_name};"))

    return conn

def _get_databases_name_from_sql_stmt(sql: str) -> list[str]:
    """
        Get all databases names from a sql statement.
        :param sql: The sql statement.
        :return: A list of databases names.
    """

    tables = [x for x in sqlglot.parse_one(sql).find_all(sqlglot.exp.Table)]
    parts = [str(x).split('.') for x in tables]
    dbs = [x[0] for x in parts if len(x) > 1]

    return dbs

def _validate_folder_path(folder_path: str):
    """
        Validate the folder path
        :param folder_path: The folder path where the sqlite3 database files are located.
    """
    if folder_path == None and MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT == None:
        return False
    
    if folder_path != None and not os.path.isdir(folder_path):
        return False

    return True

   

def load_dataframe_in_memory(dataframes: dict[str, pd.DataFrame]) -> sqlalchemy.engine.base.Connection:
    """
        Load a list of dataframes in a sqlite3 database in memory.
        :param dataframes: A list of dict with the dataframe name and the dataframe.
        :param database_name: The database name.
        :return: A sqlalchemy.engine.base.Connection object.
    """

    engine = sqlalchemy.create_engine('sqlite://', echo=False)

    conn = engine.connect()
    for df_name, df in dataframes.items():
        df.to_sql(df_name, conn, index=False, if_exists="replace")

    return conn

def load_dataframe_in_disk(dataframes: dict[str, pd.DataFrame], database_name: str, folder_path: str = MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT) -> sqlalchemy.engine.base.Connection:
    """
        Load a list of dataframes in a sqlite3 database in disk.
        :param dataframes: A list of dict with the dataframe name and the dataframe.
        :param database_name: The database name.
        :param folder_path: The folder path where the sqlite3 database files are located.
        :return: A sqlalchemy.engine.base.Engine object.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY}")

    engine = sqlalchemy.create_engine(f'sqlite:///{folder_path}/{database_name}.db', echo=False)

    conn = engine.connect()
    for df_name, df in dataframes.items():
        df.to_sql(df_name, conn, index=False, if_exists="replace" )

    return conn

def create_connection_in_memory() -> sqlalchemy.engine.base.Connection:
    """
        Create a connection in a sqlite3 database in memory.
        :return: A sqlalchemy.engine.base.Connection object.
    """

    engine = sqlalchemy.create_engine('sqlite://', echo=False)
    conn = engine.connect()

    return conn

def from_sql_to_dataframe(sql: str, database_connection: sqlalchemy.engine.base.Connection = None, folder_path: str = MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT) -> pandas.DataFrame:
    """
        Execute a sql statement in all sqlite3 database files in the folder_path. Attach all databases in the SQL to the connection and execute the sql statement.
        If databae_connections is not None, the sql statement will be executed ONLY in the databases in the database_connections list.
        :param folder_path: A dataframe with the result of the sql statement.
        :param database_connection: A sqlalchemy.engine.base.Connection object
        :param folder_path: The folder path where the sqlite3 database files are located.
        :return: A pandas.DataFrame object.
    """

    if database_connection != None:
        return pandas.read_sql(sql, database_connection)
        
    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY}")
    
    stmt_dbs = _get_databases_name_from_sql_stmt(sql)
    env_manager = _create_sqlite3_wrapper(folder_path)
    storage_env_databases = [x.db_name for x in env_manager.databases]

    if len(stmt_dbs) == 0:
        raise ValueError("The sql statement does not contain any database name.")

    for db in stmt_dbs:
        if db not in storage_env_databases:
            raise ValueError(f"The database {db} does not exist in the storage environment.")
        
    databases = [x for x in env_manager.databases if x.db_name in stmt_dbs]

    conn = _create_connection_with_attached_databases(databases)

    return pandas.read_sql(sql, conn)

def create_connection(databases: typing.List[str], folder_path: str = MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT) -> sqlalchemy.engine.base.Connection:
    """
        Create a connection with attached databases.
        :param databases: A list of databases names.
        :param folder_path: The folder path where the sqlite3 database files are located.
        :return: A sqlalchemy.engine.base.Connection object.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY}")

    env_manager = _create_sqlite3_wrapper(folder_path)
    storage_env_databases = [x.db_name for x in env_manager.databases]

    if len(databases) == 0:
        raise ValueError("The databases list is empty.")

    for db in databases:
        if db not in storage_env_databases:
            raise ValueError(f"The database {db} does not exist in the storage environment.")

    dbs = [x for x in env_manager.databases if x.db_name in databases]

    return _create_connection_with_attached_databases(dbs)

def print_databases(folder_path: str = MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT):
    """
        Print all databases in the folder_path.
        :param folder_path: The folder path where the sqlite3 database files are located.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY}")

    env_manager = _create_sqlite3_wrapper(folder_path)

    for db in env_manager.databases:
        print('-> ', db.db_name, ' - ', db.filename)

def print_tables(database_name: str, folder_path: str = MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT):
    """
        Print all tables in the database.
        :param database: The database name.
        :param folder_path: The folder path where the sqlite3 database files are located.
    """
    from sqlalchemy import text

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_KEY}")

    env_manager = _create_sqlite3_wrapper(folder_path)

    if database_name not in [x.db_name for x in env_manager.databases]:
        raise ValueError(f"The database {database_name} does not exist in the storage environment.")

    conn = _create_connection_with_attached_databases([x for x in env_manager.databases if x.db_name == database_name])

    tables = conn.execute(text(f"SELECT name FROM {database_name}.sqlite_master WHERE type='table';"))
    for table in tables:
        print('-> ', database_name, ' - ', table[0])
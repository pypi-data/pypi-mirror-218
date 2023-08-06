import unittest
import pandas as pd
import sqlite3_manager
import sqlalchemy
import os
import sqlite3

class TestSqlite3Manager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database_folder_path = sqlite3_manager.MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT
        """The folder path where the sqlite3 database files are located."""

        cls.list_of_databases_objects = [
            sqlite3_manager._Database('test_db', os.path.join(sqlite3_manager.MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT, 'test_db.db')),
            sqlite3_manager._Database('test_db_2', os.path.join(sqlite3_manager.MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT,'test_db_2.db'))
        ]
        """A list of _Database objects."""

        # Create a folder to store the test databases with the MULTISQLITE3MANAGER_SQLITE_FOLDER_PATH_DEFAULT directory, create all list_of_databases_objects databases and populate with a table called 'table'
        
        # Create the folder, if it doesn't exist
        if not os.path.isdir(cls.database_folder_path):
            os.mkdir(cls.database_folder_path)

        for db in cls.list_of_databases_objects:
            if os.path.isfile(db.filename):
                os.remove(db.filename)

            conn = sqlite3.connect(db.filename)
            cur = conn.cursor()
            cur.execute("CREATE TABLE table_test (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);")
            cur.execute("INSERT INTO table_test VALUES (1, 'John', 20);")
            cur.execute("INSERT INTO table_test VALUES (2, 'Mary', 30);")
            cur.execute("INSERT INTO table_test VALUES (3, 'Peter', 40);")
            conn.commit()
            conn.close()

    def test_create_sqlite3_wrapper(self):
        """
            Test the _create_sqlite3_wrapper function. This test create a _Sqlite3Wrapper object and then check if the returned object is a _Sqlite3Wrapper object
        """
        wrapper = sqlite3_manager._create_sqlite3_wrapper(self.database_folder_path)
        self.assertIsInstance(wrapper, sqlite3_manager._Sqlite3Wrapper)

    def test_create_connection_with_attached_databases(self):
        """
            Test the _create_connection_with_attached_databases function creating a connection with attached databases. This test create a connection with attached databases and then check if the returned object is a sqlalchemy.engine.base.Connection object
        """

        with sqlite3_manager._create_connection_with_attached_databases(self.list_of_databases_objects) as conn: 
            self.assertIsInstance(conn, sqlalchemy.engine.base.Connection)
        

    def test_get_databases_name_from_sql_stmt(self):
        """
            Test the _get_databases_name_from_sql_stmt function returning a list of databases name used in a sql statement
        """

        sql = "SELECT * FROM test_db.table"
        dbs = sqlite3_manager._get_databases_name_from_sql_stmt(sql)
        self.assertEqual(dbs, ['test_db'])

    def test_validate_folder_path(self):
        """
            Test the _validate_folder_path function validating a folder path. If the param is a directory it returns True, otherwise it returns False
        """
        self.assertTrue(sqlite3_manager._validate_folder_path(self.database_folder_path))

    def test_load_dataframe_in_memory(self):
        """
            Test the load_dataframe_in_memory function. This test load a Dataframe in a memory connection and then read the Dataframe from the database, 
            comparing the original Dataframe with the Dataframe read from the database
        """

        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        with sqlite3_manager.load_dataframe_in_memory({'test_df': df}) as conn:
            returned_df = pd.read_sql('SELECT * FROM test_df', conn)

            self.assertIsInstance(conn, sqlalchemy.engine.base.Connection)
            self.assertTrue(df.equals(returned_df))
            
    def test_load_dataframe_in_disk(self):
        """
            Test the load_dataframe_in_disk function. This test load a Dataframe in a disk connection and then read the Dataframe from the database,
            comparing the original Dataframe with the Dataframe read from the database
        """
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        with sqlite3_manager.load_dataframe_in_disk({'test_df': df}, 'test_db') as conn:
            returned_df = pd.read_sql('SELECT * FROM test_df', conn)

            self.assertIsInstance(conn, sqlalchemy.engine.base.Connection)
            self.assertTrue(df.equals(returned_df))


    def test_create_connection_in_memory(self):
        """
            Test the create_connection_in_memory function. This test create a connection in memory and then check if the connection is a sqlalchemy.engine.base.Connection object
        """
        with sqlite3_manager.create_connection_in_memory() as conn:
            self.assertIsInstance(conn, sqlalchemy.engine.base.Connection)


    def test_from_sql_to_dataframe(self):
        """
            Test the from_sql_to_dataframe function. This test execute a sql statement and then check if the returned object is a pandas.DataFrame object
        """
        sql = "SELECT * FROM test_db.table_test"
        df = sqlite3_manager.from_sql_to_dataframe(sql)
        self.assertIsInstance(df, pd.DataFrame)

    def test_create_connection(self):
        """
            Test the create_connection function. This test create a connection and then check if the returned object is a sqlalchemy.engine.base.Connection object
        """
        with sqlite3_manager.create_connection(['test_db'], self.database_folder_path) as conn:
            self.assertIsInstance(conn, sqlalchemy.engine.base.Connection)

    def test_print_databases(self):
        """
            Test the print_databases function. This function prints to stdout, so it's a bitharder to test. You might not need to test this function.
        """
        sqlite3_manager.print_databases()

    def test_print_tables(self):
        """
            Test the print_tables function. This function prints to stdout, so it's a bitharder to test. You might not need to test this function.
        """
        sqlite3_manager.print_tables('test_db')

if __name__ == '__main__':
    unittest.main(verbosity=2)

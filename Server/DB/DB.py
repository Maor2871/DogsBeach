# -*- coding: utf-8 -*-
import sqlite3 as lite


class DB():

    """
        This class is responsible on anything relates to the server's data base.
    """

    def __init__(self, name, user, password, host="127.0.0.1", port=23):

        """The function receives the data base name, user, password, host and port.
        The function create an object which offers an access to the data base (w/r).
        The function does not return parameters."""

        self.name = name

        self.user = user

        self.password = password

        self.host = host

        self.port = port

        # The data base connection handle.
        self.db = None

        # The instance which returned when connecting to the data base.
        self.connector = None

        # The cursor of the data base.
        self.cursor = None

    def connect(self, db_name):

        """
            The function receives db_name.
            The function connects to the data base.
        """

        # Connect the data base.
        self.connector = lite.connect(db_name + ".db")

        # Get the cursor to the data base.
        self.cursor = self.connector.cursor()

    def create_table(self, table_name, columns):

        """
            The function creates new table in the data base. In addition, it inserts the columns and their types to the
            table. columns is as follow: [[column_name, type]...]
        """

        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + "(" +
                            ', '.join(rubric[0] + " " + rubric[1] for rubric in columns) + ");")

        self.connector.commit()

    def insert(self, table_name, values):
        """
            The function receives a name of a table, and a list of the values of the new row by the order of the columns
            in the table.
        """

        self.cursor.execute('INSERT INTO ' + table_name + ' VALUES(' + '"' + ('"' + ", " + '"').join(values) + '"' +
                            ');')

        self.connector.commit()

    def select(self, table_name, columns, condition):

        """The function select data from the data base respectively to the condition it get and than it returns this
        data."""

        if columns[0] != "*":

            selection = self.cursor.execute('SELECT (' + ', '.join(columns) + ') FROM ' + table_name + condition + ';')

        else:

            selection = self.cursor.execute('SELECT * FROM ' + table_name + condition + ';')

        return selection

    def remove(self, table_name, condition):

        """
            The function removes rows from the received table according to the condition.
        """

        self.cursor.execute('DELETE FROM ' + table_name + condition + ';')

        self.connector.commit()


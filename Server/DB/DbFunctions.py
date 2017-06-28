__author__ = 'talmid'
from Thread import Thread
from DB import DB


class DbFunctions(Thread):

    """represent a bunch of functions that are use the data base.
    in this thread the data base will be created and the thread will wait for server requests to use the data base."""

    def __init__(self):

        """The function create a db functions instance.
        The function does not return parameters."""

        Thread.__init__(self, 5, "DbFunctions")

        self.asks = []

        #flag that sign if there is duplicates of the user name it get or not

        self.user_name_duplicates_flags = {}

    def manager(self):

        """The function does not receive or return parameters.
        The thread wait for server asks to use the data base."""

        self.db = DB('users and lessons', "yuval", "19hothot")

        self.connect("'users and lessons'")

        self.build_data_base()

        while True:

            for ask in self.asks:

                if ask[0] == "register me":

                    print 'got to db functions'

                    self.add_user(ask[1])

                elif ask[0] == "check user name duplicates":

                    self.check_username_duplicates(ask[1], ask[2])
					
				elif ask[0] == "give me his details":
				
					self.select_details()

            self.asks = []

    def add_to_db(self, table_name, values):

        """The function receive an table name and a list of values.
        The function add this values as a row in the table name."""

        self.db.insert(table_name, values)

    def add_user(self, values):

        """The function get user values and insert them to the data base."""

        self.add_to_db("STUDENTS", values)

    def check_select_results_exists(self, results):

        """The function check select results and return True if they are exists, elsewhere return False."""

        is_exist = False

        for row in results:

            is_exist = True

        return is_exist

    def check_username_duplicates(self, username, communicator):

        """The function receives a username.
        The function check if this user name is used by another user and return True if it is.
        Elsewhere, the function return False."""

        condition = [["Username", username]]

        #if the select is None it return False - because there is no user name duplicates, elsewhere it return True

        print "welcome to check username duplicates station"

        if self.check_select_results_exists(self.db.select("STUDENTS", ["Username"], self.convert_condition(condition))):

            self.user_name_duplicates_flags[communicator] = True

        else:

            self.user_name_duplicates_flags[communicator] = False

    def connect(self, name):

        """The function connect between the db it create and the thread and give him a name it get."""

        self.db.connect(name)

    def build_data_base(self):

        """
            The function does not receive or return parameters.
            The function creates the tables of the databases and setting it up (Students, Online lessons)
        """

        self.db.create_table("STUDENTS", [["Firstname", "TEXT"], ["LastName", "TEXT"], ["Id", "TEXT"],
                                                         ["Gender", "TEXT"], ["Country", "TEXT"], ["Age", "TEXT"],
                                                         ["Username", "TEXT"], ["Password", "TEXT"]])

        self.db.create_table("OnlineLessons", [["GeneralSubject", "TEXT"], ["MainSubject", "TEXT"],
                                                              ["TargetAudience", "TEXT"], ["AuthorName", "TEXT"],
                                                              ["AuthorAge", "TEXT"], ["LastName", "TEXT"],
                                                              ["ExceptedLength", "TEXT"]])
    def convert_condition(self, condition):

        """
            credit to M.R.Studios.
            The function receives a condition and returns the condition as it should be written in sql.
            [[col, value], 0, [col, value], 1, [col, value]] --> ""col" = "value" OR "col" = "value" AND "col" = "value"
        """

        new_con = " WHERE"

        for item in condition:

            if item is int:

                if item == 0:

                    new_con += " OR"

                if item == 1:

                    new_con += " AND"

            elif type(item) is list:

                new_con += " " + item[0] + " = " + '"' + item[1] + '"'

        return new_con
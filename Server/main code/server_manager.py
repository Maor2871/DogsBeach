# -*- coding: utf-8 -*-
from DB import DB
from Online_lesson import OnlineLesson
import time
import socket
import sys
import select
from communication_thread import CommunicationThread
from User import User
from Thread import Thread
from DbFunctions import DbFunctions


class General_variables():

    """a class that represents general variables which you can access from every place in the code."""

    def __init__(self):

        self.db_functions = DbFunctions()

        self.open_client_sockets = []

        self.online_lessons = []

        # The communication instance of the server.
        self.server_manager= None

        self.main_code = None

        self.connected_users = {}

        self.online_lessons_threads = {}

        #the thread communication that work during the online lesson.

        self.main_lesson_thread = None

    def send(self, message):
        """
            The function transfer the message to the function which sends the message to other entities. Useful for
            cleaner code.
        """

        self.server_manager.send.current_messages.append(message)

    def send_to_connected_users(self, message):

        """The function receives a message and send it to every connected user (by his communication thread).
        The function does not return parameters."""

        for user in self.connected_users.values():

            user.client_com_thread.send.messages_to_send.append(message)

    def send_to_others(self, message, except_user):

        """The function receives a message and send it to every connected user (by his communication thread)
        except one user it get. The function does not return parameters.
        The function does not return parameters."""

        for user in self.connected_users.values():

            if user is not except_user:

                user.client_com_thread.send.messages_to_send.append(message)

    def get_user_name_by_id(self, id):

        """The function receives an id and return the user name that fitted to this id."""

        for user in self.connected_users.values():

            if user.id == id:

                return user.user_name


class ServerManager(object):

    """Creates fitted threads to the client that connect to the server."""

    def __init__(self, general):

        """The function receives an instance which include all the general variables.
        The function create an server communication manager which will manage the receive and send threads."""

        self.general = general

        self.socket = socket.socket()

        self.socket.bind(('0.0.0.0', 23))

        self.socket.listen(5)

        # The receive instance.
        self.receive = None

        # The send instance.
        self.send = None

    def start(self):

        """
            The function does not receive parameters.
            The function starts the send an receive threads.
            The function does not return parameters.
        """

        # Create the send instance.
        self.send = Send(self)

        # Start thr start instance.
        self.send.start()

        # Create the receive instance.
        self.receive = Receive(self)

        # Start the receive instance.
        self.receive.start()

    def generate_socket(self, ip):
        """
            The function receives the ip of the client it want to generate new socket for as a parameters.
            The function generates new socket for a new client.
            The function does not return parameters.
        """

        new_socket = socket.socket()

        # Bind the new socket with the ip of the server but use different open port.
        new_socket.bind((ip, 0))

        new_socket.listen(1)

        return new_socket


class Receive(Thread):

    """The class instance accept all the client that trying to connect to the server."""

    def __init__(self, server_manager):

        """The function receives server manager and respectively to this server manager instance it received it create
        an receive thread."""

        Thread.__init__(self, 1, "Receive")

        self.server_manager = server_manager

        self.general = server_manager.general

        # The main socket of the current server.
        self.server_socket = server_manager.socket

    def server_loop(self):

        """The function run the server loop.
        The function response to a connection of new clients and opened an communication thread to each client that
        has been connected to the server.
        The function does not return parameters."""

        while True:

            rlist, wlist, xlist = select.select( [self.server_socket] + self.general.open_client_sockets,
                                                 self.general.open_client_sockets, [])
            for current_socket in rlist:

                if current_socket is self.server_socket:

                    (new_socket, address) = self.server_socket.accept()

                    self.general.open_client_sockets.append(new_socket)

                    self.add_client(new_socket)

    def add_client(self, client_socket):
        """
            The function signs the new socket it get in to the system as a client.
            It creates a new thread that will communicate with the socket it get.
            The function does not return parameters.
        """

        print client_socket.getsockname()[0]

        client_communication_thread = ClientCommunicator(self.general, self.server_manager.generate_socket(client_socket.getsockname()[0]))


        current_client = User(self.general, client_socket, client_communication_thread)

        self.general.send([current_client, "message:connection success, new socket:" +
                                           str(current_client.client_com_thread.thread_socket.getsockname()[1])])

        # Notify the client that he is now connected to the server. Send him the new socket he'll communicate with.

    def manager(self):

        """The function does not return or receive parameters.
        The function runs the server loop."""

        self.server_loop()


class Send(Thread):

    """
         This class's instance sends anything which intended to be sent to other entities in the system.
    """

    def __init__(self, server_manager):

        """The function receives server manager and respectively to this server manager instance it received it create
        an send thread."""

        Thread.__init__(self, 2, "Send")

        self.general = server_manager.general

        # The main socket of the current Server.
        self.socket = server_manager.socket

        # The current message this class has to send.
        self.current_messages = []

        # The current message the class sends. [client, content].
        self.message = []

    def manager(self):

        """
            The function does not receive or return parameters.
        """

        while True:

            if self.current_messages:

                for message in self.current_messages:

                    self.message = message

                    self.send()

                self.current_messages = []

    def send(self):
        """
            The function sends the message in self.message to the entity in the system it should be sent to.
        """

        # The client to send the message to.
        client = self.message[0]

        # The message itself.
        content = self.message[1]

        # Send the content to the client.
        client.socket.send(content)

class MainCode():

    """The main code of the program."""

    def __init__(self, general):

        """The function create starts the program run and defines his general variables object.
        The function does not receive or return parameters."""

        self.general = general


    def start(self):
        """
            The function does not receive or return parameters.
            The function runs the main code of the client as a thread.
        """

        # start the data base thread

        self.general.db_functions.start()

        # The instance this client is going to use in order to commit ant type of outside communication.
        self.general.server_manager = ServerManager(self.general)

        # Start the communication threads. Receive and Send are beginning to operate in the background.
        self.general.server_manager.start()






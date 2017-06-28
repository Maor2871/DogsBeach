# -*- coding: utf-8 -*-
import threading
import random


class User():

    """
        The class represent a user that has connected to the program and use it right now.
    """

    random_id_numbers = []

    def __init__(self, general, socket):

        """Constructor.
        The function receives general, socket and client_com_thread in order to create an instance which will
        represent a user in the program.
        The function does not return parameters."""

        self.id = None

        self.get_random_id_number()

        self.general = general

        # The socket of the client. With this socket the system can communicate with the client

        self.socket = socket

        self.user_name = "unknown"
		
		# Start the communicator of the client.

        self.update_con_users = threading.Thread(target=self.update_connected_users)

        self.update_con_users.start()

    def update_connected_users(self):

        """The function wait till the client will connect to the program as a user, than it update this to general.
        The function does not receive or return parameters."""

        while self.user_name == "unknown":

            pass

        self.general.connected_users[self.user_name] = self

    def get_random_id_number(self):

        """The function does not receive or return parameters.
        The function update a random id number that will sign the user to self.id."""

        self.id = random.randint(0, 60000)

        #blocking until we get a number that not sign another client.

        while self.id in User.random_id_numbers:

            self.id = random.randint(0, 60000)

        User.random_id_numbers.append(self.id)
class Login:

	"""The class manage the login process"""
	
	def __init__(self, general, communicator, details):
	
		self.general = general
		
		self.communicator = communicator
		
		self.details = details
		
	def check_login_validation():
	
		"""The function check the validation of the details that the client entered at the login page."""
	
		pass
		
	def update_details(self):
	
		"""The function update the user details and the connected users list respectively to the user name he registered by."""
		
	    self.communicator.user.user_name = details[0][details[0].index(',') + 1:]

        self.general.connected_users[self.communicator.user.user_name] = self.communicator.user
		
	def start():
	
		error_container = self.check_login_validation()
	
		if not error_container:

			#log in the user.

            self.communicator.send.messages_to_send.append("message:you have been logged in to the program.:")

        else:

            #Sending the details error to the client.

            self.communicator.send.messages_to_send.append("message:login details error:" + error_container)
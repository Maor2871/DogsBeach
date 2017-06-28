class Registration:

	"""The class handle the registration process with the client."""

	def __init__(self, details):
	
		self.result = None
		
		self.details = details
		
	def check_details_validation(self):
	
		"""The function check the validation of the details that the client sent."""
		
		pass
		
	def register_to_Db(self):
	
		"""The function insert the details that the client entered for registration to db and saves him as an assigned user."""
		
		pass
		
	def send_result(self):
	
		"""The function send to the client if the registration process succeed or failed (and the reason it failed)"""
		
		pass
		
	def start(self):
	
		"""The function run the registration process."""

        error_containter = check_user_details_validation(self.communicator, self.details)

        #if error containter is none, it means that there is no problems with the details and the server need to register the user.

        #not error_containter is like - error_containter == None

        if not error_containter:

            #register the user.

            details = convert_to_original_type(self.details)

            self.general.db_functions.asks.append(("register me", self.details))

            self.communicator.send.messages_to_send.append("message:you have been registered to the program.")

        else:

            #Sending the details error to the client.

            self.communicator.send.messages_to_send.append("message:details error:" + error_containter)
		
		
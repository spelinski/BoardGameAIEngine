class MockPlayerCommunication(object):
    """
    A class used for mocking out player communication
    """

    def __init__(self):
        """
        Constructor
        """
        self.responses = []
        self.messages_received = []

    def add_response(self, response):
        self.responses.append(response)

    def send_message(self, message):
        self.messages_received.append(message)
        self.add_response("This is a response")
    
    def get_response(self):
        return self.responses.pop() if self.responses else ""

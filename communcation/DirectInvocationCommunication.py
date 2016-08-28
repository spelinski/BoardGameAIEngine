class DirectInvocationCommunication(object):

    def __init__(self, send_func, respond_func):
        self.send_func = send_func;
        self.respond_func = respond_func

    def send_message(self, message):
        send_func(message)

    def get_response(self):
        return respond_func()

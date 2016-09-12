class Notification(object):
    def __init__(self, type, **kwargs):
        self.type = type
        for k,v in kwargs.items():
            setattr(self, k, v)

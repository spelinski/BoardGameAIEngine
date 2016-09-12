from mechanics.Notification import *
import unittest

class TestNotification(unittest.TestCase):

    def test_notification(self):
        notification = Notification("type")
        self.assertEquals("type", notification.type)

    def test_notification_with_kwargs(self):
        notification = Notification("other type", arbitrary="123")
        self.assertEquals("other type", notification.type)
        self.assertEquals("123", notification.arbitrary)

__author__ = 'karolisrusenas'
from tornado.testing import AsyncHTTPTestCase
from run import TornadoApplication
import os

class Base(AsyncHTTPTestCase):
    def get_app(self):
        return TornadoApplication()

    def setUp(self):
        super(Base, self).setUp()
        # the default settting of 5 secs is not enough for my old mac
        os.environ['ASYNC_TEST_TIMEOUT'] = '50'


class TestWebHandlers(Base):

    def test_get_countries(self):
        """

        Test getting countries information
        """
        print("Testing countries")
        self.http_client.fetch(self.get_url('/top-countries'), self.stop,
                               method="GET")
        response = self.wait()
        self.assertEqual(response.code, 300, response.reason)
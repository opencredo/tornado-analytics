import tornado.ioloop
import json
import tornado.web
from tornado import auth as tornado_auth
from tornado import gen
from functools import partial, wraps
from concurrent.futures import ThreadPoolExecutor

from utilities.cache import CacheMixin

import logging
logger = logging.getLogger(__name__)


class BaseHandler(CacheMixin, tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def prepare(self):
        super(BaseHandler, self).prepare()

    def get_current_user(self):
        """
        Gets secure cookie containing user email address. Secure cookies are encrypted.
        :return:
        """
        user = self.get_secure_cookie('tracker')
        if user:
            return user
        else:
            return None

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.
        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                         "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg


class GAuthLoginHandler(BaseHandler, tornado_auth.GoogleOAuth2Mixin):

    @tornado.gen.coroutine
    def get(self):
        # if user is authenticated - redirect them
        if self.get_current_user():
            self.redirect('/')
            return

        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings["google_redirect_url"],
                                                     code=self.get_argument('code'))
            if not user:
                self.clear_all_cookies()
                raise tornado.web.HTTPError(500, 'Google authentication failed')

            access_token = str(user['access_token'])
            http_client = self.get_auth_http_client()
            response = yield http_client.fetch(
                'https://www.googleapis.com/oauth2/v1/userinfo?access_token='+access_token)

            # decoding bytecode to utf-8
            user = json.loads(response.body.decode('utf-8'))

            self.set_secure_cookie('tracker', user['email'])
            self.redirect('/')
            return

        elif self.get_secure_cookie('tracker'):
            self.redirect('/')
            return

        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings["google_redirect_url"],
                client_id=self.settings['google_oauth']['key'],
                scope=['email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto',
                              'hd': self.settings['allowed_domain']})  # passing 'hd' parameter to whitelist this domain

class AuthLogoutHandler(BaseHandler):
    def get(self):
        """
        Logout handler - deletes authentication secure cookie
        """
        if self.get_current_user():
            self.clear_cookie("tracker")
            self.redirect(self.get_argument("next", "/"))


def allowed():
    def decorator(func):
        def decorated(self, *args, **kwargs):
            user = self.get_current_user()

            # User is refused
            if user is None:
                raise Exception('Cannot proceed role check: user not found')

            if user.decode("utf-8") not in self.settings['sFwhitelist']:
                self.set_status(403)
                return self.render('500.html',
                                   code=403,
                                   error="Not authorized")
                # self.set_status(403, reason='Not authorized. Contact administrator.')
                # self._transforms = []
                # self.finish()
                # return None

            return func(self, *args, **kwargs)
        return decorated
    return decorator

EXECUTOR = ThreadPoolExecutor(max_workers=100)

def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper

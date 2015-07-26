"""A simple example of how to access the Google Analytics API."""

from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
import os


class GAcess:
    def __init__(self, scope=['https://www.googleapis.com/auth/analytics.readonly'], key_file_location=None,
                 service_account_email=None):
        """
        The google-api-python-client library is built on top of the httplib2 library, which is not thread-safe.
        Therefore, if you are running as a multi-threaded application, each thread that you are
        making requests from must have its own instance of httplib2.Http().

        :param scope:
        :param key_file_location:
        :param service_account_email:
        """
        if key_file_location is None:
            key_file_location = os.path.dirname(os.path.realpath(__file__)) + '/' + 'client_secrets.p12'
        # getting service object
        self.service = self.get_service('analytics', 'v3', scope, key_file_location,
                                        service_account_email)

    def get_service(self, api_name, api_version, scope, key_file_location,
                    service_account_email):
        """Get a service that communicates to a Google API.

        Args:
          api_name: The name of the api to connect to.
          api_version: The api version to connect to.
          scope: A list auth scopes to authorize for the application.
          key_file_location: The path to a valid service account p12 key file.
          service_account_email: The service account email address.

        Returns:
          A service that is connected to the specified API.
        """
        f = open(key_file_location, 'rb')
        key = f.read()
        f.close()

        credentials = SignedJwtAssertionCredentials(service_account_email, key,
                                                    scope=scope)

        http = credentials.authorize(httplib2.Http())

        # Build the service object.
        service = build(api_name, api_version, http=http)

        return service

    def get_first_profile_id(self):
        # Use the Analytics service object to get the first profile id.

        # Get a list of all Google Analytics accounts for this user
        accounts = self.service.management().accounts().list().execute()

        if accounts.get('items'):
            # Get the first Google Analytics account.
            account = accounts.get('items')[0].get('id')

            # Get a list of all the properties for the first account.
            properties = self.service.management().webproperties().list(
                accountId=account).execute()

            if properties.get('items'):
                # Get the first property id.
                property = properties.get('items')[0].get('id')

                # Get a list of all views (profiles) for the first property.
                profiles = self.service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

                if profiles.get('items'):
                    # return the first view (profile) id.
                    return profiles.get('items')[0].get('id')

        return None

    def get_sessions_results(self, profile_id=None, days=30):
        """
         Use the Analytics Service Object to query the Core Reporting API
        for the number of sessions within the past seven days.

        :param profile_id: profile ID - leave blank to use the first one, otherwise provide string containing profile ID
        :param days: optional, integer
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:sessions').execute()
        print("got sessions")
        return results

    def get_people_sources(self, profile_id=None, days=30, max_results=10):
        """

        :param profile_id: profile ID - leave blank to use the first one, otherwise provide string containing profile ID
        :param days: optional, integer
        :param max_results: optional, integer
        :return:
        """

        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:sessions,ga:pageviews,ga:sessionDuration',
            dimensions='ga:source,ga:medium',
            sort='-ga:sessions',
            max_results=max_results).execute()
        print("got sources")
        return results

    def get_top_countries(self, profile_id=None, days=30, max_results=5):
        """
        Get countries where your readers live

        :param profile_id: integer, default is the first one in your profile
        :param days: integer, default is 30
        :param max_results: integer, default is 5
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:sessions',
            dimensions='ga:country',
            sort='-ga:sessions',
            max_results=max_results).execute()
        print("got countries")
        return results

    def get_users(self, profile_id=None, days=30):
        """
        Gets total unique users that are reading your posts

        :param profile_id: integer, default is the first one in your profile
        :param days: integer, default is 30
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:users').execute()
        print("got total users")
        return results

    def get_top_pages(self, profile_id=None, days=30, max_results=10):
        """
        Which posts are most popular?
        :param profile_id:
        :param days:
        :param max_results:
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:pageviews,ga:uniquePageviews,ga:timeOnPage,ga:bounces,ga:entrances,ga:exits',
            dimensions='ga:pagePath',
            max_results=max_results,
            sort='-ga:pageviews').execute()
        print("got top pages")
        return results

    def get_top_keywords(self, profile_id=None, days=30, max_results=10):
        """
        Which search terms are used to find you?

        :param profile_id:
        :param days:
        :param max_results:
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:sessions',
            dimensions='ga:keyword',
            filters='ga:keyword!@(not',
            max_results=max_results,
            sort='-ga:sessions').execute()
        print("got top keywords")
        return results

    def get_referrers(self, profile_id=None, days=30, max_results=10):
        """
        Who is referring to your site?

        :param profile_id:
        :param days:
        :param max_results:
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:users,ga:bounceRate',
            dimensions='ga:fullReferrer',
            filters='ga:fullReferrer!@google;ga:fullReferrer!@(direct)',
            max_results=max_results,
            sort='-ga:users').execute()
        print("got top referrers")
        return results

    def get_top_browsers_n_os(self, profile_id=None, days=30, max_results=10):
        """
        Who is referring to your site?

        :param profile_id:
        :param days:
        :param max_results:
        :return:
        """
        # getting profile ID
        if profile_id is None:
            profile_id = self.get_first_profile_id()

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='%sdaysAgo' % days,
            end_date='today',
            metrics='ga:sessions',
            dimensions='ga:operatingSystem,ga:operatingSystemVersion,ga:browser,ga:browserVersion',
            max_results=max_results,
            sort='-ga:sessions').execute()
        print("got top browsers and os")
        return results

def main():

    """
    This function is meant for testing. Add client_secrets to your utilities directory (next to gaclient.py) and type
    in your console (when in project root) "python utilities/gaclient.py" to access shell. You can manipulate
    "sv" object to try out new queries or commands to API client. You can also override some parameters, like
    service account, scope or key_file_location.

    """
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    # don't forget to add your service account email address to your google analytics users!
    service_account_email = '***REMOVED***'
    # download client secrets file from your google developer console > auth > credentials
    # key_file_location = 'utilities/client_secrets.p12'

    # authenticate and construct service
    # service = GAcess(scope, key_file_location, service_account_email)
    sv = GAcess(service_account_email=service_account_email)

    # use service object to call commands (get_people_sources, etc..)
    import pdb
    pdb.set_trace()


if __name__ == '__main__':
    main()

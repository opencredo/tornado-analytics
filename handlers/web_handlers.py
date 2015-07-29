from handlers.base import BaseHandler, unblock
from utilities.gaclient import GAcess
from utilities.cache import cache
from settings import CACHE_EXPIRES
from tornado import web

class LoginPage(BaseHandler):

    @cache(1)
    def get(self):
        self.render('accounts/login.html')


class MainHandler(BaseHandler):

    @web.authenticated
    @cache(1)
    def get(self):
        self.render('index.html')


class PeopleSourcesHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns people sources, how they find you. Result dictionary contains headers and rows.

        Example:
        headers:
        {'columnHeaders': [{'columnType': 'DIMENSION',
                    'dataType': 'STRING',
                    'name': 'ga:source'},
                   {'columnType': 'DIMENSION',
                    'dataType': 'STRING',
                    'name': 'ga:medium'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:sessions'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:pageviews'},
                   {'columnType': 'METRIC',
                    'dataType': 'TIME',
                    'name': 'ga:sessionDuration'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:exits'}],

        rows:
        ['google', 'organic', '7598', '10480', '366955.0', '7598'],
         ['(direct)', '(none)', '3563', '4376', '134037.0', '3562'],
         ['reddit.com', 'referral', '1026', '1236', '39638.0', '1026'],

        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_people_sources(profile_id=self.settings['ga_profile_id'],
                                                           days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch people source data')
            else:
                # formatting seconds to more human readable version
                for row in data:
                    m, s = divmod(int(float(row[4])), 60)
                    h, m = divmod(m, 60)
                    row[4] = "%d:%02d:%02d" % (h, m, s)

                table_title = 'How did people found our pages?'
                headers = ['Source', 'Medium', 'Sessions', 'Page views', 'Avg. duration']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)


class TopCountriesHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns top countries where your readers live.

        Example:
        headers:
        [{'columnType': 'DIMENSION',
                    'dataType': 'STRING',
                    'name': 'ga:country'},
        {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:sessions'}],

        rows:
        'rows': [['United States', '3740'],
                  ['United Kingdom', '2228'],
                  ['India', '1177'],
                  ['Russia', '667'],
                  ['Germany', '612']],


        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_top_countries(profile_id=self.settings['ga_profile_id'],
                                                          days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch top countries data')
            else:
                table_title = 'Where do our readers live?'
                headers = ['Country', 'Users']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)

class TopPagesHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns posts that are most popular.

        Example:
        headers:
         [{'columnType': 'DIMENSION',
                    'dataType': 'STRING',
                    'name': 'ga:pagePath'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:pageviews'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:uniquePageviews'},
                   {'columnType': 'METRIC',
                    'dataType': 'TIME',
                    'name': 'ga:timeOnPage'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:bounces'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:entrances'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:exits'}],
        rows:
        [['/2015/07/08/a-deep-dive-into-angular-2-0/',
           '4327',
           '4043',
           '126847.0',
           '3741',
           '4012',
           '3993'],
          ['/', '1892', '1689', '3CACHE_EXPIRES65.0', '1095', '1590', '1191'],
          ['/2014/02/24/experiences-with-spring-boot/',
           '1166',
           '1133',
           '16328.0',
           '1097',
           '1129',
           '1127'],

        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_top_pages(profile_id=self.settings['ga_profile_id'],
                                                      days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch top pages data')
            else:
                # formatting seconds to more human readable version
                for row in data:
                    m, s = divmod(int(float(row[3])), 60)
                    h, m = divmod(m, 60)
                    row[3] = "%d:%02d:%02d" % (h, m, s)

                table_title = 'Which posts are most popular?'
                headers = ['Path', 'Page views', 'Unique views', 'Avg. time on page', 'Bounces', 'Ent.', 'Exits']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)


class TopKeywordsHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns a list of top search terms that have been used to find you

        example:
        headers:
        [{'columnType': 'DIMENSION',
                    'dataType': 'STRING',
                    'name': 'ga:keyword'},
                   {'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:sessions'}],
        rows:
        [['linkplug-angularjs-job-board-contractor-listings', '302'],
          ['spring with cassandra', '13'],
          ['opencredo', '5'],
          ['https://www.opencredo.com/2015/07/08/a-deep-dive-into-angular-2-0/',
           '4'],
          ['0_4bba7e0c9e-e432a867c8-344988337', '3'],

        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_top_keywords(profile_id=self.settings['ga_profile_id'],
                                                         days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch top keywords data')
            else:
                table_title = 'What keywords were used to find us?'
                headers = ['Keyword', 'Sessions']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)

class TotalUsersHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns total amount of people that are reading your posts

        example:
        headers:
        [{'columnType': 'METRIC',
                    'dataType': 'INTEGER',
                    'name': 'ga:users'}],

        rows:
        [['11135']],

        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_users(profile_id=self.settings['ga_profile_id'],
                                                  days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch total users data')
            else:
                table_title = 'How many people are reading our posts?'
                headers = ['']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)

class ReferrersHandler(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns your referrers list

        example:
        headers:
        [
          {
           "name": "ga:fullReferrer",
           "columnType": "DIMENSION",
           "dataType": "STRING"
          },
          {
           "name": "ga:users",
           "columnType": "METRIC",
           "dataType": "INTEGER"
          },
          {
           "name": "ga:bounces",
           "columnType": "METRIC",
           "dataType": "INTEGER"
          }
         ],

        rows:
        [
          [
           "linkplug",
           "216",
           "273"
          ],
          [
           "4webmasters.org/",
           "189",
           "194"
          ],
          [
           "reddit.com/",
           "152",
           "173"
          ],
        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_referrers(profile_id=self.settings['ga_profile_id'],
                                                      days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch referrers data')
            else:
                # formatting decimal values to percentage
                for row in data:
                    row[2] = ("%.2f" % float(row[2])) + "%"

                table_title = 'Who is linking to us?'
                headers = ['Full referrer', 'Users', 'Bounces']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)


class TopBrowserAndOs(BaseHandler):

    @web.authenticated
    @cache(CACHE_EXPIRES)  # set the cache expires
    @unblock
    def get(self):
        """
        Returns your users top browsers and operating systems

        example:
        headers:
        "columnHeaders": [
              {
               "name": "ga:operatingSystem",
               "columnType": "DIMENSION",
               "dataType": "STRING"
              },
              {
               "name": "ga:operatingSystemVersion",
               "columnType": "DIMENSION",
               "dataType": "STRING"
              },
              {
               "name": "ga:browser",
               "columnType": "DIMENSION",
               "dataType": "STRING"
              },
              {
               "name": "ga:browserVersion",
               "columnType": "DIMENSION",
               "dataType": "STRING"
              },
              {
               "name": "ga:sessions",
               "columnType": "METRIC",
               "dataType": "INTEGER"
              }
        :return:
        """
        try:
            service_account = self.settings['service_account_email']
            self.service = GAcess(service_account_email=service_account,
                                  key_file_location=self.settings['key_file_location'])

            query_result = self.service.get_top_browsers_n_os(profile_id=self.settings['ga_profile_id'],
                                                              days=self.settings['start_days_ago'])
            try:
                data = query_result['rows']
            except KeyError:
                self.set_status(400, reason='Failed to fetch referrers data')
            else:

                table_title = 'What browser and OS our readers use?'
                headers = ['OS', 'Version', 'Browser', 'Browser version', 'Sessions']
                return self.render_string('webhandler/data_table.html',
                                          data=data,
                                          table_title=table_title,
                                          headers=headers)
        except Exception as ex:
            self.set_status(403)
            return self.render_string('error.html',
                                      error=ex)


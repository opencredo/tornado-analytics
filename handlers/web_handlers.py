from handlers.base import BaseHandler, unblock
from utilities.gaclient import GAcess
from pprint import pprint as pp
import time

class MainHandler(BaseHandler):

    def get(self):

        self.render('index.html')


class PeopleSourcesHandler(BaseHandler):

    def initialize(self):
        service_account = self.settings['service_account_email']
        self.service = GAcess(service_account_email=service_account)

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
        query_result = self.service.get_people_sources()
        try:
            data = query_result['rows']
        except KeyError:
            self.set_status(400, reason='Failed to fetch people source data')
        else:
            return self.render_string('webhandler/people_sources.html', data=data)
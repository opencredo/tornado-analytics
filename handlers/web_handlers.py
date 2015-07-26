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
            table_title = 'How did people found your pages?'
            headers = ['Source', 'Medium', 'Sessions', 'Page views', 'Duration']
            return self.render_string('webhandler/data_table.html',
                                      data=data,
                                      table_title=table_title,
                                      headers=headers)


class TopCountriesHandler(BaseHandler):
    def initialize(self):
        service_account = self.settings['service_account_email']
        self.service = GAcess(service_account_email=service_account)

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
        query_result = self.service.get_top_countries()

        try:
            data = query_result['rows']
        except KeyError:
            self.set_status(400, reason='Failed to fetch top countries data')
        else:
            table_title = 'Where do your readers live??'
            headers = ['Country', 'Users']
            return self.render_string('webhandler/data_table.html',
                                      data=data,
                                      table_title=table_title,
                                      headers=headers)

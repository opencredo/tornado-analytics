__author__ = 'karolisrusenas'
from tornado.httpclient import AsyncHTTPClient
import json
from tornado import gen
import collections

from simple_salesforce import Salesforce


class SFAccess:
    session = None
    instance = None

    def __init__(self, settings):
        self.sf_user = settings["sfUser"]
        self.sf_pswd = settings["sfPsw"]
        self.sf_token = settings["sfToken"]

    def login(self):
        self.sf = Salesforce(username=self.sf_user,
                             password=self.sf_pswd,
                             security_token=self.sf_token)

        # these can be stored and reused for faster authentication
        self.instance = self.sf.sf_instance
        self.session = self.sf.session_id

    def quick_search(self, name):
        return self.sf.quick_search(name)

    @gen.coroutine
    def get_report(self, report_id=None):
        if report_id is not None:
            # check if we have logged in
            if self.session is None:
                self.login()
            # do the call
            http_client = AsyncHTTPClient()
            future = http_client.fetch(
                "https://%s/services/data/v34.0/analytics/reports/%s" % (self.instance, report_id),
                headers={
                    "Authorization": "Bearer %s" % self.session}
            )
            result = yield future
            # result here brings whole report and you need to decode it then
            # https://developer.salesforce.com/docs/atlas.en-us.api_analytics.meta/api_analytics/sforce_analytics_rest_api_factmap_example.htm
            data = json.loads(result.body.decode("utf-8"))
            return data
        else:
            raise ValueError("You must provide report_id")

    @gen.coroutine
    def get_utilisation_report(self, report_id):
        data = yield self.get_report(report_id)
        # getting useful date range dictionary
        date_range_dict = get_time_range(data)
        # getting employee names and keys
        employee_key_dict = get_employee_names(data)

        # getting final report
        final_report = create_final_util_report(raw_report=data,
                                                time_dict=date_range_dict,
                                                employee_dict=employee_key_dict)
        return final_report

    @gen.coroutine
    def get_billability_report(self, report_id):
        data = yield self.get_report(report_id)
        # getting useful date range dictionary
        date_range_dict = get_time_range(data)
        # getting employee names and keys
        employee_key_dict = get_employee_names(data)
        # getting final report
        final_report = create_final_billability_report(raw_report=data,
                                                       time_dict=date_range_dict,
                                                       employee_dict=employee_key_dict)
        return final_report

def get_time_range(report):
    """
    Provide date ranges. Keys should be sorted in ascending order
    :param report: decoded and json loaded Kimble report
    :return: :raise KeyError:
    """
    if 'groupingsAcross' in report:
        result_dict = {}
        # we are only interested in this part of the report
        date_ranges = report['groupingsAcross']['groupings']
        # groupings provide a list with date ranges (months)
        for date_range in date_ranges:
            key = date_range['key']
            result_dict[key] = {'label': date_range['label'],
                                'value': date_range['value']}

        return result_dict
    else:
        raise KeyError("groupingsAcross key was not found in your report")


def get_employee_names(report):
    """
    Creates employee dictionary, where you can query for results like this:
    (PDB) employee_key_dict['1_13']
    {'name': 'Karolis Rusenas', 'group_key': '1', 'group_name': 'Employee'}

    :param report: decoded and json loaded Kimble report
    :return: :raise KeyError:
    """
    if 'groupingsDown' in report:
        result_dict = {}
        people_groupings = report['groupingsDown']['groupings']
        for people_group in people_groupings:
            group_name = people_group['label']
            group_key = people_group['key']

            for people in people_group['groupings']:
                key = people['key']

                result_dict[key] = {'name': people['label'],
                                    'group_name': group_name,
                                    'group_key': group_key}
        return result_dict
    else:
        raise KeyError("groupingsDown key was not found in your report")


def create_final_billability_report(raw_report, time_dict, employee_dict):
    """
    Returns final report which has title, headers with months, metadata with currency, and body with:

    :param raw_report:
    :param time_dict:
    :param employee_dict:
    :return: Dict
    """
    result_dict = {}
    # create headers for the report
    headers = []
    for key, value in sorted(time_dict.items()):
        headers.append(value['label'])
    result_dict['headers'] = headers

    # add title
    result_dict['title'] = raw_report['attributes']['reportName']

    # report metadata - column descriptions and currency
    column_info = collections.OrderedDict(sorted(raw_report['reportExtendedMetadata']['aggregateColumnInfo'].items()))
    columns = []
    for _, v in column_info.items():
        columns.append(v['label'])
    meta = {
        'column_info': columns,
        'currency': raw_report['reportMetadata']['currency']
    }
    result_dict['meta'] = meta

    # create body for the report
    body_employee_records = {}

    for key, value in raw_report['factMap'].items():

        empl_key, code = key.split('!')
        # if there is no '_' symbol in key - this is group statistic then
        if '_' not in empl_key:
            continue

        # get full name from value {'group_key': '1', 'group_name': 'Employee', 'name': 'Karolis Rusenas'}
        employee_full_name = employee_dict[empl_key]['name']
        # getting utilisation
        aggregates = value['aggregates']

        # check if employee is not in dictionary
        if employee_full_name not in body_employee_records.keys():
            # creating name in dictionary and assign empty list
            body_employee_records[employee_full_name] = {code: aggregates}

        # append new rows with billability
        else:
            current_dict = body_employee_records[employee_full_name]
            current_dict[code] = aggregates
            body_employee_records[employee_full_name] = current_dict

    result_dict['body'] = body_employee_records
    return result_dict



def create_final_util_report(raw_report, time_dict, employee_dict):
    """
    Returns final report which has title, headers with months, and body with:
    {'body':
      {'Some Employee': {'1': '100.00%', '2': '63.64%', 'T': '84.00%', '0': '100.00%'},
       'Another Employee': {'2': '0.00%', '1': '110.00%', 'T': '69.23%', '0': '100.00%'},
       ...
       ...
       ...
       },
       'headers': ['August 2015', 'September 2015', 'July 2015'],
       'title: 'Utilisation report 1'
    }

    :param raw_report:
    :param time_dict:
    :param employee_dict:
    :return: Dict
    """
    result_dict = {}
    # create headers for the report
    headers = []
    for key, value in sorted(time_dict.items()):
        headers.append(value['label'])
    result_dict['headers'] = headers

    # add title
    result_dict['title'] = raw_report['attributes']['reportName']

    # create body for the report
    body_employee_records = {}

    for key, value in raw_report['factMap'].items():

        empl_key, code = key.split('!')
        # if there is no '_' symbol in key - this is group statistic then
        if '_' not in empl_key:
            continue

        # get full name from value {'group_key': '1', 'group_name': 'Employee', 'name': 'Karolis Rusenas'}
        employee_full_name = employee_dict[empl_key]['name']
        # getting utilisation
        utilisation = value['aggregates'][0]['value']
        # check for Nones
        if utilisation == "None" or utilisation is None:
            utilisation = '0.00'

        utilisation = float("{0:.2f}".format(float(utilisation)))

        # check if employee is not in dictionary
        if employee_full_name not in body_employee_records.keys():
            # creating name in dictionary and assign empty list
            body_employee_records[employee_full_name] = {code: utilisation}

        # append new rows with utilization
        else:
            current_dict = body_employee_records[employee_full_name]
            current_dict[code] = utilisation
            body_employee_records[employee_full_name] = current_dict

    result_dict['body'] = body_employee_records
    return result_dict

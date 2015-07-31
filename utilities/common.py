__author__ = 'karolisrusenas'

from tornado.httpclient import AsyncHTTPClient
import json
from tornado import gen

@gen.coroutine
def get_facebook_results(urls):
    """
    Gets statistics for given URLs in facebook, returns a list with results
    :param urls: list of urls
    :return: list with integers (how many shares)
    """
    http_client = AsyncHTTPClient()
    futures_list = []
    results = []
    for url in urls:
        futures_list.append(http_client.fetch("http://graph.facebook.com/?id="+url))
    responses = yield futures_list
    for response in responses:
        try:
            results.append(json.loads(response.body.decode('utf-8'))['shares'])
        except KeyError:
            results.append(0)
        except Exception as ex:
            print(ex)
            results.append(0)
    return results

@gen.coroutine
def get_twitter_results(urls):
    """
    Gets statistics for given URLs in twitter, returns a list with results
    :param urls: list of urls
    :return: list with integers (how many shares)
    """
    http_client = AsyncHTTPClient()
    futures_list = []
    results = []
    for url in urls:
        futures_list.append(http_client.fetch("https://cdn.api.twitter.com/1/urls/count.json?url="+url))
    responses = yield futures_list
    for response in responses:
        try:
            results.append(json.loads(response.body.decode('utf-8'))['count'])
        except KeyError:
            results.append(0)
        except Exception as ex:
            print(ex)
            results.append(0)
    return results

@gen.coroutine
def get_linkedin_results(urls):
    """
    Gets statistics for given URLs in linkedin, returns a list with results
    :param urls: list of urls
    :return: list with integers (how many shares)
    """
    http_client = AsyncHTTPClient()
    futures_list = []
    results = []
    for url in urls:
        futures_list.append(http_client.fetch("http://www.linkedin.com/countserv/count/share?url="+url+"&format=json"))
    responses = yield futures_list
    for response in responses:
        try:
            results.append(json.loads(response.body.decode('utf-8'))['count'])
        except KeyError:
            results.append(0)
        except Exception as ex:
            print(ex)
            results.append(0)
    return results

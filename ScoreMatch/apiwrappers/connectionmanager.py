#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides helpers for API calls.
   
"""
import urllib
import contextlib
import time
import singleton
import json
import requests
import httplib

class CheckInformation(object):
    """
        This class represent a check information for an api call.

        Responses to api calls are checked with instances of this class.For example  successful responses to
        echonest api calls  are marked with 'Success' in data['response']['status']['message']
        :class:`.ConnectionManager` use this clue and repeat its calls after waiting a period if the response is unsuccessful
        because api usage threshold is exceeded

        attributes:
            keys:Keys for the data json
            expected_value: Expected value for the check information
            wait_amount: Number of seconds the wait if check is not satisfied
            wait_text: Informative text when the check condition is not satisfied and program waits


    """
    def __init__(
        self,
        keys,
        expected_value,
        wait_amount,
        wait_text,
        ):

        self.keys = keys
        self.expected_value = expected_value
        self.wait_amount = wait_amount
        self.wait_text = wait_text


class ConnectionManager(object):

    """This class provides general helpers for interacting with echonest, spotify and musescore apis.

    """
    __metaclass__ = singleton.Singleton

    def get_from_dict(self, data, keylist):
        return reduce(lambda d, k: d[k], keylist, data)

    @staticmethod
    def print_info_and_wait(wait_text, wait_amount):
        """waits by a specified wait amount and prints why the execution is paused.

        This function is called when api calls are returned unsuccessful response upon exceeding of usage threshold 

        attributes:
            wait_text: Text to print
            wait_amount: Number of seconds to wait
        """
        print wait_text, wait_amount, 'secs'
        time.sleep(wait_amount)

    def need_to_wait(self, data, check_information_list):

        if type(check_information_list) is not list:
            check_information_list = [check_information_list]
        for check_information in check_information_list:
            try:

                value = self.get_from_dict(data, check_information.keys)
                if value == check_information.expected_value:
                    return False
            except:
                continue
        ConnectionManager.print_info_and_wait(check_information.wait_text,
                check_information.wait_amount)
        return True

    def get_data(
        self,
        url,
        params={},
        check_information=None,
        ):
        params = urllib.urlencode(params)
        url = urllib.quote(url + params, safe="%/:=&?~#+!$,;'@()*[]")
        print url
        with contextlib.closing(urllib.urlopen(url)) as response:
            data = json.loads(response.read())
            if check_information:
                while self.need_to_wait(data, check_information):
                    with contextlib.closing(urllib.urlopen(url)) as \
                        nested_response:
                        data = json.loads(nested_response.read())
            return data

    def post_data(
        self,
        url,
        file_,
        params,
        check_information=None,
        ):

        params = urllib.urlencode(params)
        url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        url = url + params

        # data = requests.post(url, files=files, data=values).json()

        file_data = file_.read()
        res = requests.post(url=url, data=file_data,
                            headers={'Content-Type': 'application/octet-stream'
                            })
        data = res.json()
        if check_information:
            while self.need_to_wait(data, check_information):
                res = requests.post(url=url, data=file_data,
                                    headers={'Content-Type': 'application/octet-stream'
                                    })
                data = res.json()
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib.parse import urlencode
import httplib2


class JamendoRadio(object):
    def __init__(self):
        self.__endpoint = 'http://api.jamendo.com/v3.0/'
        self.__client_id = 'b6747d04'
        self.__format = 'json' # enum: {xml, json, jsonpretty}

    def __request(self, endpoint, parameters):
        h = httplib2.Http('.cache')
        parameters.update({'client_id': self.__client_id, 'format': self.__format})
        response, content = h.request(endpoint + urlencode(parameters), 'GET')
        json_content = json.loads(content.decode())

        if json_content['headers']['status'] == 'success':
            return json_content['results']
        else:
            raise Exception('Failed to get result.')

    def get_radio_list(self):
        return self.__request(self.__endpoint + 'radios/?', {'limit': 200})

    def get_stream_info(self, id):
        return self.__request(self.__endpoint + 'radios/stream/?', {'id': id})

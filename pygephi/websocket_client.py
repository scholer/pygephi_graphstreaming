#!/usr/bin/python
# coding: utf-8
#
# Copyright (C) 2012 André Panisson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Websocket communication with Gephi using the Gephi Graph-streaming protocol and plugin.

Based on client.py by André Panisson and examples by Matthieu Totet

See also:
* https://github.com/totetmatt/gephi.stream.graph.websocket
* http://matthieu-totet.fr/Koumin/2014/06/15/lets-play-gephi-streaming-api-the-hidden-websocket/
* https://github.com/panisson/pygephi_graphstreaming/network

"""

from __future__ import print_function, absolute_import

__author__ = 'rasmusscholer@gmail.com'

import json
import time
from websocket import create_connection

from .client import GephiClient


class GephiWsClient(GephiClient):
    """
    Class for communicating with the Gephi graph-streaming plugin over websocket protocol.
    This is slightly faster than REST communication with HTTP requests.
    """
    def __init__(self, url='ws://127.0.0.1:8080/workspace0', autoflush=False, autoconnect=True):
        GephiClient.__init__(self, url, autoflush)
        self.conn = None
        if autoconnect:
            self.connect()

    def connect(self):
        self.conn = create_connection(self.url)

    def _send(self, data):
        if self.conn is None:
            self.connect()
        try:
            return self.conn.send(data)
        except ConnectionAbortedError as e:
            print("Connection aborted,", e)
            print("Retrying connection...")
            self.connect()
            self.conn.send(data)

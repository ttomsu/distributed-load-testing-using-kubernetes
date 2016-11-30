#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from datetime import datetime
from locust import HttpLocust, TaskSet, task


class MetricsTaskSet(TaskSet):
    _auth_header = None
    _cookie_jar = None

    def on_start(self):
        self._auth_header = 'Bearer ' + os.environ['ACCESS_TOKEN']
        resp = self.client.request('GET', '/credentials', headers={'Authorization': self._auth_header} )
        self._cookie_jar = resp.cookies

    @task(1)
    def get_credentials(self):
        self.client.get('/credentials', cookies=self._cookie_jar)

    @task(1)
    def get_server_groups(self):
        self.client.get('/applications/spin/serverGroups', cookies=self._cookie_jar)

    @task(1)
    def get_loadBalancers(self):
        self.client.get('/applications/spin/loadBalancers', cookies=self._cookie_jar)

    @task(1)
    def get_pipelines(self):
        self.client.get('/applications/spin/pipelines?limit=30&statuses=RUNNING,SUSPENDED,PAUSED,NOT_STARTED', cookies=self._cookie_jar)

    def on_failure(request_type, name, response_time, exception, **kwargs):
        print exception

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet

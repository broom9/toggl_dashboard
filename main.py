#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import base64
from google.appengine.api import urlfetch
import json
import hashlib
from tokens import tokens

class MainHandler(webapp2.RequestHandler):
	def get(self):
		results = []
		for t in tokens:
			url = "https://www.toggl.com/api/v6/me.json?with_related_data=true"
			base64string = base64.encodestring('%s:%s' % (t, "api_token")).replace('\n', '')
			result = urlfetch.fetch(url=url,
													 method = urlfetch.GET,
													 headers = {"Authorization": "Basic %s" % base64string})
			j = json.loads(result.content)
			results.append({"fullname" : j["data"]["fullname"], 
									 "email_md5" : hashlib.md5(j["data"]["email"]).hexdigest(),
									 "time_entry" : filter(lambda x: x["duration"] < 0, j["data"]["time_entries"])})

		self.response.write(json.dumps(results))

app = webapp2.WSGIApplication([
	('/proxy', MainHandler)
], debug=True)

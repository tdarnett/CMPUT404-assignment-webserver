#  coding: utf-8 
import SocketServer
import mimetypes
import os

# Copyright 2017 Taylor Arnett
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
#
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    www_path = os.path.abspath('./www')

    STATUS = dict(
        OK="HTTP/1.1 200 OK\r\n",
        NOT_FOUND="HTTP/1.1 404 Not Found\r\n",
        METHOD_NOT_ALLOWED="HTTP/1.1 405 Method Not Allowed\r\n",
    )

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.split('\r')[0]
        resource = self.get_resource(request)

        if resource[-1] == '/':
            resource = '%sindex.html' % resource  # given a trailing '/', load an index.html page

        try:
            if "/.." in resource:  # for security
                raise

            resource_path = self.www_path + resource

            if not os.path.exists(resource_path):
                raise

            body = open(resource_path, 'r')

            # Send headers
            # Header information used from https://davidwalsh.name/curl-headers on January 18, 2017
            self.request.sendall(self.STATUS['OK'])

            mime_type = mimetypes.guess_type(resource)
            self.request.sendall("Content-Type: %s ; charset=utf-8\r\n\r\n" % mime_type[0])  # To support MIME types

            self.request.sendall(body.read())

        except:  # catch all errors potentially thrown with a 404
            self.request.sendall(self.STATUS['NOT_FOUND'])
            return

    def get_resource(self, request):
        '''
        returns the requested resource from the url.
        Only accepts GET requests
        '''
        request_array = request.split(' ')
        if request_array[0] != 'GET':
            self.request.sendall(self.STATUS['METHOD_NOT_ALLOWED'])
            return

        return request_array[1]  # url


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

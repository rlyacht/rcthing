#!/usr/bin/env python

"""Toy database program for pair programming interview, as described here:

    https://www.recurse.com/pairing-tasks

Provides two methods to get and set values in a (transient) database

     /set?{key}={value}...
     /get?key={key}
"""

import BaseHTTPServer
import urlparse

HOST = 'localhost'
PORT = 4000


class ToyDatabase(BaseHTTPServer.BaseHTTPRequestHandler):
    Database = {'fish': 'bream'}

    def respond(self, json=None, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        print "sending back", json
        self.wfile.write(json)

    def handle_set(self, parameters):
        print "parameters", parameters

        ToyDatabase.Database.update({k: v[0] for k, v in parameters.iteritems()})
        self.respond(ToyDatabase.Database)

    def handle_get(self, parameters):
        try:
            requested = parameters['key'][0]
        except KeyError:
            self.respond(None, 403)

        print "requested", requested
        try:
            print {requested: ToyDatabase.Database[requested]}
            self.respond({requested: ToyDatabase.Database[requested]})
        except KeyError:
            self.respond(None, 404)

    handlers = {
        '/set': handle_set,
        '/get': handle_get
        }

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        parameters = urlparse.parse_qs(parsed.query)
        print 'path', parsed.path
        try:
            print "parameters", parameters
            print "path", parsed.path
            ToyDatabase.handlers[parsed.path](self, parameters)
        except KeyError:
            self.respond(None, 403)

def main():
    server = BaseHTTPServer.HTTPServer((HOST,PORT), ToyDatabase)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    print "Shutting Down"
    server.server_close()


if __name__ == '__main__':
    main()


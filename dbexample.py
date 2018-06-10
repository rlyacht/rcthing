import BaseHTTPServer
import urlparse

HOST = 'localhost'
PORT = 3141


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    Database = {'fish': 'bream'}

    def respond(self, json=None, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        print "sending back", json
        self.wfile.write(json)

    def handle_set(self, parameters):
        print "parameters", parameters

        MyHandler.Database.update({k: v[0] for k, v in parameters.iteritems()})
        self.respond(MyHandler.Database)

    def handle_get(self, parameters):
        try:
            requested = parameters['key'][0]
        except KeyError:
            self.respond(None, 403)

        print "requested", requested
        try:
            print {requested: MyHandler.Database[requested]}
            self.respond({requested: MyHandler.Database[requested]})
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
            MyHandler.handlers[parsed.path](self, parameters)
        except KeyError:
            self.respond(None, 403)


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST, PORT), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()

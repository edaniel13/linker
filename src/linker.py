#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

import json

PORT_NUMBER = 12345

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
  #Handler for the GET requests
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("Hello World !")
    return

  def do_POST(self):
    print "client_address: ", self.client_address
    print "server: ", self.server
    print "command: ", self.command
    print "path: ", self.path
    print "request_version: ", self.request_version
    print "headers: ", self.headers
    #print "rfile: ", self.rfile
    #print "content-length: ", self.headers['Content-Length']
    #print self.rfile.read(self.headers['Content-Length'])
    print self.rfile.read(int(self.headers['Content-Length']))

    if self.path == "/Plugin.Activate":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      x = { "Implements": ["NetworkDriver"] }
      self.wfile.write(json.dumps(x))

    if self.path == "/NetworkDriver.GetCapabilities":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      x = { "Scope": "local",
            "ConnectivityScope": "global" }
      self.wfile.write(json.dumps(x))

    if self.path == "/NetworkDriver.AllocateNetwork":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.FreeNetwork":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.CreateNetwork":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DeleteNetwork":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.CreateEndpoint":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.EndpointOperInfo":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DeleteEndpoint":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.Join":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.Leave":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DiscoverNew":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DiscoverDelete":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.ProgramExternalConnectivity":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.RevokeExternalConnectivity":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass

try:
  #Create a web server and define the handler to manage the
  #incoming request
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ' , PORT_NUMBER
	
  #Wait forever for incoming htto requests
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()


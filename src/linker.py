#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

import json
import subprocess

PORT_NUMBER = 12345

def runBashCmd(cmd):
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output, error

def getMacByInterface(interfaceName):
  cmd = "cat /sys/class/net/" + interfaceName + "/address"
  output, error = runBashCmd(cmd)
  return output.rstrip()

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

  def mySetup(self):
    self.interfaceName = "myIface"
    self.parentInterfaceName = "eno1"
    self.interfaceIP = "192.168.0.151/24"
    self.gateway = "192.168.0.1"

  def CreateEndpoint(self):
    # Create the macvlan interface
    cmd = "ip link add " + self.interfaceName + " link " + self.parentInterfaceName + " type macvlan mode bridge"
    output, error = runBashCmd(cmd)

    # Add an IP to the new interface
    cmd = "ip addr add " + self.interfaceIP + "dev " + self.interfaceName
    output, error = runBashCmd(cmd)
    #print output

    self.interfaceMac = getMacByInterface(self.interfaceName)

    x = { 
          "Interface": 
          {
             #
             # Since the "Interface" object we received was NOT empty, 
             # an empty response must be provided.
             #
#            'Address':self.interfaceIP,
#            'AddressIPv6':'',
#            'MacAddress':self.interfaceMac
          }
        }

    return json.dumps(x)

  def DeleteEndpoint(self):
    # Create the macvlan interface
    cmd = "ip link del " + self.interfaceName
    output, error = runBashCmd(cmd)
    

  #Handler for the GET requests
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()

  def do_POST(self):
    self.mySetup()
    print "client_address: ", self.client_address
    print "server: ", self.server
    print "command: ", self.command
    print "path: ", self.path
    print "request_version: ", self.request_version
    print "headers: ", self.headers
    #print "rfile: ", self.rfile
    #print "content-length: ", self.headers['Content-Length']
    #print self.rfile.read(self.headers['Content-Length'])
    self.content = self.rfile.read(int(self.headers['Content-Length']))
    self.contentDict = json.loads(self.content)
    print str(self.contentDict)

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
      #cmd = "ip link add br0 type bridge"
      #output, error = runBashCmd(cmd)
      #print output

      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DeleteNetwork":
      #cmd = "ip link del br0"
      #output, error = runBashCmd(cmd)
      #print output

      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.CreateEndpoint":
      response = self.CreateEndpoint()
      print "response:", response
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write(response)
      pass
    if self.path == "/NetworkDriver.EndpointOperInfo":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.DeleteEndpoint":
      self.DeleteEndpoint()
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write("{ }")
      pass
    if self.path == "/NetworkDriver.Join":
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()

      response = {
                   "InterfaceName": {
                           "SrcName": self.interfaceName,
                           "DstPrefix": "boot" # '0' will be appended
                   },
                   "Gateway": self.gateway,
                   "GatewayIPv6": "",
                   "StaticRoutes": []
                 }
      self.wfile.write(json.dumps(response))
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
#  testHandler = myHandler("","","")
#  testHandler.setup()
#  print testHandler.CreateEndpoint()
#  testHandler.DeleteEndpoint()

  #Create a web server and define the handler to manage the
  #incoming request
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ' , PORT_NUMBER
	
  #Wait forever for incoming htto requests
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()


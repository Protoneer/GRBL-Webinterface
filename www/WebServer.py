import cgi
import serial

# Serial Config
#serialPort = '/dev/ttyAMA0'
serialPort = 'COM26'
serilaBaudRate = 9600

#Webserver Config
wwwPort = 91 
wwwHostName = ''
wwwHistoryFileName = 'history.txt' # Stores results from commands run



#from BaseHTTPServer import HTTPServer
from http.server import HTTPServer
#from SimpleHTTPServer import SimpleHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    print(self.path)
    if self.path == '/arduino':
      form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD':'POST'})
      code = form['code'].value
      addReturnChar = form['addReturnChar'].value
      
      print('Sent To Serial:', code)

      if addReturnChar == 'true' :
        arduino.write(bytes(code + '\r', 'UTF-8'))
      else :
        arduino.write(bytes(code, 'UTF-8'))
      
      from time import sleep
      sleep(0.02)
      # write to file
      f = open(wwwHistoryFileName,'a')
      
      out = ''
      while arduino.inWaiting() > 0:
	  
        out = out + arduino.readline().decode(encoding='UTF-8')
        sleep(0.02)

        #f.write(arduino.readline())
        #if addReturnChar == 'on' :
          #f.write('\r\n')
      f.write(out)
      f.close()
      
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.send_header('Access-Control-Allow-Origin', '*')
      self.end_headers()
      return
    return self.do_GET()

print("starting up....")
arduino = serial.Serial(serialPort, serilaBaudRate, timeout=1)
server = HTTPServer((wwwHostName, wwwPort), MyHandler).serve_forever()

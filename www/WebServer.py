import cgi
import serial
import re

# Serial Config
#serialPort = '/dev/ttyAMA0'
serialPort = 'COM26'
serilaBaudRate = 9600

#Webserver Config
wwwPort = 91 
wwwHostName = ''
wwwHistoryFileName = 'WWW/history.txt' # Stores results from commands run

#from BaseHTTPServer import HTTPServer
from http.server import HTTPServer
#from SimpleHTTPServer import SimpleHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler

def writeToFile(filename,stringToAppend):
    f = open(filename,'a')
    f.write(re.sub(r"\r", "", stringToAppend))
    f.close()

class MyHandler(SimpleHTTPRequestHandler):

  def do_POST(self):
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

      out = ''
      while arduino.inWaiting() > 0:
	  
        out = out + arduino.readline().decode(encoding='UTF-8')
        sleep(0.02)        

      writeToFile(wwwHistoryFileName,out)
	  
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.send_header('Access-Control-Allow-Origin', '*')
      self.end_headers()
      return
    return do_GET()

  def do_GET(self):
      if wwwHistoryFileName in self.path:
        print("Reading...")
        out = ''
        from time import sleep
        while arduino.inWaiting() > 0:
          out = out + arduino.readline().decode(encoding='UTF-8')
          sleep(0.02)        
        writeToFile(wwwHistoryFileName,out)

        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()	  
      else:
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()	  

    
				
print("starting up....")
print("Hosted @ " + wwwHostName + " Port : " + str(wwwPort))
arduino = serial.Serial(serialPort, serilaBaudRate, timeout=1)
server = HTTPServer((wwwHostName, wwwPort), MyHandler).serve_forever()

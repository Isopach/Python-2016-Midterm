#"client" side, using TCP
# this client will simply send a message to the server

import socket
import sys
import threading
import urllib2
import Queue
#Comparison of getting source code with the web service (socket) method and multithreading method

def __init__(self, urlz):
    self.urlz = urlz
countx = 0
urls = ["http://www.google.com", "http://www.yahoo.com"]
while countx < len(urls):
    x = urls[countx][7:]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((x, 80))
    sock.sendall("GET /\r\n") 
    #prints source code
    print sock.recv(4096)
    sock.close()
    countx +=1


def url(q,url):
   q.put(urllib2.urlopen(url).read())
   return "The definition of Q is: {0}".format(q,url) #decorator

q = Queue.Queue()

for u in urls:
    z = threading.Thread(target=url, args = (q,u))
    z.daemon = True #if main threads end, process also ends
    z.start()

s = q.get()
print s

#For decoration. q replaces the location of the tuple {0}
def url_deco(func):
    def func_wrapper(q, url):
        return "<p>{0}</p>".format(func(q,url))
    return func_wrapper
    
define_q = url_deco(url)

print define_q(q, urls[0])

#Demo of managed attributes that does practically nothing (init, getter & setter)
class url_list:
    def __init__(self, urlz):
        self.urlz = urlz

    @property
    def urlz(self):
        return self._urlz

    @urlz.setter
    def urlz(self, v):
        if not isinstance(v, str):
            raise TypeError('Invalid format')
        self._urlz = v
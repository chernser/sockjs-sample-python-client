from threading import Thread
import time
import httplib
import random
import string
import socket

def random_str(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for c in range(length))


""" SockJS Client class  """
class Client(Thread):
    TRANSPORT = "xhr_streaming"

    _wait_thread = 0
    _prefix = ""
    _host = ""
    _port = 80

    def __init__(self, prefix, host = "localhost", port = 80):
        self._prefix = prefix
        self._host = host
        self._port = port
        Thread.__init__(self)

    def connect(self):
        self.get_socket_info()
        self.start()

    def disconnect(self):
        pass

    def run(self):
        print ">>> "
        conn = httplib.HTTPConnection(self._host, self._port)
        self._r1 = str(random.randint(0, 1000))
        self._conn_id = random_str(8)
        url = '/'.join([self._prefix, self._r1, self._conn_id, 'xhr_streaming'])
        print "Connecting to URL: ", url
        conn.request('POST', url)
        response = conn.getresponse()
        print "connected: ", response.status
        sock = socket.fromfd(response.fileno(), socket.AF_INET, socket.SOCK_STREAM)
        data = 1
        while data:
            data = sock.recv(1)

            if data == 'o':
                print "Socket connected"
            if data == 'c':
                print "Socket disconnected"
                return
            if data == 'h':
                pass
            if data in ('m', 'a'):
                msg = sock.recv(1000)
                print "Message: ", msg

        time.sleep(0)
        print "server disconnected"


    def get_socket_info(self):
        conn = 0
        try:
            conn = httplib.HTTPConnection(self._host, self._port)
            print " Getting info from ", self._host, ":", self._port
            conn.request('GET', '/socket.io/info')
            response = conn.getresponse()
            print "INFO", response.status, response.reason, response.read()
        finally:
            if not conn: conn.close()

    def send(self, message):
        conn = httplib.HTTPConnection(self._host, self._port)
        url = '/'.join([self._prefix, self._r1, self._conn_id, 'xhr_send'])
        print "Send to: ", url

        conn.request('POST', url, "[" + message + "]", {'Content-Type': 'text/plain'})
        #print "Sent: ", conn.getresponse().status, conn.getresponse().reason
        return conn.getresponse().status in (200, 204)

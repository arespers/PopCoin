import sys
import socket


def __init__(self, maxpeers, serverport, myid=None, serverhost=None):
    self.debug = 0

    self.maxpeers = int(maxpeers)
    self.serverport = int(serverport)

    # If not supplied, the host name/IP address will be determined
    # by attempting to connect to an Internet host like Google.
    if serverhost:
        self.serverhost = serverhost
    else:
        self.__initserverhost()

    # If not supplied, the peer id will be composed of the host address
    # and port number
    if myid:
        self.myid = myid
    else:
        self.myid = '%s:%d' % (self.serverhost, self.serverport)

    # list (dictionary/hash table) of known peers
    self.peers = {}

    # used to stop the main loop
    self.shutdown = False

    self.handlers = {}
    self.router = None


# end constructor
def makeserversocket(self, port, backlog=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(backlog)
    return s


def mainloop(self):
    s = self.makeserversocket(self.serverport)
    s.settimeout(2)
    self.__debug('Server started: %s (%s:%d)'
                 % (self.myid, self.serverhost, self.serverport))

    while not self.shutdown:
        try:
            self.__debug('Listening for connections...')
            clientsock, clientaddr = s.accept()
            clientsock.settimeout(None)

            t = threading.Thread(target=self.__handlepeer, args=[clientsock])
            t.start()
        except KeyboardInterrupt:
            self.shutdown = True
            continue
        except:
            if self.debug:
                traceback.print_exc()
                continue
    # end while loop

    self.__debug('Main loop exiting')
    s.close()


# end mainloop method
host, port = clientsock.getpeername()
peerconn = BTPeerConnection(None, host, port, clientsock, debug=False)


def __handlepeer(self, clientsock):
    self.__debug('Connected ' + str(clientsock.getpeername()))

    host, port = clientsock.getpeername()
    peerconn = BTPeerConnection(None, host, port, clientsock, debug=False)

    try:
        msgtype, msgdata = peerconn.recvdata()
        if msgtype: msgtype = msgtype.upper()
        if msgtype not in self.handlers:
            self.__debug('Not handled: %s: %s' % (msgtype, msgdata))
        else:
            self.__debug('Handling peer msg: %s: %s' % (msgtype, msgdata))
            self.handlers[msgtype](peerconn, msgdata)
    except KeyboardInterrupt:
        raise
    except:
        if self.debug:
            traceback.print_exc()

    self.__debug('Disconnecting ' + str(clientsock.getpeername()))
    peerconn.close()

    # end handlepeer method

    def sendtopeer(self, peerid, msgtype, msgdata, waitreply=True):
        if self.router:
            nextpid, host, port = self.router(peerid)
        if not self.router or not nextpid:
            self.__debug('Unable to route %s to %s' % (msgtype, peerid))
            return None
        return self.connectandsend(host, port, msgtype, msgdata, pid=nextpid,
                                   waitreply=waitreply)

    # end sendtopeer method


def connectandsend(self, host, port, msgtype, msgdata, pid=None, waitreply=True):
    msgreply = []  # list of replies
    try:
        peerconn = BTPeerConnection(pid, host, port, debug=self.debug)
        peerconn.senddata(msgtype, msgdata)
        self.__debug('Sent %s: %s' % (pid, msgtype))

        if waitreply:
            onereply = peerconn.recvdata()
            while (onereply != (None, None)):
                msgreply.append(onereply)
                self.__debug('Got reply %s: %s' % (pid, str(msgreply)))
                onereply = peerconn.recvdata()
        peerconn.close()
    except KeyboardInterrupt:
        raise
    except:
        if self.debug:
            traceback.print_exc()

    return msgreply

# end connectsend method

from __future__ import print_function

#Imports to access nugget methods
import argparse
import hashlib
import sys
from getpass import getpass
#from Cryptodome.Cipher import AES

import sys
#sys.modules['Crypto'] = crypto
from crankycoin import *

# Import for the GUI
import Tkinter as tk
import random
import requests

# from config import *
# from node import NodeMixin
# from transaction import *
import socket 
ip = '10.0.2.15'
# print(ip)
public_key = config['user']['public_key']
fullnode = FullNode(ip, public_key)



def Main():
		host = '127.0.0.1'
		port = 57335

		s = socket.socket()
		s.bind((host, port))

		s.listen(1)
		c, addr = s.accept()
		# print(fullnode.add_node(host))
		print ("Got Conecttion From: " + str(addr))
		while True: 
				data =c.recv(1024)
				if not data:
						break
				print ("from connected user: " + str(data))
				data = str(data).upper()
				print ("sending: " + str(data))
				c.send(data)
		c.close()


if __name__ == '__main__':
	Main()

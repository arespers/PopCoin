# import socket
import __future__
from __future__ import print_function
import socket

# Imports to access nugget methods
import argparse
import hashlib
import sys
from getpass import getpass
from Cryptodome.Cipher import AES
from crankycoin import *

# Import for the GUI
import Tkinter as tk
import random
import requests

# from config import *
# from node import NodeMixin
# from transaction import *

def main(): 
		host = '10.0.2.15'
		port = 5000

		s = socket.socket()
		s.connect((host, port))

		fullnode.add_node()
		while message != 'q ':
				s.send(message)
				data = s.recv(1024)
				print ('Received from server' + str(data))
				message = raw_input("->")
		s.close()


if __name__ == '__main__':
	main() 
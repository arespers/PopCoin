#!/usr/bin/env python

from __future__ import print_function

import argparse
import hashlib
import socket
import sys
from getpass import getpass

import config
from Cryptodome.Cipher import AES
from wallet import Client
#from crankycoin import *

_PY3 = sys.version_info[0] > 2
if _PY3:
    raw_input = input


def client():
    helptext = '''
        Available commands:
        ===================
        balance <public key (optional)>
        send <destination> <amount>
        publickey
        privatekey
        history <public key (optional)>
        quit or exit
    '''
    encrypted = config['user']['encrypted_private_key']
    print(encrypted)
    if encrypted is None:
        print("\n\nNo private key provided. A new wallet will be generated for you...\n\n")
        client = Client()
    else:
        passphrase = getpass("Enter passphrase: ")
        encrypted = encrypted.decode('hex')
        nonce = encrypted[0:16]
        tag = encrypted[16:32]
        ciphertext = encrypted[32:]
        hashedpass = hashlib.sha256(passphrase).digest()
        cipher = AES.new(hashedpass, AES.MODE_EAX, nonce)
        try:
            private_key = cipher.decrypt_and_verify(ciphertext, tag)
            client = Client(private_key)
        except ValueError as ve:
            logger.warn('Invalid passphrase')
            print("\n\nInvalid passphrase\n\n")
            sys.exit(1)

    while True:
        cmd = raw_input("{} ({}) wallet > ".format(config['network']['name'], config['network']['ticker_symbol']))
        cmd_split = cmd.split()
        try:
            if cmd_split[0] == "balance":
                if len(cmd_split) == 2:
                    print(client.get_balance(cmd_split[1]))
                else:
                    print(client)
                    print(client.get_balance())
            elif cmd_split[0] == "send":
                if len(cmd_split) == 4:
                    print(client.create_transaction(cmd_split[1], float(cmd_split[2]), float(cmd_split[3])))
                else:
                    print("\nRequires destination, amount, and fee\n")
            elif cmd_split[0] == "publickey":
                print(client.get_public_key())
            elif cmd_split[0] == "privatekey":
                print(client.get_private_key())
            elif cmd_split[0] == "history":
                if len(cmd_split) == 2:
                    print(client.get_transaction_history(cmd_split[1]))
                else:
                    print(client.get_transaction_history())
            elif cmd_split[0] in ("quit", "exit"):
                sys.exit(0)
            else:  # help
                print(helptext)
        except IndexError:
            pass


def connect():
    host = '0.0.0.0'
    # host =  '137.198.12.190'
    port = 5000  # type: int

    ip = '137.198.12.99'
    # print(ip)
    public_key = config['user']['public_key']
    fullNode = FullNode(ip, public_key)
    s = socket.socket()
    s.bind((host, port))
    myaddr = '137.198.12.99'

    s.listen(1)
    c, addr = s.accept()
    # print(fullNode.add_node(host))
    # print ("Got Conecttion From: " + str(addr))
    c.send(myaddr)
    data = c.recv(1024)
    print("\n\n\n\n")
    print(fullNode.full_nodes)
    fullNode.add_node(data)
    print(fullNode.full_nodes)
    print("Node Added" + str(data))
    # data = s.recv(1024)
    # fullNode.add_node(data)
    # print(fullNode.add_node('10.0.2.15'))
    # c.send(fullNode.add_node('137.198.12.190'))
    # while True:
    #         data =c.recv(1024)
    #         if not data:
    #                 break
    #         print ("from connected user: " + str(data))
    #         data = str(data).upper()
    #         print ("sending: " + str(data))
    #         c.send(data)
    c.close()


def full():
    helptext = '''
        Available commands:
        ===================
        synchronize
        addnode <host>
        getnodes
        loadblockchain <path/to/blockchain>
        getblock <index (optional)>
        getblocks <start index (optional)> <stop index (optional)>
        quit or exit
    '''

    me = '137.198.12.190'
    ip = config['user']['ip']
    public_key = config['user']['public_key']
    if ip is None or public_key is None:
        print("\n\npublic key and IP must be provided.\n\n")
        sys.exit(1)
    else:
        print("\n\nfull node starting...\n\n")
        fullnode = FullNode(ip, public_key)
        # host1 = '10.0.2.15'
        # print(fullnode.add_node(host1))

    while True:
        cmd = raw_input("{} ({}) full node > ".format(config['network']['name'], config['network']['ticker_symbol']))
        cmd_split = cmd.split()
        try:
            if cmd_split[0] == "synchronize":
                print(fullnode.synchronize())
            elif cmd_split[0] == "addpeer":
                # connect() 
                host = '10.0.2.15'
                # host =  '137.198.12.190'
                port = 5000

                ip = '10.0.2.15'
                # print(ip)
                public_key = config['user']['public_key']
                # fullnode = FullNode(ip, public_key)
                s = socket.socket()
                s.bind((host, port))
                myaddr = '137.198.12.190'

                s.listen(1)
                c, addr = s.accept()
                # print(fullnode.add_node(host))
                # print ("Got Conecttion From: " + str(addr))
                c.send(myaddr)
                data = c.recv(1024)
                print("\n\n\n\n")
                print(fullnode.full_nodes)
                fullnode.add_node(data)
                config['network']['seed_nodes'].append(data)
                update()
                print(fullnode.full_nodes)
                print("Node Added" + str(data))
                # data = s.recv(1024)
                # fullnode.add_node(data)
                # print(fullnode.add_node('10.0.2.15'))
                # c.send(fullnode.add_node('137.198.12.190'))
                # while True:
                #         data =c.recv(1024)
                #         if not data:
                #                 break
                #         print ("from connected user: " + str(data))
                #         data = str(data).upper()
                #         print ("sending: " + str(data))
                #         c.send(data)
                c.close()
            elif cmd_split[0] == "addnode":
                if len(cmd_split) == 2:
                    print(fullnode.add_node(cmd_split[1]))
                else:
                    print("\nRequires host of node to add\n")
            elif cmd_split[0] == "getnodes":
                print(fullnode.full_nodes)
            elif cmd_split[0] == "loadblockchain":
                if len(cmd_split) == 2:
                    print(fullnode.load_blockchain(cmd_split[1]))
                else:
                    print("\nRequires path/to/blockchain\n")
            elif cmd_split[0] == "getblock":
                if len(cmd_split) == 2:
                    print(fullnode.blockchain.get_block_by_index(int(cmd_split[1])))
                else:
                    print(fullnode.blockchain.get_latest_block())
            elif cmd_split[0] == "getblocks":
                if len(cmd_split) == 3:
                    print(fullnode.blockchain.get_blocks_range(int(cmd_split[1]), int(cmd_split[2])))
                else:
                    print(fullnode.blockchain.get_all_blocks())
            elif cmd_split[0] in ("quit", "exit"):
                # fullnode.shutdown(True)
                sys.exit(0)
            else:  # help
                print(helptext)
        except IndexError:
            pass


def miner():
    helptext = '''
        Available commands:
        ===================
        synchronize
        addnode <host>
        getnodes
        loadblockchain <path/to/blockchain>
        getblock <index (optional)>
        getblocks <start index (optional)> <stop index (optional)>
        quit or exit
    '''
    ip = config['user']['ip']
    public_key = config['user']['public_key']
    if ip is None or public_key is None:
        print("\n\npublic key and IP must be provided.\n\n")
        sys.exit(1)
    else:
        print("\n\nmining node starting...\n\n")
        fullnode = FullNode(ip, public_key, mining=True)

    while True:
        cmd = raw_input("{} ({}) full node > ".format(config['network']['name'], config['network']['ticker_symbol']))
        cmd_split = cmd.split()
        try:
            if cmd_split[0] == "synchronize":
                print(fullnode.synchronize())
            elif cmd_split[0] == "addnode":
                if len(cmd_split) == 2:
                    print(fullnode.add_node(cmd_split[1]))
                else:
                    print("\nRequires host of node to add\n")
            elif cmd_split[0] == "getnodes":
                print(fullnode.full_nodes)
            elif cmd_split[0] == "loadblockchain":
                if len(cmd_split) == 2:
                    print(fullnode.load_blockchain(cmd_split[1]))
                else:
                    print("\nRequires path/to/blockchain\n")
            elif cmd_split[0] == "getblock":
                if len(cmd_split) == 2:
                    print(fullnode.blockchain.get_block_by_index(int(cmd_split[1])))
                else:
                    print(fullnode.blockchain.get_latest_block())
            elif cmd_split[0] == "getblocks":
                if len(cmd_split) == 3:
                    print(fullnode.blockchain.get_blocks_range(int(cmd_split[1]), int(cmd_split[2])))
                else:
                    print(fullnode.blockchain.get_all_blocks())
            elif cmd_split[0] in ("quit", "exit"):
                fullnode.shutdown(True)
                sys.exit(0)
            else:  # help
                print(helptext)
        except IndexError:
            pass

'''
def main(argv):
    parser = argparse.ArgumentParser(description='Starts a ' + config['network']['name'] + ' node')
    parser.add_argument('mode', metavar='type', nargs='?', default=None, help='client | full | miner')
    args = parser.parse_args()
    if args.mode == "client":
        client()
    elif args.mode == "full":
        full()
    elif args.mode == "miner":
        miner()
    else:
        print("Node operation mode not specified")


if __name__ == "__main__":
    main(sys.argv[1:])
'''

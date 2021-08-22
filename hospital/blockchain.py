# import libraries
import hashlib
from hashlib import sha256
import random
import binascii
import datetime
import collections
import json
from json import JSONEncoder
import time
import requests
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import rsa
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


#wallet = utilisateur
class Wallet:
    def __init__(self):
      random = Crypto.Random.new().read
      self._private_key = RSA.generate(1024, random)
      self._public_key = self._private_key.publickey()
      self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


class transaction:

    def __init__(self, ffrom, tto, data):
        self.ffrom      = ffrom
        self.tto        = tto
        self.data       = data
        self.time       = datetime.datetime.now()

    def to_dict(self):
        if self.ffrom == "ADMIN":
            identity = "ADMIN"
        else:
            identity = self.ffrom

        return collections.OrderedDict({
            'From': identity,
            'To': self.tto,
            'Data': self.data,
            'Time' : str(self.time)})

    def sign_transaction(self):
        private_key = self.ffrom._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

def display_transaction(transaction):
    #for transaction in transactions:
    dict = transaction.to_dict()
    print ("FROM: " + dict['_from'])
    print ('-----')
    print ("TO: " + dict['_to'])
    print ('-----')
    print ("data: " + str(dict['data']))
    print ('-----')
    print ("time: " + str(dict['time']))
    print ('-----')

from os import path

class Block:
    def __init__(self):
        self.index = ""
        self.verified_transactions = []
        self.hash = ""
        self.previous_block_hash = ""
        self.Time = datetime.datetime.now()
        self.Nonce = ""

    def saveTOjson(self):
        data = []
        filename = 'hospital/blocks.json'
        dict0     = {}
        dict0["index"]=self.index
        dict0["previousHash"]=self.previous_block_hash
        dict0["hash"]=self.hash
        dict0["Nonce"]=self.Nonce
        dict0["Time"]=self.Time.__str__()
        dict0["transaction"]=self.verified_transactions


        
        
        # Check if file exists
        if path.isfile(filename) is False:
            raise Exception("File not found")
 
        # Read JSON file
        with open(filename) as fp:
            data = json.load(fp)
 
        data.append(dict0)
 
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, 
                                indent=4,  
                                separators=(',',': '))
            

def mine(message):
    digest = "fff"
    n = 1
    check_mine = False
    while check_mine is False:
        digest = hashlib.sha256((message + str(n)).encode('ascii')).hexdigest()
        if digest[:4] == "0000":
            check_mine = True
        else:
            n +=1
    return n,digest
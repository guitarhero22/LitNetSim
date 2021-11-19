import os
import time
from .credentials import public_key, private_key

from solcx import compile_source
from web3 import Web3

contract_path = os.path.join(os.path.dirname(__file__), 'DAPP.sol')

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses


def connectWeb3():
    return Web3(Web3.HTTPProvider('http://127.0.0.1:1558 '))

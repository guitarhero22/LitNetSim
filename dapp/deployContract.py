import os
import time
from .credentials import public_key, private_key

from solc import compile_source
from web3 import *

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
    return Web3(IPCProvider(os.environ['HOME']+'/L2-DAPP/eth-test-net/data/geth.ipc', timeout=100000))
    
abi = None
def deployEmptyContract(contract_source_path, w3, account):
    global abi
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    abi = contract_interface3['abi']
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':1000000})
    return tx_hash

def deployContracts(w3, account):
    tx_hash3 = deployEmptyContract(empty_source_path, w3, account)

    
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    while ((receipt3 is None)) :
        time.sleep(1)
        receipt3 = w3.eth.getTransactionReceipt(tx_hash3)


    
    if receipt3 is not None:
        print("empty:{0}".format(receipt3['contractAddress']))
        return receipt3


empty_source_path = contract_path


w3 = connectWeb3()
w3.miner.start(1)
time.sleep(4)
receipt3 = deployContracts(w3, w3.eth.accounts[0])

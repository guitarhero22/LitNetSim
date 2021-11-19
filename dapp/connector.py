from web3 import *
from solc import compile_source
import os

# def sendEmptyLoopTransaction(address):
       
#     contract_source_path = os.environ['HOME']+'/HW3/emptyLoop.sol'
#     compiled_sol = compile_source_file(contract_source_path)

#     contract_id, contract_interface = compiled_sol.popitem()

#     sort_contract = w3.eth.contract(
#     address=address,
#     abi=contract_interface['abi'])
#     tx_hash = sort_contract.functions.runLoop().transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
#     return tx_hash

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

class EthConnector(object):
    w3 = Web3(IPCProvider(os.path.join(
                                        os.path.dirname(__file__),
                                        'geth.ipc',
                                        timeout=100000
                                    )
                        )
            )
    
    def __init__(self, address, contract_name="DAPP.sol"):
        self.contract_path = os.path.join(
            os.path.dirname(__file__),
            contract_name
        )
        self.contract_address = address
        self.compiled_sol = compile_source_file(self.contract_path)
        self.contract_id, self.contract_interface = self.compiled_sol.popitem()
        self.contract = EthConnector.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_interface['abi']
        )
    
    def register_user(self, user_id: int, user_name: str):
        contract = EthConnector.w3.eth.contract(
         
        )






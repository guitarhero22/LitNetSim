from web3 import *
from solcx import compile_source
import os
from .credentials import public_key, private_key
from .deployContract import compile_source_file, connectWeb3
import time

class DAPPConnector(object):
    w3 = connectWeb3()
    
    def __init__(self, contract_name="DAPP.sol"):
        self.contract_path = os.path.join(
            os.path.dirname(__file__),
            contract_name
        )
        self.account = DAPPConnector.w3.eth.accounts[0]
        self.compiled_sol = compile_source_file(self.contract_path)
        self.contract_id, self.contract_interface = self.compiled_sol.popitem()
        self.last_hash = None
    
    def deploy_dapp_contract(self):
        DAPPConnector.start_mining()
        tx_hash = DAPPConnector.w3.eth.contract(
            abi=self.contract_interface['abi'],
            bytecode=self.contract_interface['bin']
        ).constructor().transact({'txType':"0x0", 'from':self.account, 'gas':1000000})

        self.last_hash = tx_hash
        receipt = self.wait_for_transaction()


        print(type(receipt))

        if receipt is not None:
            self.contract_address = receipt['contractAddress']
            print(f"Contract address: {self.contract_address}") 


        DAPPConnector.stop_mining()
        self.contract = DAPPConnector.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_interface['abi']
        )

    @staticmethod
    def start_mining():
        DAPPConnector.w3.miner.start(1)
        time.sleep(4)
    
    @staticmethod
    def stop_mining():
        DAPPConnector.w3.miner.stop()

    def wait_for_transaction(self):

        if self.last_hash is None:
            raise Exception("No hash present to check")
        
    
        tx_hash = self.last_hash
        receipt = DAPPConnector.w3.eth.getTransactionReceipt(tx_hash)

        while receipt is None:
            time.sleep(1)
            receipt = DAPPConnector.w3.eth.getTransactionReceipt(tx_hash)

        return receipt
            

    def register_user(self, user_id: int, user_name: str):
        self.start_mining()
        tx_hash = self.contract.functions.registerUser(user_id, user_name).transact({'txType':"0x3", 'from':self.account, 'gas':2409638})
        self.last_hash =  tx_hash
        conn.wait_for_transaction()
        self.stop_mining()
    
    def create_acc(self, id1: int, id2: int, balance: float):
        self.start_mining()
        tx_hash = self.contract.functions.registerUser(id1, id2, balance).transact({'txType':"0x3", 'from':self.account, 'gas':2409638})
        self.last_hash = tx_hash
        conn.wait_for_transaction()
        self.stop_mining()

    def send_amount(self, id1: int, id2: int):
        self.start_mining()
        tx_hash = self.contract.functions.sendAmount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':2409638})
        self.last_hash = tx_hash
        conn.wait_for_transaction()
        self.stop_mining()

    def close_account(self, id1:int, id2: int):
        self.start_mining()
        tx_hash = self.contract.functions.closeAccount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':2409638})
        self.last_hash = tx_hash
        conn.wait_for_transaction()
        self.stop_mining()
    
    def get_successful_transactions(self):
        time.sleep(60)
        return self.contract.functions.getSuccessfulTransactions().call()


if __name__ == "__main__":
    print("Compiling contract")
    conn = DAPPConnector()
    print("Deploying Contract")
    conn.deploy_dapp_contract()
    print("Deployed")

    conn.register_user(1, "test1")
    conn.register_user(2, "test2")
    print(conn.get_successful_transactions())


    






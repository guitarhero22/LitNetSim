from web3 import Web3
from solcx import compile_source, set_solc_version
import os
from .credentials import public_key, private_key
import time
set_solc_version('0.4.25')

def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)

def connectWeb3():
    return Web3(Web3.HTTPProvider('http://127.0.0.1:1558'))

class DAPPConnector(object):
    w3 = connectWeb3()
    
    def __init__(self, contract_name="DAPP.sol"):
        self.start_mining()
        self.contract_path = os.path.join(
            os.path.dirname(__file__),
            contract_name
        )
        self.account = DAPPConnector.w3.eth.accounts[0]
        self.compiled_sol = compile_source_file(self.contract_path)
        
        self.contract_id, self.contract_interface = self.compiled_sol.popitem()
        self.last_hash = None
        self.unchecked_hashes = []
    
    def deploy_dapp_contract(self):
        tx_hash = DAPPConnector.w3.eth.contract(
            abi=self.contract_interface['abi'],
            bytecode=self.contract_interface['bin']
        ).constructor().transact({'txType':"0x0", 'from':self.account, 'gas':10000000})

        self.unchecked_hashes.append(tx_hash)
        receipt = self.check_unchecked_transactions()[-1]


        if receipt is not None:
            self.contract_address = receipt['contractAddress']
            print(f"Contract address: {self.contract_address}") 


        self.contract = DAPPConnector.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_interface['abi']
        )

    @staticmethod
    def start_mining():
        DAPPConnector.w3.geth.miner.start(1)
        time.sleep(1)
    
    @staticmethod
    def stop_mining():
        DAPPConnector.w3.geth.miner.stop()

    def wait_for_transaction(self, hash):
        return DAPPConnector.w3.eth.wait_for_transaction_receipt(hash)
            

    def register_user(self, user_id: int, user_name: str):
        tx_hash = self.contract.functions.registerUser(user_id, user_name).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.last_hash =  tx_hash
        receipt = self.wait_for_transaction(tx_hash)
    
    def create_acc(self, id1: int, id2: int, balance: float):
        tx_hash = self.contract.functions.createAcc(id1, id2, balance).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.last_hash = tx_hash
        receipt = self.wait_for_transaction(tx_hash)

    def send_amount(self, id1: int, id2: int):
        tx_hash = self.contract.functions.sendAmount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.last_hash = tx_hash
        receipt = self.wait_for_transaction(tx_hash)

    def close_account(self, id1:int, id2: int):
        tx_hash = self.contract.functions.closeAccount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.last_hash = tx_hash
        receipt = self.wait_for_transaction(tx_hash)

    def check_unchecked_transactions(self):
        receipts = []
        for tx_hash in self.unchecked_hashes:
            receipt = self.wait_for_transaction(tx_hash)
            receipts.append(receipt)
        
        time.sleep(1)

        self.unchecked_hashes = []

        return receipts


    def get_successful_transactions(self):
        time.sleep(5)
        return self.contract.functions.getSuccessfulTransactions().call()

if __name__ == "__main__":
    print("Compiling contract")
    conn = DAPPConnector()
    print("Deploying Contract")
    conn.deploy_dapp_contract()
    print("Deployed")
    conn.register_user(1, "test1")
    conn.register_user(2, "test2")
    conn.register_user(3, "test3")
    conn.register_user(4, "test4")
    conn.register_user(5, "test5")
    conn.register_user(6, "test6")
    conn.register_user(7, "test7")
    conn.register_user(8, "test8")
    time.sleep(5)

    conn.create_acc(1, 2, 10)
    conn.create_acc(2, 3, 10)
    conn.create_acc(3, 4, 10)
    conn.create_acc(4, 5, 10)
    conn.create_acc(5, 6, 10)
    conn.create_acc(6, 7, 10)
    conn.create_acc(7, 8, 10)
    time.sleep(5)

    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(0.5)
    conn.send_amount(1, 8)
    time.sleep(5)
    print(conn.get_successful_transactions())


    






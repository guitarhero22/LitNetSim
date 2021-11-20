from web3 import Web3
from solcx import compile_source, set_solc_version
import os
import time
set_solc_version('0.4.25')

def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)

class DAPPConnector(object):
    '''DAPPConnector class is the connector that holds the connection between
    python script and the DAPP
    
    Attributes
    ----------
    w3: Web3
        Static variable that holds a connection to the Ethereum blockchain
    contract_path: str
        Holds the contract path
    account: str
        Stores the account name
    compiled_sol: Dict
        Stores the output from the compiler for the contract
    contract_id: str
        Stores the contract ID
    contract_interface: Dict
        Stores the contract interface
    unchecked_hashes: list[str]
        List of transaction hashes whose receipts haven't been asked for yet
    num_bulk_transaction: int
        Number of transactions after which we check for the
        receipts of unchecked transaction hashes

    
    Methods
    -------
    
    start_mining()
        A static method to start mining on the ethereum chain
    stop_mining()
        A static method to stop mining on gthe ethereum chain
    wait_for_transaction_receipt(hash: str)
        A static method that provides the transaction receipt
    deploy_dapp_contract()
        Deploys the smart contract for the DAPP
    register_user(user_id: int, user_name: str)
        Wrapper function for registerUser() smart contract function
    create_acc(id1: int, id2: int, balance: float)
        Wrapper function for createAcc() smart contract function
    send_amount(id1: int, id2: int)
        Wrapper function for sendAmount() smart contract function
    close_account(id1:int, id2: int)
        Wrapper function for closeAccount() smart contract function    
    check_unchecked_transactions()
        Obtains the receipts for the unchecked transactions
    get_successful_transactions()
        Wrapper function for the getter function for the number of successful transactions

    '''

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:1558'))
    
    @staticmethod
    def start_mining():
        '''Starts mining on the ethereum chain'''
        DAPPConnector.w3.geth.miner.start(1)
        time.sleep(1)
    
    @staticmethod
    def stop_mining():
        '''stops mining on the ethereum chain'''
        DAPPConnector.w3.geth.miner.stop()

    @staticmethod
    def wait_for_transaction_receipt(hash: str):
        '''Obtains the transaction receipt
        
        Parameters
        ----------
        hash: str
            Transaction hash whose receipt is needed
        
        Returns
        -------
        TxReceipt
            The transaction receipt'''
        return DAPPConnector.w3.eth.wait_for_transaction_receipt(hash)

    def __init__(self, contract_name: str="DAPP.sol", num_bulk_transaction: int=100):
        '''
        Constructor for the DAPPConnector

        Parameters
        ----------
        contract_name: str, optional
            file name of the smart contract. The smart contract must be in the
            same diretory as that of connector.py
        num_bulk_transaction: int
            Number of transactions after which we check for receipts
        '''
        DAPPConnector.start_mining()
        self.contract_path = os.path.join(
            os.path.dirname(__file__),
            contract_name
        )
        self.account = DAPPConnector.w3.eth.accounts[0]
        self.compiled_sol = compile_source_file(self.contract_path)
        
        self.contract_id, self.contract_interface = self.compiled_sol.popitem()
        self.unchecked_hashes = []

        self.num_bulk_transaction = num_bulk_transaction
    
    def deploy_dapp_contract(self):
        '''Deploys the DAPP Contract to the ethereum chain'''
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

    
    def __update_transaction_status(self, tx_hash: str):
        self.unchecked_hashes.append(tx_hash)

        if len(self.unchecked_hashes) >= self.num_bulk_transaction:
            self.check_unchecked_transactions()

    
    def register_user(self, user_id: int, user_name: str):
        '''Wrapper function for the registerUser() smart contract function
        
        Parameters
        ----------
        user_id: int
            The user ID for the new user
        user_name: str
            The user name of the new user'''
        tx_hash = self.contract.functions.registerUser(user_id, user_name).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.__update_transaction_status(tx_hash)    
    
    def create_acc(self, id1: int, id2: int, balance: int):
        '''Wrapper function for the createAcc() smart contract function
        
        Parameters
        ----------
        id1: int
            The user ID for the first user
        id2: int
            The user ID of the second user
        balance: int
            The balance to be added to the account'''
        tx_hash = self.contract.functions.createAcc(id1, id2, balance).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.__update_transaction_status(tx_hash)    


    def send_amount(self, id1: int, id2: int):
        '''Wrapper function for the sendAmount() smart contract function

        Parameters
        ----------
        id1: int
            The user ID for the user sending the money
        id2: int
            The user name of the user receiving the money'''
        tx_hash = self.contract.functions.sendAmount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.__update_transaction_status(tx_hash)    


    def close_account(self, id1:int, id2: int):
        '''Wrapper function for closing an account between 2 users
        
        Parameters
        ----------
        id1: int
            The user ID of the first user
        id2: int
            The user ID of the second user'''
        tx_hash = self.contract.functions.closeAccount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':10000000})
        self.__update_transaction_status(tx_hash)    


    def check_unchecked_transactions(self):
        '''Checks for the receipts of transactions'''
        receipts = []
        for tx_hash in self.unchecked_hashes:
            receipt = DAPPConnector.wait_for_transaction_receipt(tx_hash)
            receipts.append(receipt)
        
        time.sleep(1)

        self.unchecked_hashes = []

        return receipts


    def get_successful_transactions(self):
        '''Obtains the number of successful transactions using the 
        smart contract getter function getSuccessfulTransactions()
        
        Returns
        -------
        int
            Number of successful transactions'''
        return self.contract.functions.getSuccessfulTransactions().call()






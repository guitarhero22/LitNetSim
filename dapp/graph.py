import numpy as np
import graphviz
from .connector import DAPPConnector
import time

class Graph(object):
    '''The Graph class is the simulator that generates the graph based on
    Barabasi-Albert model to follow power law, and sends the transactions to the
    DAPP via the DAPP connector
    
    Attributes
    ----------
    num_nodes: int
        Number of nodes in the graph (default 100)
    num_initial_nodes;
        Number of initial connected nodes in the Barabasi-Albert Algorithm (default 2)
    adj_matrix: list[list[int]]
        Adjacency matrix for the graph
    balance:list[dict{int: float}]
        Balance assigned to a node in an account
    deg: np.ndarray(int)
        Degree of each node
    edges: int
        Total number of edges
    m: int
        The m-value for the Barabasi-Albert Model (defualt 2)
    exp_mean: float, optional
        The mean to be used for the exponential distribution, in order to distribute balance (default 10)
    
    Methods
    -------
    init_nodes()
        Generates Users in the DAPP
    barabasi_algorithm()
        Generates the graph based on Barabasi-Albert model and generates the accounts in the DAPP
    generate_graph()
        Generates the visualization of graph using graphviz
    transactions(num_transactions: int=1000, num_steps: int=100)
        Generates the transactions that need to be simulated
    close_accounts()
        Closes all accounts'''

    def __init__(self, num_nodes: int=100, m: int=2,  num_initial_nodes: int=2, exp_mean: float=10):
        '''Constructor for the Graph class

        Parameters
        ----------
        num_nodes: int, optional
            The number of nodes in the graph
        m: int, optional
            The m-value for the Barabasi-Albert Model
        num_initial_nodes: int, optional
            The number of initial nodes that are connected in the Barabasi-Albert model
        exp_mean: float, optional
            The mean to be used for the exponential distribution, in order to distribute balance'''

        self.num_nodes = num_nodes
        self.num_initial_nodes = num_initial_nodes
        self.adj_matrix = [[] for i in range(self.num_nodes)]
        self.balance = [{} for i in range(self.num_nodes)]
        self.deg = np.zeros(self.num_nodes)
        self.edges = 0
        self.m = m
        self.exp_mean = exp_mean
        self.conn = DAPPConnector()
        self.conn.deploy_dapp_contract()
    
    def init_nodes(self):
        '''Generates users in the DAPP'''
        for i in range(self.num_nodes):
            self.conn.register_user(i, f"node {i}")
        
    def __init_barabasi(self):
        '''Connects the initial nodes for the Barabasi-Albert model'''
        self.adj_matrix = [[] for i in range(self.num_nodes)]
        self.balance = [{} for i in range(self.num_nodes)]
        self.deg = np.zeros(self.num_nodes)
        self.edges = 0
    
        for i in range(self.num_initial_nodes):
            for j in range(i+1, self.num_initial_nodes):
                self.__add_edge(i, j)


    def __add_edge(self, i: int, j: int):
        '''Adds and edge to the graph, and creates an account in the DAPP
        
        Parameters
        ----------
        i: int
            The first node
        j: int
            The second node'''

        if i in self.adj_matrix[j] and j in self.adj_matrix[i]:
            return
        if i in self.adj_matrix[j] and j not in self.adj_matrix[i]:
            raise Exception(f"{i} {j} incomplete graph")
        if i not in self.adj_matrix[j] and j in self.adj_matrix[i]:
            raise Exception(f"{j} {i} incomplete graph 2")

        self.adj_matrix[i].append(j)
        self.adj_matrix[j].append(i)

        self.deg[i] += 1
        self.deg[j] += 1

        self.edges += 1
        bal = np.random.exponential(self.exp_mean)

        # Since we do not have support for float, we will convert total balance as
        # the closest even number
        bal = int(round(bal))
        if bal%2 == 1:
            bal += 1

        self.conn.create_acc(int(i), int(j), int(bal))

        self.balance[i][j] = bal/2
        self.balance[j][i] = bal/2


    def __assign_edges_to_node_barabasi(self, new_node: int):
        '''Adds edges to a new node in the Barabasi-Albert model
        
        Parameters
        ----------
        new_node: int
            The new node being added to the graph'''
        old_nodes_adj = []
        prob = self.deg/(2*self.edges)
        prob = prob[:new_node]

        count_edges = 0
        while count_edges < self.m:
            node = np.random.choice(np.arange(new_node), p=prob)
            if node not in old_nodes_adj:
                count_edges += 1
                old_nodes_adj.append(node)
        
        for node in old_nodes_adj:
            self.__add_edge(node, new_node)
        

    def barabasi_algorithm(self):
        '''Generates a connected graph based on the Barabasi-Albert model'''
        self.__init_barabasi()
        for new_node in range(self.num_initial_nodes, self.num_nodes):
            self.__assign_edges_to_node_barabasi(new_node)
        self.conn.check_unchecked_transactions()
    
    def generate_graph(self):
        '''Generates a graphviz visualization for the graph'''
        dot = graphviz.Graph(name="Balance graph")
        
        for i in range(self.num_nodes):
            dot.node(str(i))
        
        for node1 in range(self.num_nodes):
            for node2 in self.adj_matrix[node1]:
                if node1 > node2:
                    continue
                dot.edge(
                    str(node1),
                    str(node2),
                    str(self.balance[node1][node2] + self.balance[node2][node1])
                )
        
        dot.render('result/payment-channel.gv', view=False)
    
    def __transact(self):
        '''Generates a random transaction ie. send 1 coin, and sends the transaction to the DAPP'''
        s1 = np.random.randint(0, self.num_nodes)
        s2 = s1
        while s2 == s1:
            s2 = np.random.randint(0, self.num_nodes)
        
        self.conn.send_amount(int(s1), int(s2))
    
    def transactions(self, num_transactions: int=1000, num_steps: int=100):
        '''Generates random transactions ie.send 1 coin to test the number of successful transfers
        
        Parameters
        ----------
        num_transactions: int, optional
            The number of money transfers
        
        num_steps: int, optional
            The number of steps after which we check for the number of successful money transfers
            
        
        Returns
        -------
        list[float]
            A list of the ratio of successful transactions to total transactions'''

        succ_percentage = []

        for i in range(num_transactions):
            
            self.__transact()
            if i % num_steps == num_steps -1:
                print(f"Step {i+1}")
                self.conn.check_unchecked_transactions()
                time.sleep(5)
                print(f"% Successful transactions = {100*self.conn.get_successful_transactions()/(i+1)}")

                succ_percentage.append(self.conn.get_successful_transactions()/(i+1))
        return succ_percentage
    

    def close_acconts(self):
        '''Closes all the accounts'''
        for i in range(self.num_nodes):
            for j in self.adj_matrix[i]:
                if j < i:
                    continue
                self.conn.close_account(i, j)
        
        print("Closed all accounts")

import numpy as np
import graphviz

class Graph(object):

    def __init__(self, m=2, num_nodes=100, num_initial_nodes=2, exp_mean=10):
        self.num_nodes = num_nodes
        self.num_initial_nodes = num_initial_nodes
        self.adj_matrix = [[] for i in range(self.num_nodes)]
        self.balance = [{} for i in range(self.num_nodes)]
        self.deg = np.zeros(self.num_nodes)
        self.edges = 0
        self.m = m
        self.exp_mean = exp_mean
        
    def __init_barabasi(self):

        self.adj_matrix = [[] for i in range(self.num_nodes)]
        self.balance = [{} for i in range(self.num_nodes)]
        self.deg = np.zeros(self.num_nodes)
        self.edges = 0
    
        for i in range(self.num_initial_nodes):
            for j in range(i+1, self.num_initial_nodes):
                print(f"I, j, {i} {j}")
                self.__add_edge(i, j)


    def __add_edge(self, i: int, j: int):

        if i in self.adj_matrix[j] and j in self.adj_matrix[i]:
            return
        if i in self.adj_matrix[j] and j not in self.adj_matrix[i]:
            raise Exception(f"{i} {j} incomplete graph")
        if i not in self.adj_matrix[j] and j in self.adj_matrix[i]:
            raise Exception(f"{j} {i} incomplete graph 2")

        self.adj_matrix[i].append(j)
        print(self.adj_matrix)
        self.adj_matrix[j].append(i)
        print(self.adj_matrix)

        self.deg[i] += 1
        self.deg[j] += 1

        self.edges += 1

        bal = np.random.exponential(self.exp_mean)
        self.balance[i][j] = bal/2
        self.balance[j][i] = bal/2


    def __assign_edges_to_node_barabasi(self, new_node: int):
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
            print(self.adj_matrix[new_node])
            self.__add_edge(node, new_node)

    def barabasi_algorithm(self):
        self.__init_barabasi()
        for new_node in range(self.num_initial_nodes, self.num_nodes):
            self.__assign_edges_to_node_barabasi(new_node)
    
    def get_adj_matrix(self):
        return self.adj_matrix
    
    def get_balance(self):
        return self.balance

    
    def generate_graph(self):
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
        
        dot.render('data/payment-channel.gv', view=False)
    
    def transact(self):
        s1 = np.random.randint(0, self.num_nodes)
        s2 = s1
        while s2 == s1:
            s2 = np.random.randint(0, self.num_nodes)
    
    def transaction(self):
        pass
        


        



if __name__ == "__main__":
    graph = Graph(num_nodes=20)

    graph.barabasi_algorithm()
    graph.generate_graph()
    pass


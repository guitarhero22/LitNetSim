from .graph import Graph
import pickle
from matplotlib import pyplot as plt
import numpy as np
def generate_success_chart(result: list, num_transaction: int=1000, num_steps: int=100):
    x = np.arange(num_steps, num_transaction+1, num_steps)
    plt.plot(x, result)
    
    plt.xlabel("Number of transactions")
    plt.ylabel("Ratio of successful transactions to total transactions")
    plt.title("Ratio of successful to total transactions VS Number of transactions")
    plt.show()

if __name__ == "__main__":
    print("Deploying Contract")
    graph = Graph(m=3)
    print("Initializing nodes")
    graph.init_nodes()
    print("Generating graph")
    graph.barabasi_algorithm()
    print("Generating Transactions")
    succ_percentage = graph.transactions()
    with open("result/result.pkl", "wb") as fp:   #Pickling
        pickle.dump(succ_percentage, fp)
    generate_success_chart(succ_percentage)
    graph.generate_graph()

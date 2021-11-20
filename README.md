# L2-DAPP
Layer 2 DAPP on top of blockchain

## Compiler And Run

- Install geth v1.9.3, easiest way is to use prebuild binaries available [here](https://geth.ethereum.org/downloads/)
- Install python3.8
- Create a virtual environment
    ```python3 -m venv ./.dapp-venv```
- Activate virtual environment
    ```source ./.dapp-venv/bin/activate```
- Install python packages from requirements.txt
    ```pip install -r requirements.txt```
- Run the following command to install solc 0.4.25
    ```python pysolc-installation.py```
- In order to start the node
    ```sh eth-test-net/runEthereumNode.sh```
- Finally, in order to run the simulation
    ```python -m dapp.main```
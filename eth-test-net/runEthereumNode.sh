# !/bin/bash
cd eth-test-net
rm -r data/geth/chaindata/;
rm -r data/geth/lightchaindata/;
rm -r data/geth/nodes/;
rm -r data/geth/ethash/;
rm data/geth/LOCK;
rm data/geth/transactions.rlp;
sleep 2
$HOME/geth-dir/geth --datadir data/ --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt init genesis.json
gnome-terminal --geometry 90x25+1300+1550 -- bash startIpc.sh 1
$HOME/geth-dir/geth --datadir data/ --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0x8bF1384286f068058c41e136EB25451F95158722 --password password.txt
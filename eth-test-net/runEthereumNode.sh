# !/bin/bash
cd eth-test-net
rm -rf data
sleep 2
mkdir data
geth --datadir data --networkid=2310 init genesis.json
geth --datadir data --rpc --rpcapi "eth,net,web3,debug,miner,admin,personal" --networkid=2310 --syncmode full --gcmode archive --nodiscover --verbosity 5 --allow-insecure-unlock --mine --etherbase 0x76EB2f0d9C5f00292a47438a32a2b256003419C5
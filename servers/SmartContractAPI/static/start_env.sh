#!/bin/bash

anvil
forge create --rpc-url http://127.0.0.1:8545 --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 ~/facultate/thesis/BlockchainedSupplychain/contracts/src/SCContract.sol:SC

from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3


#  until https://youtu.be/M576WGiDBdQ?t=33186
# get ILendingPool.sol code and fixing the imports 

# untill here https://youtu.be/M576WGiDBdQ?t=32552
# using WETH erc20 tokens with AAVE

# 0.1
amount = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    # get weth_token address
    erc20_address = config["networks"][network.show_active()]["weth_token"] 
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # now to deposit the weth into the lending pool.
    lending_pool = get_lending_pool()
    # approve sending out ERC20 tokens / weth
    # need an approve function
    approve_erc20(amount, lending_pool.address, erc20_address, account)


# until here:https://youtu.be/M576WGiDBdQ?t=33476
#   approve function approve(address spender, uint256 value) external returns (bool success);

def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    # need abi and address of the contract
    # we could create the interface ourselves, by going to eips.ethereum.org and put all the functions of the erc20 token standard into our interface.
    # or we can copy the interface from patrick's github
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")


def get_lending_pool():
    #ABI => interfaces/ILendingPoolAddressesProvider.sol
    #Address => get from aave documentation (https://docs.aave.com/developers/deployed-contracts/deployed-contracts)
    # if we know that we're just working with a few functions, we can create our own interface (e.g. ILendingPoolAddressProvider.sol)
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
 
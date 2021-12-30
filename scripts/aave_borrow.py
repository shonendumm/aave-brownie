from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth


#  until https://youtu.be/M576WGiDBdQ?t=33186
# get ILendingPool.sol code and fixing the imports 

# untill here https://youtu.be/M576WGiDBdQ?t=32552
# using WETH erc20 tokens with AAVE

def main():
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # now to deposit the weth
    # need ABI and address
    lending_pool = get_lending_pool()
    print(lending_pool)

def get_lending_pool():
    #ABI => interfaces/ILendingPoolAddressesProvider.sol
    #Address => get from aave documentation (https://docs.aave.com/developers/deployed-contracts/deployed-contracts)
    # if we know that we're just working with a few functions, we can create our own interface (e.g. ILendingPoolAddressProvider.sol)
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
 
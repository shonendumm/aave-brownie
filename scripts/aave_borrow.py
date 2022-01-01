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
    # deposit the weth into the lending pool but need to approve first
    lending_pool = get_lending_pool()
    # approve sending out ERC20 tokens / weth
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(erc20_address, amount, account.address, 0, {"from": account})
    tx.wait(1) # use wait when we make a state change
    print("Deposited!")
    # how much did we deposit?
    # aave has a getUserAccountData function in lending pool / https://docs.aave.com/developers/the-core-protocol/lendingpool#getuseraccountdata
    (available_borrow_eth, total_debt_eth) = get_borrowable_data(lending_pool, account)
    # https://youtu.be/M576WGiDBdQ?t=34110 



# https://youtu.be/M576WGiDBdQ?t=33833 until here
def get_borrowable_data(lending_pool, account):
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_threshold, ltv, health_factor ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    print(f"You have deposited total collateral eth: {total_collateral_eth}")
    print(f"Total debt eth: {total_debt_eth}")
    print(f"You can borrow available borrow eth: {available_borrow_eth}")
    print(f"The health factor is {health_factor}")
    return( float(available_borrow_eth), float(total_debt_eth))



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
    # lending pool address provider provides address of lending pool
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
 
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

    print("Depositing into lending pool...")
    tx = lending_pool.deposit(erc20_address, amount, account.address, 0, {"from": account})
    tx.wait(1) # use wait when we make a state change
    print("Deposited!")
    # how much did we deposit?
    # aave has a getUserAccountData function in lending pool / https://docs.aave.com/developers/the-core-protocol/lendingpool#getuseraccountdata
    # (available_borrow_eth, total_debt_eth) = get_borrowable_data(lending_pool, account)
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    
    # Dai in terms of ETH
    dai_eth_price = get_asset_price("dai_eth_price_feed")


    # borrow_from_lendingPool(lending_pool)
    # get_borrowable_data(lending_pool, account)

def get_asset_price(price_feed_address):
    price_feed_address = config["networks"][network.show_active()][price_feed_address]
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1] 
    converted_price = Web3.fromWei(latest_price, 'ether')
    print(f"1 dai is equal to {converted_price}")
    return float(converted_price) # returned by .sol as int256



def borrow_from_lendingPool(lending_pool):
    # 0.1 Ethereum = 370.304191 Dai (DAI) 
    borrow_amount = 300 * 10 ** 18 # 18 decimals for Dai token contract
    asset = config["networks"][network.show_active()]["dai_token"]
    print("Borrowing from pool")
    account = get_account()
    lending_pool = lending_pool
    tx = lending_pool.borrow(asset, borrow_amount, 1, 0, account, {"from": account})
    tx.wait(1)
    borrow_amount = Web3.fromWei(borrow_amount, "ether")
    print(f"Borrowed {borrow_amount} of Dai from lending pool!")


# https://youtu.be/M576WGiDBdQ?t=33833 until here
def get_borrowable_data(lending_pool, account):
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_threshold, ltv, health_factor ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    print(f"You have deposited total collateral eth: {total_collateral_eth}")
    print(f"Total debt eth: {total_debt_eth}")
    print(f"You can borrow available borrow eth: {available_borrow_eth}")
    print(f"LTV is {ltv}")
    calculate_health_factor(total_collateral_eth, current_liquidation_threshold, total_debt_eth)
    return( float(available_borrow_eth), float(total_debt_eth))


# Health factor = (total collateral in eth * liquidation threshold) / total borrows in eth
def calculate_health_factor(total_collateral_eth, current_liquidation_threshold, total_debt_eth):
    total_collateral_eth = float(total_collateral_eth)
    current_liquidation_threshold = float(current_liquidation_threshold) / 10000
    total_debt_eth = float(total_debt_eth)
    if total_debt_eth == 0:
        health_factor = total_collateral_eth * current_liquidation_threshold
    else:
        health_factor = (total_collateral_eth * current_liquidation_threshold) / total_debt_eth
    print(f"Your health factor is {health_factor}")



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
 
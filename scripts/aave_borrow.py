from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3




# 0.1
AMOUNT = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    # get weth_token address
    erc20_address = config["networks"][network.show_active()]["weth_token"] 
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # deposit the weth into the lending pool but need to approve first
    lending_pool = get_lending_pool()
    print(f"Lending pool address is {lending_pool.address}")

    # approve sending out ERC20 tokens / weth
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)

    print("Depositing into lending pool...")
    tx = lending_pool.deposit(erc20_address, AMOUNT, account.address, 0, {"from": account})
    tx.wait(1) # use wait when we make a state change
    print("Deposited!")
    # how much did we deposit?
    # aave has a getUserAccountData function in lending pool / https://docs.aave.com/developers/the-core-protocol/lendingpool#getuseraccountdata

    borrowable_eth, total_debt_eth = get_borrowable_data(lending_pool, account)
    
    # Dai in terms of ETH (0.00026691243)
    dai_eth_price = get_asset_price("dai_eth_price_feed")
    # 100% or 95% of borrowable amount, just change 1 or 0.95
    borrowable_dai = (borrowable_eth * 0.95) / dai_eth_price 
    print(f"You can borrow {borrowable_dai} Dai")
    borrow_from_lendingPool(lending_pool, borrowable_dai, "dai_token")
    borrowable_eth2, total_debt_eth2 = get_borrowable_data(lending_pool, account)
    # Repay debt 
    repay_all(AMOUNT, lending_pool, account, "dai_token")
    get_borrowable_data(lending_pool, account)

# similar to borrow, we need to approve on the asset token first
# https://youtu.be/M576WGiDBdQ?t=34929
def repay_all(amount, lending_pool, account, token_name):
    borrowed_token_address = config["networks"][network.show_active()][token_name]
    # approve dai_token for repayment
    approve_erc20(
        Web3.toWei(amount, "ether"), 
        lending_pool.address, 
        borrowed_token_address, 
        account)
    print("Repaying debt...")
    repay_tx = lending_pool.repay(borrowed_token_address, amount, 1, account.address, {"from": account})
    repay_tx.wait(1)
    print(f"Repaid {repay_tx} in ETH!")



def get_asset_price(price_feed_address):
    price_feed_address = config["networks"][network.show_active()][price_feed_address]
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1] 
    converted_price = Web3.fromWei(latest_price, 'ether')
    print(f"1 dai is equal to {converted_price}")
    return float(converted_price) # returned by .sol as int256



def borrow_from_lendingPool(lending_pool, amount, token):
    account = get_account()
    borrow_amount = amount * 10 ** 18 # 18 decimals for Dai token contract
    asset = config["networks"][network.show_active()][token]
    print("Borrowing from pool")
    borrow_tx = lending_pool.borrow(asset, borrow_amount, 1, 0, account, {"from": account})
    borrow_tx.wait(1)
    borrow_amount = Web3.fromWei(borrow_amount, "ether")
    print(f"Borrowed {borrow_amount} of Dai from lending pool!")


def get_borrowable_data(lending_pool, account):
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_threshold, ltv, health_factor ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    print(f"You have deposited total collateral eth: {total_collateral_eth}")
    print(f"Total debt in eth: {total_debt_eth}")
    print(f"You can borrow available borrow eth: {available_borrow_eth}")
    print(f"LTV is {ltv}")
    print(f"Health Factor: {health_factor}")
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
    print(f"Your calculated health factor is {health_factor}")





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
 


 #  https://youtu.be/M576WGiDBdQ?t=33186
# get ILendingPool.sol code and fixing the imports 

# https://youtu.be/M576WGiDBdQ?t=32552
# using WETH erc20 tokens with AAVE

# until here:https://youtu.be/M576WGiDBdQ?t=33476
#   approve function approve(address spender, uint256 value) external returns (bool success);
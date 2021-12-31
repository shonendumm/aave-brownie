from scripts.helpful_scripts import get_account
from brownie import interface, config, network

def main():
    get_weth()

# We interact with the WETH contract to change ETH to WETH (erc20)
# then we can use WETH to interact with AAVE
def get_weth():
    """
    Mints WETH by depositing ETH
    """
    # To interact with a contract, we need its ABI and address
    # untill here https://youtu.be/M576WGiDBdQ?t=32211
    account = get_account()
    # because we know that we're interacting only on Kovan net here, we're not using get_contract()
    # interface.IWeth => abi (copied from .sol file provided on tutorial's github; we can probably copy from the original)
    # weth_token => address
    # hence we can call the deposit function of the contract
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1*10**18})
    tx.wait(1)
    print(f"Received 0.1 WETH!")
    return tx



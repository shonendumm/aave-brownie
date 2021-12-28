from scripts.helpful_scripts import get_account
from brownie import interface, config, network

def main():
    get_weth()

def get_weth():
    """
    Mints WETH by depositing ETH
    """
    # Need ABI
    # Need Address
    # untill here https://youtu.be/M576WGiDBdQ?t=32211
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1*10**18})
    print(f"Received 0.1 WETH!")
    return tx



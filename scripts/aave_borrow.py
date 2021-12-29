from scripts.helpful_scripts import get_account
from brownie import network, config
from scripts.get_weth import get_weth

# untill here https://youtu.be/M576WGiDBdQ?t=32552
# using WETH erc20 tokens with AAVE

def main():
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
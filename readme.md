No smart contracts, just interacting with other contracts

1. Swap ETH for Weth via the weth contract, approve it for sending
1. Deposit into Aave
2. Borrow some asset with the ETH collateral
    1. Sell that borrowed asset. (Short selling)
3. Repay everything


Work with dexes too.

For testing:
    integration test: Kovan
    unit tests: Mainnet-fork

If we are not using oracles (pricefeed, vrf/randomness) and don't need to mock responses, we can go ahead and use a mainnet-fork to do our test

If we are using a oracle, it makes more sense to do the development network we mock the oracles and oracle responses.
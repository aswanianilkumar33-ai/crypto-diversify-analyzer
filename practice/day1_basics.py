def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        daily_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(daily_return)
    return returns


btc_prices = [45000, 46500, 44000, 47200, 48100]
eth_prices = [3000, 3100, 2950, 3200, 3050]

btc_returns = calculate_returns(btc_prices)
eth_returns = calculate_returns(eth_prices)

print("BTC returns:", btc_returns)
print("ETH returns:", eth_returns)

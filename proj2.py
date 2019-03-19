import numpy
import statistics


def get_price(phi, m, sigma, last_price):
    epsilon = numpy.random.normal(0, 1)
    return (1-phi) * m + phi * last_price + sigma * epsilon


def eval_policy(policy, N, initial_price, M, price_params):
    final_pis = []
    for path in range(M):
        n = 0
        last_price = initial_price
        while True:
            price = get_price(**price_params, last_price=last_price)
            if price >= policy['high'] or price <= policy['low'] or n >= N:
                final_pis.append(price-initial_price)
                break
            else:
                last_price = price
                n += 1
    assert len(final_pis) == M
    return final_pis


def sharpe(array):
    mu = statistics.mean(array)
    sigma = statistics.stdev(array)
    if sigma <= 0:
        print("ERROR SHARPE CALL")
        return 0
    return mu/sigma


if __name__ == '__main__':
    params = [
        {'phi': 2**(-0.2), 'm': 0, 'sigma': 1},
        {'phi': 2**(-0.2), 'm': 5, 'sigma': 1},
        {'phi': 2**(-0.2), 'm': -5, 'sigma': 1},
        {'phi': 2**(-0.2), 'm': 0, 'sigma': 2},
        {'phi': 2**(-0.1), 'm': 0, 'sigma': 1},
    ]

    results = {}

    for param in params:
        print(param)
        ratios = {}
        for i in range(0, 6, 2):
            for j in range(-10, 5, 5):
                policy = {'high': i, 'low': j}
                ratios[(i, j)] = sharpe(eval_policy(policy, N=100, initial_price=0, M=10**6, price_params=param))
        max_key = max(ratios, key=ratios.get)
        print(f'{max_key}: {ratios[max_key]}', end='\n\n')


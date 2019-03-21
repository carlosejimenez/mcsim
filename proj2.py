import numpy
import statistics


def eval_policy(policy, N, initial_price, M, price_params):
    """
    :param policy: Policy is a dictionary type like {'high': 2, 'low: -2}
    :param N: Integer for maximum iterations for each path
    :param initial_price: float
    :param M: number of paths to run
    :param price_params: keyword dictionary like {'phi': 0.8, 'm'= 0, 'sigma'= 1}
    :return: List of final returns. Of length M.
    """
    final_pis = []
    for path in range(M):
        print(f'\rpolicy {policy["high"], policy["low"]} - path {path+1}', end='')
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


def get_price(phi, m, sigma, last_price):
    """
    Mean reversion model with all the parameters
    :param phi: float
    :param m: integer
    :param sigma: float
    :param last_price: float
    :return: float
    """
    epsilon = numpy.random.normal(0, 1)
    return (1-phi) * m + phi * last_price + sigma * epsilon


def sharpe(array):
    mu = statistics.mean(array)
    sigma = statistics.stdev(array)
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
        for i in range(0, 4 + 1, 2):
            for j in range(-10, 0 + 1, 5):
                policy = {'high': i, 'low': j}
                ratios[(i, j)] = sharpe(eval_policy(policy, N=100, initial_price=0, M=10**6, price_params=param))
        max_key = max(ratios, key=ratios.get)
        print(f'\rpolicy{max_key}: {ratios[max_key]}', end='\n\n')


import numpy as np

def calc_score(player, strategy):
    m = np.array(strategy, dtype='float64')
    try:
        p = np.array(player, dtype='float64')
        sum = 0
        res = np.multiply(p,m)
        for i in res:
            sum+=i
        return sum/(11)
    except ValueError:
        return 0
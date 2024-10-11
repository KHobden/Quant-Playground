class StrategyBackTester:
    def __init__(self, pnl_vec:list[float]):
        self.pnl_vec = pnl_vec

    def maxRunUp(self):
        '''
        Obtains the maximum contiguous sub-array, V(i,j), in O(n)
        where V(i, j) is the sum of the PnL vector from element i up to j (i<=j)
        Efficiency is obtained by decomposing V(i,j) into V(j,0) - V(i,0)
        '''

        total_pnl = 0 # Equivalent to V(0,0)
        min_total_pnl = 0
        max_subarray = 0
        for pnl in self.pnl_vec:
            total_pnl += pnl
            min_total_pnl = total_pnl if total_pnl < min_total_pnl else min_total_pnl
            subarray_pnl = total_pnl - min_total_pnl
            max_subarray = subarray_pnl if subarray_pnl > max_subarray else max_subarray
            print(pnl, min_total_pnl, total_pnl)
        return max_subarray

if __name__ == '__main__':
    pnl_vec = [1, 2, -5, 4, -3, 2, 6, -5, -1]
    sbt = StrategyBackTester(pnl_vec)
    act_maxrunup = sbt.maxRunUp()

    exp_maxrunup = 9
    print(act_maxrunup)
    assert act_maxrunup == exp_maxrunup

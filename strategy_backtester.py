import math

class StrategyBackTester:
    def __init__(self, pnl_vec:list[float]):
        '''
        pnl_vector contains the levels not daily changes
        '''
        self.pnl_vec = pnl_vec

    def maxRunUp(self):
        '''
        Obtains the maximum contiguous sub-array, V(i,j), in O(n)
        where V(i, j) is the sum of the PnL vector from element i up to j (i<=j)
        Efficiency is obtained by decomposing V(i,j) into V(j,0)-V(i,0) or V(j,0)-V_min
        '''

        min_pnl = 0 # V_min
        max_runup = 0 # V(i,j)

        for pnl in self.pnl_vec:
            min_pnl = pnl if pnl<min_pnl else min_pnl
            max_runup = runup if (runup:=pnl-min_pnl)>max_runup else max_runup

        return max_runup
    
    def maxDrawDown(self):
        '''
        Similar to maxRunUp but the minimum contiguous sub-array, V(i,j), divided by the peak value
        Again O(n) is obtained by decomposing V(i,j) into V(j,0)-V_max
        '''

        max_pnl = 0 # V_max
        max_drawdown = 0 # V(i,j)

        for pnl in self.pnl_vec:
            max_pnl = pnl if pnl>max_pnl else max_pnl
            if max_pnl != 0: # Metric meaningless if total PnL is zero
                drawdown = (pnl-max_pnl)/max_pnl
                max_drawdown = drawdown if drawdown<max_drawdown else max_drawdown

        return max_drawdown


if __name__ == '__main__':
    pnl_vec = [0, 1, 3, -2, 2, -1, 1, 7, 2, 1]
    sbt = StrategyBackTester(pnl_vec)

    act_maxrunup = sbt.maxRunUp()
    exp_maxrunup = 9
    assert act_maxrunup == exp_maxrunup

    act_maxdrawdown = sbt.maxDrawDown()
    exp_maxdrawdown = -5/3
    assert math.isclose(act_maxdrawdown, exp_maxdrawdown)

from scipy.stats import bernoulli
from itertools import pairwise
import numpy as np
import math

class FairCoinAlgos:

    def __init__(self, p: float) -> None:
        # Generate a sequence of 1000 {H, T}
        # For comparison, these are re-used for each algorithm
        self.rvs = map(lambda e: 'H' if e else 'T', bernoulli.rvs(p, size=1000, random_state=0))

    def run_algos(self) -> None:
        for method in ('von_neumann', 'hoeffding_simons'):
            self.print_res(*getattr(self, method)())
    
    def print_res(self, outcome: int, num_flips: int) -> None:
        print(f'Outcome {outcome} was achieved in {num_flips} flips')

    def von_neumann(self) -> tuple[int, int]:
        '''
        Under the Von Neumann approach, consider pairs of events
        {H, T} and {T, H} each have probability pq so can be mapped to outcomes 1 and 0
        '''
        outcome = None
        for idx, (event1, event2) in enumerate(pairwise(self.rvs)):
            stopping_point = event1 != event2
            if stopping_point:
                if event1 == 'H': outcome = 1
                else: outcome = 0
                num_flips = (idx+1)*2
                return outcome, num_flips
        raise ValueError('Unbiased output could not be generated')
        
    
    def hoeffding_simons(self) -> tuple[int, int]:
        '''
        Hoeffding and Simons considered greater symmetries and ordering
        Using a tree, they observed sequences SH(k)T(k) and SH(k)T(k) were equiprobable
        where H(k) denotes a sequence of k Hs and S denotes a shared segment
        Outcomes can be assigned by considering the number of Hs in prior events to the stopping point
        '''
        prev_num_h = 0
        for idx, e in enumerate(self.rvs):
            num_flips = idx+1
            num_h = prev_num_h + (e=='H')
            stopping_point = not math.comb(num_flips, num_h) % 2
            if stopping_point:
                outcome = prev_num_h%2
                return outcome, num_flips
            prev_num_h = num_h
        raise ValueError('Unbiased output could not be generated')
    

if __name__ == '__main__':

    # Define the Bernoulli probability of our biased coin
    p = 0.23
    FairCoinAlgos(p).run_algos()
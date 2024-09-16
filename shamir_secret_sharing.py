import numpy as np
import operator
from abc import ABC, abstractmethod


class ShamirSecretSharing(ABC):
    MAX_SECRET_COEFF = 100

    def __init__(self, secret_val: int, num_keyholders: int, min_group: int) -> None:
        '''
        Shamir's Secret Sharing algorithm requires:
            1) A secret to be hidden
            2) The number of keys required
            3) The minimum number of keys needed to unlock the secret
        Note, an individual can have more than one key. For example, a CEO may want several keys to access data individually
        whilst giving a single key to each secretary for emergency access
        '''
        self.secret = secret_val
        self.num_keyholders = num_keyholders
        self.min_group = min_group

    @abstractmethod
    def generate_keys(self) -> list[tuple[int, int]]:
        ...
    
    @abstractmethod
    def unlock(self, keys: list[tuple[int, int]]) -> int:
        ...


class IntegerArithmeticSSS(ShamirSecretSharing):
    def __init__(self, secret_val: int, num_keyholders: int, min_group: int) -> None:
        '''
        Instantiates the ShamirSecretSharing base class
        '''
        super().__init__(secret_val, num_keyholders, min_group)

    def generate_keys(self) -> list[tuple[int, int]]:
        '''
        Generate each key using a polynomial with random coefficients
        '''

        # Define our polynomial of degree min_group using random coefficients
        rand_poly_coeffs = np.random.randint(self.MAX_SECRET_COEFF, size=self.min_group-1)
        f = lambda x: self.secret + sum(rand_poly_coeffs[idx]*x**(idx+1) for idx in range(self.min_group-1))

        # Create a key for each of the keyholders
        keys = [(x, f(x)) for x in range(1, self.num_keyholders+1)]
        return keys

    def unlock(self, keys: list[tuple[int, int]]) -> int:
        '''
        Unlock the secret with a set of keys by deciphering the random coefficients in our polynomial
        '''

        # Check enough keys were provided and consider the fewest keys required to unlock
        assert len(keys) >= self.min_group
        req_keys = keys[:self.min_group]

        # Using the keys, create and scale the first coefficient of each Lagrange polynomial
        deciphered_val = 0
        for x0, y0 in req_keys:
            lagrange_poly_coeff = y0
            for x1, y1 in req_keys:
                if x0 == x1:
                    continue
                lagrange_poly_coeff *= x1 / (x1-x0)
            deciphered_val += lagrange_poly_coeff
        return deciphered_val


if __name__ == '__main__':
    sss_method = IntegerArithmeticSSS(secret_val=12, num_keyholders=6, min_group=3)
    keys = sss_method.generate_keys()
    selected_keys = operator.itemgetter(0,1,2)(keys) # Select keys to unlock
    secret = sss_method.unlock(selected_keys)
    print(secret)
import numpy as np

class Policy:
    def __init__(self, proj_len: int):
        self.proj_len = proj_len
        self._v1 = np.full(shape=proj_len, fill_value=0, dtype=np.float64)
        self._b1 = np.full(shape=proj_len, fill_value=False, dtype=np.bool8)

        self._v2 = np.full(shape=proj_len, fill_value=0, dtype=np.float64)
        self._b2 = np.full(shape=proj_len, fill_value=False, dtype=np.bool8)

    def num_pols(self, t):
        #_v1
        if self._b1[t]:
            return self._v1[t]
        else:
            if t == 0:
                value = 1
            else:
                value = self.num_pols(t - 1) - self.num_deaths(t - 1)
            self._v1[t] = value
            self._b1[t] = True
            return value
        
    def num_deaths(self, t):
        #_v2
        if self._b2[t]:
            return self._v2[t]
        else:
            value = self.num_pols(t) * 0.01
            self._v2[t] = value
            self._b2[t] = True
            return value

def run_pol():
    p = Policy(400)
    return p.num_pols(399)


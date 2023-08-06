class Policy:
    def __init__(self, proj_len: int):
        self.proj_len = proj_len
        self._v1 = {}
        self._v2 = {}

    def num_pols(self, t):
        #_v1
        try:
            return self._v1[t]
        except KeyError:
            if t == 0:
                value = 1
            else:
                value = self.num_pols(t - 1) - self.num_deaths(t - 1)
            self._v1[t] = value
            return value
        
    def num_deaths(self, t):
        #_v2
        try:
            return self._v2[t]
        except KeyError:
            value = self.num_pols(t) * 0.01
            self._v2[t] = value
            return value

def run_pol():
    p = Policy(400)
    return p.num_pols(399)


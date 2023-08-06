from heavylight import Model

class Policy(Model):
    def num_pols(self, t):
            if t == 0:
                return 1
            else:
                return self.num_pols(t - 1) - self.num_deaths(t - 1)

    def num_deaths(self, t):
            return self.num_pols(t) * 0.01

def run_pol():
    p = Policy(do_run=True, proj_len=400)
    return p.num_pols(399)

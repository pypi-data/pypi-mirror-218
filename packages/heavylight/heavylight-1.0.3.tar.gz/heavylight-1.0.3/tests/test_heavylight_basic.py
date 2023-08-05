# run using pytest at command line
# %%
from heavylight import Model

class Ones(Model):
    def val_a(self, t):
        return 1
    
    def val_b(self, t):
        return self.val_a(t)
    
def test_ones():
    ones = Ones()
    ones.RunModel(proj_len = 12)
    assert ones.val_a(11) == 1
    assert ones.val_b(11) == 1
    assert sum(ones.val_a.values.values()) == 12
# %%

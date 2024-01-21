import random

"""
  val_max: max value of the cell inclusive
  regen_wait: how many turns until empty cell regenerates
  fav_max: maximum amount a val can be favored when regenerated
"""
class Cell:
    def __init__(self, val_max, regen_wait, fav_max):
        self.val = random.randint(0, val_max)
        self.val_max = val_max
        self.regen_wait = regen_wait
        self.regen_count = 0 # counter for determining when to regen
        self.fav_max = fav_max
        self.fav_lvl = 0 # level of favoritism
        self.fav = None

    def consume(self, fav):
        # val is replaced with -1 (empty), and chance of fav being regenerated increased
        if self.val != -1:
            if self.fav == fav:
                if self.fav_lvl < self.fav_max:
                    self.fav_lvl += 1
            else:
                self.fav = fav
                self.fav_lvl = 1
        self.val = -1

    def update(self):
        self.regen_count += 1
        if self.regen_count > self.regen_wait:
            self.regen_count = 0
            self.regen()
            return False
        return True

    def regen(self):
        # replace -1 with a new val
        ri = random.randint(0, self.val_max)
        if ri <= self.fav_lvl:
            self.val = self.fav
        else:
            remaining_vals = list(range(self.val_max + 1))
            remaining_vals.remove(self.fav)
            self.val = random.choice(remaining_vals)
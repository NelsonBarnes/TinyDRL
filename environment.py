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

    # val is replaced with -1 (empty), and chance of fav being regenerated increased
    def consume(self, fav):
        if self.val != -1:
            if self.fav == fav:
                if self.fav_lvl < self.fav_max:
                    self.fav_lvl += 1
            else:
                self.fav = fav
                self.fav_lvl = 1
        ret = self.val
        self.val = -1
        return ret

    def update(self):
        self.regen_count += 1
        if self.regen_count > self.regen_wait:
            self.regen_count = 0
            self.regen()
            return False
        return True

    # replace -1 with a new val
    def regen(self):
        ri = random.randint(0, self.val_max)
        if ri <= self.fav_lvl:
            self.val = self.fav
        else:
            remaining_vals = list(range(self.val_max + 1))
            remaining_vals.remove(self.fav)
            self.val = random.choice(remaining_vals)

class GridEnv:
    def __init__(self, width=10, height=10, cell_max=9, regen_wait=3, fav_max=4):
        if fav_max > cell_max:
            raise ValueError("fav_max must be leq to cell_max")
        self.width = width
        self.height = height
        self.state = [[Cell(cell_max, regen_wait, fav_max) for _ in range(height)] for _ in range(width)]
        self.tracked_cells = [] # only need to update empty cells, track these cells
        self.agents = {} # keep track of multiple agents

    def __str__(self):
        row_strings = []
        for y in range(self.height):
            row_string = ''
            for x in range(self.width - 1):
                if self.state[x+1][y].val < 0:
                    row_string += str(self.state[x][y].val) + ','
                else:
                    row_string += str(self.state[x][y].val) + ', '
            row_string += str(self.state[self.width - 1][y].val) + '\n'
            row_strings.append(row_string)
        return ''.join(row_strings)
    
    # initialize a new agent
    def add_agent(self, id, vis):
        while True:
            x_pos = random.randint(0, self.width - 1)
            y_pos = random.randint(0, self.height - 1)
            b = True
            for pos in self.agents.values():
                if pos[0] == x_pos and pos[1] == y_pos:
                    b = False
            if b:
                self.agents[id] = (x_pos, y_pos, vis)
                break
        return self.get_obs(x_pos, y_pos, vis)

    # TODO: add function to move multiple agents
    def move_agent(self, id, move, fav):
        try:
            x_pos = (self.agents[id][0] + move[0]) % self.width
            y_pos = (self.agents[id][1] + move[1]) % self.height
        except KeyError:
            print("agent id not found")

        new_agent_tup = (x_pos, y_pos, self.agents[id][2]) 
        self.agents[id] = new_agent_tup

        self.update_tracked_cells(self.state[x_pos][y_pos])
        self.state[x_pos][y_pos].consume(fav)

        return self.get_obs(x_pos, y_pos, self.agents[id][2])
    
    # get an observation of a grid area
    def get_obs(self, x_pos, y_pos, vis):
        x_start = (x_pos - vis) % self.width
        y_start = (y_pos - vis) % self.height
        vis_dim = vis * 2 + 1
        obs = [[None for _ in range(vis_dim)] for _ in range(vis_dim)]
        for j, y in enumerate(range(y_start, y_start + vis_dim)):
            for k, x in enumerate(range(x_start, x_start + vis_dim)):
                obs[j][k] = self.state[x % self.width][y % self.height].val
        return obs
    
    def update_tracked_cells(self, cell):
        tracked_cells_new = []
        for tc in self.tracked_cells:
            if tc.update():
                tracked_cells_new.append(tc)
        if cell not in tracked_cells_new:
            tracked_cells_new.append(cell)
        self.tracked_cells = tracked_cells_new
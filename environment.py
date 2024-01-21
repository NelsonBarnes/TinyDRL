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

class GridEnv:
    def __init__(self, width=10, height=10, cell_max=9, regen_wait=3, fav_max=4):
        if fav_max > cell_max:
            raise ValueError("fav_max must be leq to cell_max")
        self.width = width
        self.height = height
        self.state = [[Cell(cell_max, regen_wait, fav_max) for _ in range(height)] for _ in range(width)]
        self.tracked_cells = [] # only need to update empty cells, track these cells
        self.agents = {} # keep track of multiple agents
        self.moveLib = {0:(0,0),1:(1,0),2:(1,-1),3:(0,-1),4:(-1,-1),5:(-1,0),6:(-1,1),7:(0,1),8:(1,1)}

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
    
    def add_agent(self, agent):
        if agent.id in self.agents.keys():
            raise ValueError("agent needs a unique id")

        x_pos = random.randint(0, self.width - 1)
        y_pos = random.randint(0, self.height - 1)
        agent.update_pos(x_pos, y_pos)
        self.agents[agent.id] = agent

    # TODO: add function to move multiple agents
    def step(self, id, action): # action: (move_id, fav)
        try:
            x_pos, y_pos = self.agents[id].get_pos()
        except KeyError:
            print("agent id not found")

        move = self.moveLib[action[0]]
        fav = action[1]

        x_pos = (x_pos + move[0]) % self.width
        y_pos = (y_pos + move[1]) % self.height

        self.agents[id].update_pos(x_pos, y_pos)
        self.update_tracked_cells(self.state[x_pos][y_pos], fav)
        return self.get_agent_state(id)
     
    def get_agent_state(self, id):
        # get an agent's current state
        try:
            x_pos, y_pos = self.agents[id].get_pos()
        except KeyError:
            print("agent id not found")

        x_start = (x_pos - self.agents[id].vis) % self.width
        y_start = (y_pos - self.agents[id].vis) % self.height
        vis_dim = self.agents[id].vis * 2 + 1
        s = [[None for _ in range(vis_dim)] for _ in range(vis_dim)]
        for j, y in enumerate(range(y_start, y_start + vis_dim)):
            for k, x in enumerate(range(x_start, x_start + vis_dim)):
                s[j][k] = self.state[x % self.width][y % self.height].val
        return s
    
    def update_tracked_cells(self, cell, fav):
        tracked_cells_new = []
        for tc in self.tracked_cells:
            if tc != cell:
                if tc.update():
                    tracked_cells_new.append(tc)
        cell.regen_count = 0
        cell.consume(fav)
        tracked_cells_new.append(cell)
        self.tracked_cells = tracked_cells_new
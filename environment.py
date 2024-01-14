import random

class Cell:
    def __init__(self, val_max, regen_wait, fav_max):
        self.val = random.randint(0, val_max)
        self.val_max = val_max
        self.regen_wait = regen_wait
        self.regen_count = 0
        self.fav_max = fav_max
        self.fav_lvl = 0
        self.fav = None

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
        self.tracked_cells = []
        self.agents = {}

    def __str__(self):
        row_strings = []
        for y in range(self.height):
            row_string = ''
            for x in range(self.width - 1):
                row_string += str(self.state[x][y].val) + ','
            row_string += str(self.state[self.width - 1][y].val) + '\n'
            row_strings.append(row_string)
        return ''.join(row_strings)
    
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
        return self.get_view(x_pos, y_pos, vis)

    # TODO: add move_agents function
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

        return self.get_view(x_pos, y_pos, self.agents[id][2])
    
    def get_view(self, x_pos, y_pos, vis):
        x_start = (x_pos - vis) % self.width
        y_start = (y_pos - vis) % self.height
        vis_dim = vis * 2 + 1
        view = [[None for _ in range(vis_dim)] for _ in range(vis_dim)]
        for j, y in enumerate(range(y_start, y_start + vis_dim)):
            for k, x in enumerate(range(x_start, x_start + vis_dim)):
                view[j][k] = self.state[x % self.width][y % self.height].val
        return view
    
    def update_tracked_cells(self, cell):
        tracked_cells_new = []
        for tc in self.tracked_cells:
            if tc.update():
                tracked_cells_new.append(tc)
        if cell not in tracked_cells_new:
            tracked_cells_new.append(cell)
        self.tracked_cells = tracked_cells_new
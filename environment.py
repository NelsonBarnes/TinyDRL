import random


class Node:
    def __init__(self, max_val, regen_wait, favor_levels):
        self.val = random.randint(0, max_val)
        self.max_val = max_val
        self.regen_wait = regen_wait
        self.regen_step = 0
        self.favor_levels = favor_levels
        self.favor_lvl = 0
        self.favor = None

    def consume(self, fav):
        self.val = -1
        if self.favor == fav:
            if self.favor_lvl < self.favor_levels:
                self.favor_lvl += 1
        else:
            self.favor = fav
            self.favor_lvl = 1

    def update(self):
        self.regen_step += 1
        if self.regen_step > self.regen_wait:
            self.regen_step = 0
            self.regen()
            return False
        return True

    def regen(self):
        ri = random.randint(0, self.max_val)
        if ri <= self.favor_lvl:
            self.val = self.favor
        else:
            remaining_vals = list(range(self.max_val + 1))
            remaining_vals.remove(self.favor)
            self.val = random.choice(remaining_vals)


class Env:
    def __init__(self, width=10, height=10, node_max=9, regen_wait=3, favor_levels=4, visibility=2):
        if favor_levels > node_max:
            print('error: favor_levels must be <= unit_max')
        self.width = width - 1
        self.height = height - 1
        self.visibility = visibility
        self.vis_dim = (visibility * 2) + 1
        self.state = [[Node(node_max, regen_wait, favor_levels) for _ in range(height)] for _ in range(width)]
        self.tracked_nodes = []
        self.prev_view = None

    def __str__(self):
        row_strings = []
        for y in range(self.height + 1):
            row_string = ''
            for x in range(self.width):
                row_string += str(self.state[x][y].val) + ', '
            row_string += str(self.state[self.width][y].val) + '\n'
            row_strings.append(row_string)
        return ''.join(row_strings)

    def update(self, x_in, y_in, fav):
        self.update_nodes()

        if self.state[x_in][y_in] in self.tracked_nodes:
            return self.prev_view
        
        self.state[x_in][y_in].consume(fav)

        x_pad1, y_pad1 = -(x_in - self.visibility), -(y_in - self.visibility)
        x_pad2, y_pad2 = x_in + self.visibility - self.width, y_in + self.visibility - self.height

        if y_pad1 > 0:
            view = [[-1 for _ in range(self.vis_dim)] for _ in range(y_pad1)]
            if x_pad1 > 0:
                for y in range(self.vis_dim - y_pad1):
                    view.append([-1 for _ in range(x_pad1)])
                    for x in range(self.vis_dim - x_pad1):
                        view[-1].append(self.state[x][y].val)
            elif x_pad2 > 0:
                for y in range(self.vis_dim - y_pad1):
                    view.append([-1 for _ in range(x_pad2)])
                    for x in range(self.width, x_in - self.visibility - 1, -1):
                        view[-1].insert(0, self.state[x][y].val)
            else:
                for y in range(self.vis_dim - y_pad1):
                    view.append([])
                    for x in range(x_in - self.visibility, x_in + self.visibility + 1):
                        view[-1].append(self.state[x][y].val)     
        elif y_pad2 > 0:
            view = [[-1 for _ in range(self.vis_dim)] for _ in range(y_pad2)]
            if x_pad1 > 0:
                for y in range(self.height, y_in - self.visibility - 1, -1):
                    view.insert(0, [-1 for _ in range(x_pad1)])
                    for x in range(self.vis_dim - x_pad1):
                        view[0].append(self.state[x][y].val)
            elif x_pad2 > 0:
                for y in range(self.height, y_in - self.visibility - 1, -1):
                    view.insert(0, [-1 for _ in range(x_pad2)])
                    for x in range(self.width, x_in - self.visibility - 1, -1):
                        view[0].insert(0, self.state[x][y].val)
            else:
                for y in range(self.height, y_in - self.visibility - 1, -1):
                    view.insert(0, [])
                    for x in range(x_in - self.visibility, x_in + self.visibility + 1):
                        view[0].append(self.state[x][y].val)  
        else:
            view = []
            for y in range(y_in - self.visibility, y_in + self.visibility + 1):
                view.append([])
                for x in range(x_in - self.visibility, x_in + self.visibility + 1):
                    view[-1].append(self.state[x][y].val)

        self.tracked_nodes.append(self.state[x_in][y_in])
        self.prev_view = view
        return view
    
    def update_nodes(self):
        tracked_nodes_new = []
        for node in self.tracked_nodes:
            if node.update():
                tracked_nodes_new.append(node)
        self.tracked_nodes = tracked_nodes_new
        

ENV_W = 10
ENV_H = 10
NODE_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAVOR_LEVELS = 4
VISIBILITY = 2

testEnv = Env(ENV_W, ENV_H, NODE_MAX, REGEN_WAIT, FAVOR_LEVELS, VISIBILITY)
print(testEnv)
testEnv.update(4,4,4)
print(testEnv)

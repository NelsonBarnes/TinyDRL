import random

class Agent:
    def __init__(self, id, vis, reach, fav_max):
        if not isinstance(id, str):
            raise TypeError("id should be a string")
        if reach > vis:
            raise ValueError("vis should be geq to reach")
        self.id = id
        self.vis = vis
        self.reach = reach
        self.fav_max = fav_max
        self.resources = []

    def act(self, view):
        # choose where to move based off agent's view
        x_move = random.randint(-self.reach, self.reach)
        y_move = random.randint(-self.reach, self.reach)
        fav = random.randint(0, self.fav_max)
        self.resources.append(view[self.vis + x_move][self.vis + y_move])
        return (x_move, y_move), fav

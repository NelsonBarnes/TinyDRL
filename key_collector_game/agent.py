import random

"""
  id: agent's ID
  vis: how far the agent can see in each direction
  reach: how far the agent can move in each direction
"""
class Agent:
    def __init__(self, id, vis, reach, key): # TODO: remove fav_max
        if not isinstance(id, str):
            raise TypeError("id should be a string")
        if reach > vis:
            raise ValueError("vis should be geq to reach")
        self.id = id
        self.vis = vis
        self.reach = reach
        self.key = key
        self.x_pos = None
        self.y_pos = None
        self.resources = []

    def get_pos(self):
        return self.x_pos, self.y_pos

    def update_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def get_reward(self):
        kl = len(self.key)
        if len(self.resources) > kl:
            if (self.resources[-kl:] == self.key):
                return 1 # max reward

        return -.1 # small negative reward
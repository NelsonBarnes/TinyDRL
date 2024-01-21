from tinygrad import Tensor, nn
from environment import MultiEnv
from agent import Agent
from policyNet import policyNet
from valueNet import valueNet
#import math


ENV_W = 10
ENV_H = 10
CELL_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAV_MAX = 4
AGENT_VIS = 2
AGENT_REACH = 1
REWARD_KEY = 1234


N = 1 # number of parallel agents collecting training data
T = 20 # max steps each agent takes
K = 2 # number of epochs
V = .2 # value weighting factor
H = .2 # entropy weighting factor
MBATCH_SIZE = 5 # mini-batch size
NUM_MBATCH = (N*T)/MBATCH_SIZE # number of mini-batches per epoch
LR = .001 # learning rate


env = MultiEnv(ENV_W, ENV_H, CELL_MAX, REGEN_WAIT, FAV_MAX)
agent = Agent('a', AGENT_VIS, AGENT_REACH, REWARD_KEY)
env.add_agent(agent)

state_space = (AGENT_VIS * 2 + 1)**2
pnet = policyNet(state_space, 9*(CELL_MAX+1)) # movement * which fav value
vnet = valueNet(state_space)

poptim = nn.optim.Adam([pnet.l1, pnet.l2, pnet.l3], lr=LR)
voptim = nn.optim.Adam([vnet.l1, vnet.l2, vnet.l3], lr=LR)

train_data = []

def get_train_data():
    print('State 0')
    env.print_env()
    # TODO: multiple agents in env, env randomly initialized for each agent
    for t in range(1,T+1):
        state = Tensor(env.get_agent_state(agent.id)).flatten().reshape(1, state_space)
        action_probabilities = pnet(state)
        action_net = action_probabilities.multinomial().numpy()[0]
        move = int(action_net / (CELL_MAX + 1))
        fav = action_net % (CELL_MAX + 1)
        action = (move, fav)
        env.step(action, agent.id)
        print(f'State {t}, Agent Position: {agent.x_pos}, {agent.y_pos}')
        env.print_env()

get_train_data()

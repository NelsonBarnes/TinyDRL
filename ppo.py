from tinygrad import Tensor, nn
from key_collector_game.env import MultiEnv
from key_collector_game.agent import Agent
from policyNet import policyNet
from valueNet import valueNet
import random
import math


ENV_W = 10
ENV_H = 10
CELL_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAV_MAX = 4
AGENT_VIS = 2
AGENT_REACH = 1
REWARD_KEY = [1,2,3,4]


N = 1 # number of parallel agents collecting training data
T = 20 # max steps each agent takes
K = 2 # number of epochs
V = .2 # value weighting factor
H = .2 # entropy weighting factor
DF = .2 # cummulative reward discount factor
MBATCH_SIZE = 5 # mini-batch size
NUM_MBATCH = (N*T)/MBATCH_SIZE # number of mini-batches per epoch
LR = .001 # learning rate
EPS = .2 # clipping factor


env = MultiEnv(ENV_W, ENV_H, CELL_MAX, REGEN_WAIT, FAV_MAX)
agent = Agent('a', AGENT_VIS, AGENT_REACH, REWARD_KEY)
env.add_agent(agent)

state_space = (AGENT_VIS * 2 + 1)**2
pnet = policyNet(state_space, 9*(CELL_MAX+1)) # movement * which fav value
vnet = valueNet(state_space)

poptim = nn.optim.Adam([pnet.l1, pnet.l2, pnet.l3], lr=LR)
voptim = nn.optim.Adam([vnet.l1, vnet.l2, vnet.l3], lr=LR)

train_data = []
# train data element = (state, action, reward, probabily of action given state)

def generate_action(net:policyNet, state):
    action_dist = net(state)
    net_action = action_dist.multinomial().numpy()[0]
    action_prob = action_dist.numpy()[net_action]
    move = int(net_action / (CELL_MAX + 1))
    fav = net_action % (CELL_MAX + 1)
    action = (move, fav)
    return action, action_prob, action_dist

def get_train_data():
    # print('State 0')
    # env.print_env()
    # TODO: multiple agents in env, env randomly initialized for each agent
    agent_data = []
    for t in range(1,T+1):
        state = Tensor(env.get_agent_state(agent.id)).flatten().reshape(1, state_space)
        action, action_prob, _ = generate_action(pnet, state)
        state_value = vnet(state).numpy()

        env.step(action, agent.id)
        reward = agent.get_reward()

        agent_data.append((state, action, reward, action_prob, state_value))

        # print(f'State {t}, Agent Position: {agent.x_pos}, {agent.y_pos}')
        #env.print_env()

    for t in range(0,T):
        cum_reward = agent_data[t][2]
        for i, n in enumerate(range(t+1, T)):
            cum_reward += DF**(i+1) * agent_data[n][2]

        advantage = cum_reward - agent_data[t][3]
        new_tup = (agent_data[t][0], agent_data[t][1], agent_data[t][2], agent_data[t][3], cum_reward, advantage)
        agent_data[t] = new_tup

    train_data.append(agent_data)

def get_minibatches(train_data, batch_size, num_batches):
    minibatches = []
    data_flat = []
    for l in train_data:
        data_flat.extend(l)

    for _ in range(num_batches):
        batch = random.sample(data_flat, batch_size)
        minibatches.append(batch)
        data_flat = [e for e in data_flat if e not in batch]

    return minibatches

def train():
    minibatch_size = 4

    get_train_data()
    minibatches = get_minibatches(train_data, minibatch_size, 4)

    for mb in minibatches:
        l_clip_acc = 0
        l_v_acc = 0
        h_acc = Tensor(0)
        for e in mb:
            _, action_prob, cur_dist = generate_action(pnet, e[0])

            p = action_prob / e[3]
            p_clip = p
            if p < 1 - EPS:
                p_clip = 1 - EPS
            elif p > 1 + EPS:
                p_clip = 1 + EPS
            
            l_clip_acc += min(p * e[5], p_clip * e[5])

            state_value_cur = vnet(e[0]).numpy()
            l_v_acc += (state_value_cur - e[4]) ** 2

            output = (cur_dist * cur_dist.log()).sum()
            h_acc += output

        loss = Tensor(-(l_clip_acc / minibatch_size) + V * (l_v_acc / minibatch_size) - H * (h_acc / minibatch_size))

        poptim.zero_grad()
        voptim.zero_grad()

        loss.backward()

        poptim.step()
        voptim.step()

train()
        


        

            






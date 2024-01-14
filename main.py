from environment import GridEnv
from agent import Agent

ENV_W = 10
ENV_H = 10
CELL_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAV_MAX = 4
AGENT_VIS = 2
AGENT_REACH = 1

def main():
    gridEnv = GridEnv(ENV_W, ENV_H, CELL_MAX, REGEN_WAIT, FAV_MAX)
    agent = Agent('a', AGENT_VIS, AGENT_REACH, FAV_MAX)

    print('State 0')
    print(gridEnv)
    obs = gridEnv.add_agent(agent.id, agent.vis)
    for i in range(1, 11):
        move, fav = agent.act(obs)
        gridEnv.move_agent(agent.id,move, fav)
        print(f'State {i}, Agent Position: {gridEnv.agents[agent.id][0]}, {gridEnv.agents[agent.id][1]}')
        print(gridEnv)

    print('done')

if __name__ == "__main__":
    main()

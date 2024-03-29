from key_collector_game.env import MultiEnv
from key_collector_game.agent import Agent

ENV_W = 10
ENV_H = 10
CELL_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAV_MAX = 4
AGENT_VIS = 2
AGENT_REACH = 1
REWARD_KEY = [1,2,3,4]

def main():
    gridEnv = MultiEnv(ENV_W, ENV_H, CELL_MAX, REGEN_WAIT, FAV_MAX)
    agent = Agent('a', AGENT_VIS, AGENT_REACH, REWARD_KEY)
    gridEnv.add_agent(agent)

    action1 = (0, 2)
    action2 = (1, 2)
    action3 = (5, 2)

    print('State 0')
    gridEnv.print_env()

    gridEnv.step(action2, agent.id)
    print(f'State {1}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action3, agent.id)
    print(f'State {2}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action2, agent.id)
    print(f'State {3}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action3, agent.id)
    print(f'State {4}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action1, agent.id)
    print(f'State {5}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action1, agent.id)
    print(f'State {6}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action1, agent.id)
    print(f'State {7}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
    gridEnv.step(action1, agent.id)
    print(f'State {8}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    gridEnv.print_env()
        
    print('done')

if __name__ == "__main__":
    main()

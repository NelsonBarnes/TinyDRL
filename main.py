from environment import GridEnv
from agent import Agent

ENV_W = 10
ENV_H = 10
CELL_MAX = 9 # [0:UNIT_MAX]
REGEN_WAIT = 3
FAV_MAX = 4
AGENT_VIS = 2
AGENT_REACH = 1
REWARD_KEY = [1,2,3,4]

def main():
    gridEnv = GridEnv(ENV_W, ENV_H, CELL_MAX, REGEN_WAIT, FAV_MAX)
    agent = Agent('a', AGENT_VIS, AGENT_REACH, REWARD_KEY)
    gridEnv.add_agent(agent)

    action1 = (0, 2)
    action2 = (1, 2)
    action3 = (5, 2)

    print('State 0')
    print(gridEnv)

    gridEnv.step(agent.id, action2)
    print(f'State {1}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action3)
    print(f'State {2}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action2)
    print(f'State {3}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action3)
    print(f'State {4}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action1)
    print(f'State {5}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action1)
    print(f'State {6}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action1)
    print(f'State {7}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
    gridEnv.step(agent.id, action1)
    print(f'State {8}, Agent Position: {agent.x_pos}, {agent.y_pos}')
    for cell in gridEnv.tracked_cells:
        print(f'regen_count: {cell.regen_count}')
    print(gridEnv)
        

    print('done')

if __name__ == "__main__":
    main()

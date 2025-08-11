import random

# Constants
DEFAULT_GRID_SIZE = 5
DEFAULT_MAX_STEPS = 50
STEP_PENALTY = -0.01
GOAL_REWARD = 1.0


class GridWorldEnv:
    def __init__(self, grid_size=DEFAULT_GRID_SIZE, max_steps=DEFAULT_MAX_STEPS):
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.actions = ['up', 'down', 'left', 'right']
        self.reset()

    def reset(self):
        # Random positions for agent and goal (must not be at same location)
        self.agent_pos = [random.randint(0, self.grid_size - 1),
                          random.randint(0, self.grid_size - 1)]
        while True:
            self.goal_pos = [random.randint(0, self.grid_size - 1),
                             random.randint(0, self.grid_size - 1)]
            if self.goal_pos != self.agent_pos:
                break
        self.steps = 0
        return self._get_state()

    def _get_state(self):
        # Returns state as tuple: (agent_x, agent_y, goal_x, goal_y)
        return (self.agent_pos[0], self.agent_pos[1],
                self.goal_pos[0], self.goal_pos[1])

    def step(self, action):
        self.steps += 1

        if action == 0 and self.agent_pos[1] > 0:  # up
            self.agent_pos[1] -= 1
        elif action == 1 and self.agent_pos[1] < self.grid_size - 1:  # down
            self.agent_pos[1] += 1
        elif action == 2 and self.agent_pos[0] > 0:  # left
            self.agent_pos[0] -= 1
        elif action == 3 and self.agent_pos[0] < self.grid_size - 1:  # right
            self.agent_pos[0] += 1

        done = False
        reward = STEP_PENALTY

        if self.agent_pos == self.goal_pos:
            reward = GOAL_REWARD
            done = True
        elif self.steps >= self.max_steps:
            done = True

        return self._get_state(), reward, done

    def render(self):
        # Simple console visualization
        for y in range(self.grid_size):
            row = ''
            for x in range(self.grid_size):
                if [x, y] == self.agent_pos:
                    row += 'A '
                elif [x, y] == self.goal_pos:
                    row += 'G '
                else:
                    row += '. '
            print(row)
        print()

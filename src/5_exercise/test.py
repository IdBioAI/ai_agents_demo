import numpy as np
from env import GridWorldEnv
from agent import Agent

# Testing constants
DEFAULT_TEST_EPISODES = 1000
DEFAULT_MAX_STEPS = 50
Q_TABLE_FILENAME = "q_table.npy"


def test_agent(episodes=DEFAULT_TEST_EPISODES, max_steps=DEFAULT_MAX_STEPS):
    env = GridWorldEnv()
    agent = Agent(
        state_shape=(env.grid_size, env.grid_size, env.grid_size, env.grid_size),
        n_actions=4,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.0,  # No exploration, always exploit
        epsilon_decay=1.0,
        min_epsilon=0.0
    )

    agent.load_q_table(Q_TABLE_FILENAME)

    total_rewards = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        step = 0
        for step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)

            state = next_state
            total_reward += reward

            if done:
                break
        total_rewards.append(total_reward)
        print(f"Episode {episode + 1}: Total Reward = {total_reward}")

    avg_reward = sum(total_rewards) / episodes
    print(f"\nAverage Reward over {episodes} episodes: {avg_reward:.2f}")


if __name__ == "__main__":
    test_agent()

import numpy as np
from env import GridWorldEnv
from agent import Agent

# Training constants
DEFAULT_EPISODES = 5000
DEFAULT_MAX_STEPS = 50
Q_TABLE_FILENAME = "q_table.npy"


def train_agent(episodes=DEFAULT_EPISODES, max_steps=DEFAULT_MAX_STEPS):
    env = GridWorldEnv()
    agent = Agent(
        state_shape=(env.grid_size, env.grid_size, env.grid_size, env.grid_size),
        n_actions=4,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        epsilon_decay=0.995,
        min_epsilon=0.01
    )

    rewards_per_episode = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0

        for step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward

            if done:
                break

        agent.decay_epsilon()
        rewards_per_episode.append(total_reward)

        if (episode + 1) % 50 == 0:
            print(f"Episode {episode + 1}/{episodes} - Epsilon: {agent.epsilon:.3f} - Total reward: {total_reward}")

    agent.save_q_table(Q_TABLE_FILENAME)

    return rewards_per_episode


if __name__ == "__main__":
    train_agent()

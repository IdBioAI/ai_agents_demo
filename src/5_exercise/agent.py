import numpy as np
import random

# Default hyperparameters
DEFAULT_LEARNING_RATE = 0.1
DEFAULT_DISCOUNT_FACTOR = 0.9
DEFAULT_EPSILON = 1.0
DEFAULT_EPSILON_DECAY = 0.995
DEFAULT_MIN_EPSILON = 0.01


class Agent:
    def __init__(self, state_shape, n_actions, alpha=DEFAULT_LEARNING_RATE, gamma=DEFAULT_DISCOUNT_FACTOR, 
                 epsilon=DEFAULT_EPSILON, epsilon_decay=DEFAULT_EPSILON_DECAY, min_epsilon=DEFAULT_MIN_EPSILON):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.n_actions = n_actions
        self.Q = np.zeros(state_shape + (n_actions,))

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.Q[state])

    def learn(self, state, action, reward, next_state, done):
        q_predict = self.Q[state + (action,)]
        q_target = reward
        if not done:
            q_target += self.gamma * np.max(self.Q[next_state])
        self.Q[state + (action,)] += self.alpha * (q_target - q_predict)

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_q_table(self, path):
        np.save(path, self.Q)

    def load_q_table(self, path):
        self.Q = np.load(path)

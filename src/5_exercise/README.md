# GridWorld Q-Learning Agent

This project implements a **Q-learning agent** for navigation in a grid environment (*GridWorld*). The agent starts at a random position and must find a randomly placed goal. During training, the agent stores rewards for individual states and actions in a **Q-table** and gradually learns an optimal movement policy.

## Features

* **Custom environment** defined in `env.py`
* **Q-learning agent** (`agent.py`)
* Configurable learning parameters:
    * `alpha` – learning rate
    * `gamma` – discount factor
    * `epsilon` – probability of random exploration
    * `epsilon_decay` – gradual reduction of exploration
* Saving and loading Q-table (`q_table.npy`)
* Separate training (`train.py`) and testing (`test.py`)

## Files

* `env.py` – environment definition (grid, agent movement, goal generation, rewards)
* `agent.py` – Q-learning algorithm implementation
* `train.py` – agent training and Q-table saving
* `test.py` – testing of the trained agent
* `q_table.npy` – saved Q-table from training

## Usage

### Training the agent:

```bash
python train.py
```

### Testing the trained agent:

```bash
python test.py
```

## How it Works

The Q-learning agent explores the grid environment and learns optimal actions through trial and error. The Q-table stores the expected future rewards for each state-action pair, allowing the agent to make increasingly better decisions over time.

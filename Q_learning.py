import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt

def train_q_learning(env, episodes=300, alpha=0.12, gamma=0.99,
                     epsilon_start=0.7, epsilon_end=0.01, epsilon_decay=0.99):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    Q = np.zeros((n_states, n_actions))
    epsilon = epsilon_start
    q_rewards = []

    for ep in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            if np.random.rand() < epsilon:
                action = np.random.randint(n_actions)
            else:
                action = np.argmax(Q[state])

            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            best_next = np.max(Q[next_state])
            Q[state, action] += alpha * (reward + gamma * best_next - Q[state, action])

            state = next_state
            total_reward += reward

        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        q_rewards.append(total_reward)

    return q_rewards

def run_random_agent(env, episodes=300):
    rewards = []
    for _ in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False
        while not done:
            action = env.action_space.sample()
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward
        rewards.append(total_reward)
    return rewards

# Number of experiment repeats
num_runs = 10

# Lists for results from each repeat
all_q_means = []
all_random_means = []

for run in range(num_runs):
    env = gym.make("CliffWalking-v0")

    q_rewards = train_q_learning(env, episodes=300)
    random_rewards = run_random_agent(env, episodes=50)

    # Average total rewards from last 50 episodes
    q_mean_last50 = np.mean(q_rewards[-50:])
    random_mean_last50 = np.mean(random_rewards[-50:])

    all_q_means.append(q_mean_last50)
    all_random_means.append(random_mean_last50)

# Calculate and print statistics
def print_stats(name, data):
    print(f"{name}:")
    print(f"  Mean: {np.mean(data):.3f}")
    print(f"  Standard deviation: {np.std(data):.3f}")
    print(f"  Minimum: {np.min(data):.3f}")
    print(f"  Maximum: {np.max(data):.3f}")
    print()

print_stats("Q-Learning (mean from last 50 episodes)", all_q_means)
print_stats("Random agent (mean from last 50 episodes)", all_random_means)

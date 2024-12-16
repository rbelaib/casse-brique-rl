from rl_agent.environment import BrickBreakerEnv
from rl_agent.agent import DQNAgent

import time
from rl_agent.environment import BrickBreakerEnv
from rl_agent.agent import DQNAgent

def train_agent(episodes=500, batch_size=32, delay=0.001):
    env = BrickBreakerEnv()
    agent = DQNAgent(state_size=env.observation_space, action_size=len(env.action_space))
    initial_weights = agent.model.get_weights()
    print("Initial weights:", initial_weights)
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        while True:
            env.render()  # Permet de voir le jeu pendant l'entraînement
            
            # Ajoute une pause pour ralentir la vitesse d'exécution
            time.sleep(delay)
            
            action_index = agent.act(state)
            action = env.action_space[action_index]
            next_state, reward, done = env.step(action)
            agent.remember(state, action_index, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode {episode + 1}/{episodes}, Score: {total_reward}")
                break

        agent.replay(batch_size)
        agent.update_epsilon()
        if episode == episodes - 1:
            final_weights = agent.model.get_weights()
            print("Final weights:", final_weights)
            model_path="models/final_models.h5"
            agent.save(model_path)
            print(f"Model saved to {model_path}")

        
      # Ajoute une méthode pour évaluer les performances de l'agent
def evaluate(num_episodes=100):
     env = BrickBreakerEnv()
     agent = DQNAgent(state_size=env.observation_space, action_size=len(env.action_space))
     total_score = 0
     for _ in range(num_episodes):
        state = env.reset()
        done = False
        episode_score = 0
        while not done:
            action = agent.act(state)  # Ne pas explorer
            state, reward, done = env.step(action)
            episode_score += reward
        total_score += episode_score
     average_score = total_score / num_episodes
     print(f"Average Score after training: {average_score}")



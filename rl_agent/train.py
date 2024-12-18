from rl_agent.environment import BrickBreakerEnv
from rl_agent.agent import DQNAgent

import time
from rl_agent.environment import BrickBreakerEnv
from rl_agent.agent import DQNAgent

def play_agent(epochs=500, batch_size=32, delay=0.00001, train=True, model_path="models/final_models.h5"):
    """ Entraine l'agent pour jouer au jeu"""
    env = BrickBreakerEnv()
    agent = DQNAgent(state_size=env.observation_space, action_size=len(env.action_space))
    if train:
        initial_weights = agent.model.get_weights()
        print("Initial weights:", initial_weights)
    if not train:
        agent.load_model(model_path) # Charge le modèle sauvegardé
        agent.epsilon = 0.3 # Réduit l'exploration
    
    for epoch in range(epochs):
        state = env.reset()
        total_reward = 0
        previous_brick_count = len(env.game.bricks)
        while True:
            env.render()  # Permet de voir le jeu pendant l'entraînement
            time.sleep(delay)
            
            action_index = agent.act(state) # Choisit une action
            action = env.action_space[action_index] # Convertit l'index en action
            next_state, reward, done, current_brick_count = env.step(action, previous_brick_count) # Exécute l'action
            if train:
                agent.remember(state, action_index, reward, next_state, done) # Ajoute l'expérience à la mémoire
            state = next_state
            total_reward += reward
            previous_brick_count = current_brick_count

            if done:
                print(f"Epoch {epoch + 1}/{epochs}, Score: {total_reward}")
                break

        if train:
            agent.replay(batch_size) # Entraîne le modèle
            agent.update_epsilon(total_reward)
            # Model sauvegardé toutes les 50 épochs
            if (epoch % 50 == 0 and epoch != 0) or epoch == epochs - 1:
                final_weights = agent.model.get_weights()
                print("Weights:", final_weights)
                agent.save(model_path)
                print(f"Model saved to {model_path}")

        
      # Ajoute une méthode pour évaluer les performances de l'agent
def evaluate(num_epochs=100):
     env = BrickBreakerEnv()
     agent = DQNAgent(state_size=env.observation_space, action_size=len(env.action_space))
     total_score = 0
     for _ in range(num_epochs):
        state = env.reset()
        done = False
        epoch_score = 0
        while not done:
            action = agent.act(state)  # Ne pas explorer
            state, reward, done = env.step(action)
            epoch_score += reward
        total_score += epoch_score
     average_score = total_score / num_epochs
     print(f"Average score after training: {average_score}")



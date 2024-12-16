from rl_agent.train import train_agent, evaluate
from rl_agent.agent import DQNAgent
from rl_agent.environment import BrickBreakerEnv
import matplotlib.pyplot as plt
import time

def play_with_trained_agent(agent, game):
    state = game.reset()  # Réinitialiser le jeu
    done = False
    total_reward = 0
    agent.epsilon = 0.5  # Désactiver l'exploration

    while not done:
        action = agent.act(state)  # Ne pas explorer, utiliser la politique apprise
        print(f"Action: {action}")  # Afficher l'action dans la console
        state, reward, done = game.step(action)  # L'agent effectue une action et l'état change

        total_reward += reward  # Ajouter la récompense à la récompense totale

        # Mettre à jour le rendu graphique pour Tkinter
        game.render()
        
        # Optionnel : Pause pour ralentir le jeu (ajoute une meilleure expérience visuelle)
        time.sleep(0.005)

        # Afficher le score et l'état du jeu dans la console (facultatif)
        print(f"Total reward: {total_reward}")
        print(f"Game done: {done}")

    print(f"Final score: {total_reward}")



if __name__ == "__main__":
    # train_agent(episodes=10)  # Entraîne l'agent pour 500 épisodes
    # print("Training complete. Evaluating agent...")
    # evaluate(num_episodes=1)  # Évaluation de l'agent après l'entraînement
    # env = BrickBreakerEnv()
    # agent = DQNAgent(state_size=env.observation_space, action_size=len(env.action_space))
    # agent.load_model("models/final_models.h5")  # Charger le modèle entraîné
    # print("Model loaded. Starting game...")
    train_agent(train = False, episodes=1)  # Entraîne l'agent pour 500 épisodes

    # # Jouer avec l'agent entraîné
    # load the model and put it in the agent

    #play_with_trained_agent(agent, env)









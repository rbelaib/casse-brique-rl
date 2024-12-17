import argparse
from rl_agent.train import play_agent, evaluate
from rl_agent.agent import DQNAgent
from rl_agent.environment import BrickBreakerEnv
import matplotlib.pyplot as plt
import time

def play_with_trained_agent(agent, game):
    """ Joue avec un agent entraîné."""
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


def main():
    # Configurer les arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Train or play with a BrickBreaker RL Agent.")
    parser.add_argument("mode", nargs="?", default="play", choices=["train", "play"],
                        help="Mode: train the agent or play with a trained model. Default is 'play'.")
    parser.add_argument("--epochs", type=int, default=1, help="Number of epochs for training or playing.")
    parser.add_argument("--model", type=str, default="models/final_models.h5", help="Path to save or load the model.")

    args = parser.parse_args()

    if args.mode == "train":
        print(f"Training the agent for {args.epochs} epochs.... Model will be saved to {args.model}")
        play_agent(epochs=args.epochs, model_path=args.model)
    elif args.mode == "play":
        print(f"Playing the game with model: {args.model}...")
        play_agent(epochs=1, train=False, model_path=args.model)

if __name__ == "__main__":
    main()
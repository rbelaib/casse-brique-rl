import tensorflow as tf
import numpy as np
import random
from collections import deque
from tensorflow.keras.losses import MeanSquaredError
import pickle

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Facteur de réduction
        self.epsilon = 1.0  # Taux d'exploration initial
        self.epsilon_decay = 0.995 # Taux de décroissance de l'exploration à chaque epoch
        self.epsilon_min = 0.01 # Taux d'exploration minimal
        self.learning_rate = 0.001 # Taux d'apprentissage
        self.model = self._build_model()

    def _build_model(self):
        """Neural network assez simple"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                      loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        """Ajoute une expérience à la mémoire."""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Choisit une action en fonction de l'état."""
        if np.random.rand() <= self.epsilon:
            return random.choice(range(self.action_size))  # Exploration
        q_values = self.model.predict(state[np.newaxis])
        return np.argmax(q_values[0])  # Exploitation

    def replay(self, batch_size):
        """Entraine le modèle en utilisant des expériences passées."""
        if len(self.memory) < batch_size:
            return

        # Ecriture d'un batch aléatoire de la mémoire
        batch = random.sample(self.memory, batch_size)
        
        # Prépare l'état et l'état suivant (pour que ça aille plus vite)
        states = np.array([sample[0] for sample in batch])
        next_states = np.array([sample[3] for sample in batch])
        q_values = self.model.predict(states)
        q_values_next = self.model.predict(next_states)

        for i, (state, action, reward, next_state, done) in enumerate(batch):
            target = reward
            if not done:
                target += self.gamma * np.amax(q_values_next[i])  # On utilise les q-values de l'état suivant
            q_values[i][action] = target  # On update la q-value de l'action choisie

        # entraînement du modèle sur le batch
        self.model.fit(states, q_values, batch_size=batch_size, epochs=1, verbose=0)


    def update_epsilon(self, reward_total):
        """Réduit epsilon pour moins d'exploration au fil du temps."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        # Si le modèle obtient un bon score, on réduit l'exploration plus rapidement
        # Je ne sais pas si c'est vraiment une bonne idée, mais les résultats obtenus ne sont pas mauvais
        if reward_total > -50:
            self.epsilon *= 0.8
        if reward_total > 0:
            self.epsilon *= 0.5

    def save(self, path):
        """Sauvegarde le modèle."""
        self.model.save(path)

    def load_model(self, path):
        """Charge un modèle sauvegardé."""
        self.model = tf.keras.models.load_model(path, custom_objects={'mse': MeanSquaredError()})


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
        self.memory = deque(maxlen=2000)  # Replay buffer
        self.gamma = 0.95  # Facteur de réduction
        self.epsilon = 1.0  # Taux d'exploration initial
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        """Construit le modèle du réseau neuronal."""
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
        """Entraîne le modèle avec un échantillon de la mémoire."""
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state[np.newaxis])[0])
            target_f = self.model.predict(state[np.newaxis])
            target_f[0][action] = target
            self.model.fit(state[np.newaxis], target_f, epochs=1, verbose=0)

    def update_epsilon(self):
        """Réduit epsilon pour moins d'exploration au fil du temps."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, path):
        """Sauvegarde le modèle."""
        self.model.save(path)

    def load_model(self, path):
        """Charge un modèle sauvegardé."""
        self.model = tf.keras.models.load_model(path, custom_objects={'mse': MeanSquaredError()})
    
    def save_agent(self, path):
        """Sauvegarde l'agent."""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    def load_agent(path):
        """Charge un agent sauvegardé."""
        with open(path, 'rb') as f:
            return pickle.load(f)
            


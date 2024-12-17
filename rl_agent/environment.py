import numpy as np
from game.game import BrickBreakerGame


class BrickBreakerEnv:
    def __init__(self, width=400, height=600):
        """ Initialisation de l'environnement.
        width: largeur de la fenêtre
        height: hauteur de la fenêtre
        """
        self.game = BrickBreakerGame(width, height, manual_control=False)
        self.action_space = [-30, 0, 30]  # Paddle : gauche, immobile, droite
        self.observation_space = 5  # ball_x, ball_y, ball_dx, ball_dy, paddle_x
        self.done = False
        self.destroyed_bricks_set = set()  # Pour suivre les briques cassées

    def reset(self):
        """Réinitialise l'environnement et renvoie l'état initial."""
        self.game.restart_game()
        self.done = False
        return self.get_state()

    def step(self, action, previous_brick_count):
        """ Exécute une action et renvoie l'état suivant, la récompense, et si le jeu est terminé."""
        # Mouvement du paddle et de la balle
        reward_instant = 0
        self.game.paddle.move(action)
        self.game.ball.move()
        self.game.check_collisions() # Gestion des collisions
        len_bricks = len(self.game.bricks)
        if len_bricks < previous_brick_count:
            reward_instant = 10 # Récompense pour avoir cassé une brique
            
        # Punir si la balle tombe hors écran
        if self.game.ball.get_coords()[3] >= self.game.height - 10:
            reward_instant = -100  # Pénalité pour perte de balle

        # Vérifier si le jeu est terminé
        if len(self.game.bricks) == 0 or self.game.ball.get_coords()[3] >= self.game.height - 10:
            print("GAME OVER !!")
            self.done = True
        return self.get_state(), reward_instant, self.done, len_bricks


    def get_state(self):
        """Renvoie les informations nécessaires à l'agent pour décider."""
        ball_coords = self.game.ball.get_coords()
        paddle_coords = self.game.paddle.get_coords()
        return np.array([
            ball_coords[0], ball_coords[1], self.game.ball.dx, self.game.ball.dy, paddle_coords[0]
        ])

    def render(self):
        """Met à jour l'affichage."""
        self.game.canvas.update()

import numpy as np
from game.game import BrickBreakerGame


class BrickBreakerEnv:
    def __init__(self, width=400, height=600):
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

    def step(self, action):
        # Mouvement du paddle et de la balle
        len_bricks = len(self.game.bricks)
        self.game.paddle.move(action)
        self.game.ball.move()
        self.game.check_collisions()
        reward_instant = 0
        if len(self.game.bricks) < len_bricks:
            reward_instant = 10


        # Punir si la balle tombe hors écran
        if self.game.ball.get_coords()[3] >= self.game.height - 10:
            reward_instant = -100  # Pénalité pour perte de balle

        # Vérifier si le jeu est terminé
        if len(self.game.bricks) == 0 or self.game.ball.get_coords()[3] >= self.game.height - 10:
            print("GAME OVER !!")
            self.done = True
        return self.get_state(), reward_instant, self.done


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

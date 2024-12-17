from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
import tkinter as tk
import math

class BrickBreakerGame:
    def __init__(self, width=400, height=600, manual_control=True):
        """ Initialisation du jeu.
        width: largeur de la fenêtre
        height: hauteur de la fenêtre
        manual_control : activation du contrôle manuel"""
        self.width = width
        self.height = height
        self.manual_control = manual_control  # Contrôle manuel activé ou non
        self.score = 0  # Initialisation du score

        # Initialisation de la fenêtre et du canvas
        self.window = tk.Tk()
        self.window.title("Brick Breaker")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Initialisation des éléments du jeu
        self.paddle = Paddle(self.canvas, x=self.width // 2, y=self.height - 20)
        self.ball = Ball(self.canvas, x=self.width // 2, y=self.height - 50)
        self.bricks = []
        self.create_bricks()

        # Affichage du score
        self.score_text = self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 12)
        )

        # Liaison des contrôles (si manuel)
        if self.manual_control:
            self.window.bind("<Left>", lambda _: self.paddle.move(-30))  # Vitesse augmentée
            self.window.bind("<Right>", lambda _: self.paddle.move(30))  # Vitesse augmentée

        # Démarrer le jeu
        self.run_game()

    def create_bricks(self):
        """Crée les briques en haut de l'écran."""
        rows = 5
        cols = 8
        brick_width = self.width // cols
        brick_height = 20
        for row in range(rows):
            for col in range(cols):
                x1 = col * brick_width
                y1 = row * brick_height
                x2 = x1 + brick_width
                y2 = y1 + brick_height
                brick = Brick(self.canvas, x1, y1, x2, y2)
                self.bricks.append(brick)

    def check_collisions(self):
        """Gère les collisions entre la balle, la raquette, et les briques."""
        ball_coords = self.ball.get_coords()

        # Rebonds sur les murs
        if ball_coords[0] <= 0 or ball_coords[2] >= self.width:
            self.ball.bounce_horizontal()
        if ball_coords[1] <= 0:
            self.ball.bounce_vertical()

        # Rebonds sur la raquette
        paddle_coords = self.paddle.get_coords()
        if (ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and
                ball_coords[3] >= paddle_coords[1] and ball_coords[1] <= paddle_coords[3]):
            self.ball.bounce_vertical()

        # Collision avec les briques
        for brick in self.bricks:
            brick_coords = brick.get_coords()
            if (ball_coords[2] >= brick_coords[0] and ball_coords[0] <= brick_coords[2] and
                    ball_coords[3] >= brick_coords[1] and ball_coords[1] <= brick_coords[3]):
                self.bricks.remove(brick)
                self.ball.bounce_vertical()
                self.update_score(10)  # Incrément du score
                brickid = id(brick)
                brick.destroy()
                return brickid
        return None

    def update_score(self, points):
        """Met à jour le score et rafraîchit l'affichage."""
        self.score += points
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def restart_game(self):
        """Redémarre le jeu lorsque la balle tombe."""
        self.canvas.delete("all")  # Efface tout
        self.score = 0  # Réinitialise le score
        self.bricks = []
        self.create_bricks()  # Reconstruit les briques
        self.paddle = Paddle(self.canvas, x=self.width // 2, y=self.height - 20)
        self.ball = Ball(self.canvas, x=self.width // 2, y=self.height - 50)
        self.score_text = self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 12)
        )
        
    def is_ball_colliding_with_brick(self, brick):
        ball_coords = self.ball.get_coords()
    # Collision avec les briques
        for brick in self.bricks:
            brick_coords = brick.get_coords()
            if (ball_coords[2] >= brick_coords[0] and ball_coords[0] <= brick_coords[2] and
                    ball_coords[3] >= brick_coords[1] and ball_coords[1] <= brick_coords[3]):
                return True
        return False


    def run_game(self):
        """Boucle principale du jeu."""
        self.ball.move()
        self.check_collisions()
        self.window.after(10, self.run_game)

    def start(self):
        """Démarre le jeu."""
        self.window.mainloop()
        
    def check_for_destroyed_bricks(self):
        """ Vérifie si des briques ont été détruites par la balle et les renvoie."""
        destroyed_bricks = []
        for brick in self.bricks:
            if self.is_ball_colliding_with_brick(brick):
                destroyed_bricks.append(brick)
        return destroyed_bricks

if __name__ == "__main__":
    # Par défaut, le jeu est en mode manuel (modifiable via le paramètre manual_control)
    game = BrickBreakerGame(manual_control=True)
    game.start()

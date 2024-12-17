class Ball:
    def __init__(self, canvas, x, y, radius=10, color="grey"):
        """
        Initialise la balle.
        :param canvas: Canvas Tkinter où la balle est dessinée.
        :param x: Position X du centre de la balle.
        :param y: Position Y du centre de la balle.
        :param radius: Rayon de la balle.
        :param color: Couleur de la balle.
        """
        self.canvas = canvas
        self.radius = radius
        self.color = color
        self.ball = canvas.create_oval(
            x - radius, y - radius, 
            x + radius, y + radius, 
            fill=color
        )
        self.dx = 4  # Vitesse horizontale
        self.dy = -4  # Vitesse verticale

    def move(self):
        """
        Déplace la balle dans sa direction actuelle.
        """
        self.canvas.move(self.ball, self.dx, self.dy)

    def get_coords(self):
        """
        Retourne les coordonnées actuelles de la balle.
        :return: Tuple (x1, y1, x2, y2) représentant les bords de la balle.
        """
        return self.canvas.coords(self.ball)

    def bounce_horizontal(self):
        """
        Inverse la direction horizontale de la balle.
        """
        self.dx = -self.dx

    def bounce_vertical(self):
        """
        Inverse la direction verticale de la balle.
        """
        self.dy = -self.dy

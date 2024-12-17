class Paddle:
    def __init__(self, canvas, x, y, width=80, height=10, color="white"):
        """ Initialise la raquette. """
        self.canvas = canvas
        self.width = width
        self.height = height
        self.color = color
        self.id = canvas.create_rectangle(x - width // 2, y - height // 2, x + width // 2, y + height // 2, fill=color)

    def move(self, dx):
        """Déplace la raquette horizontalement de dx pixels, en restant dans les limites de l'écran."""
        coords = self.get_coords()
        # Vérifie si le paddle reste dans les limites
        if coords[0] + dx < 0:  # Limite gauche
            dx = -coords[0]
        elif coords[2] + dx > self.canvas.winfo_width():  # Limite droite
            dx = self.canvas.winfo_width() - coords[2]

        self.canvas.move(self.id, dx, 0)

    def get_coords(self):
        """Renvoie les coordonnées actuelles du paddle."""
        return self.canvas.coords(self.id)

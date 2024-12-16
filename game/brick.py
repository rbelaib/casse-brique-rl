class Brick:
    def __init__(self, canvas, x1, y1, x2, y2, color="blue"):
        """
        Initialise une brique.
        :param canvas: Canvas Tkinter où la brique est dessinée.
        :param x1, y1: Coordonnées du coin supérieur gauche.
        :param x2, y2: Coordonnées du coin inférieur droit.
        :param color: Couleur de la brique.
        """
        self.canvas = canvas
        self.brick = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def get_coords(self):
        """
        Retourne les coordonnées de la brique.
        :return: Tuple (x1, y1, x2, y2) représentant les bords de la brique.
        """
        return self.canvas.coords(self.brick)

    def destroy(self):
        """
        Supprime la brique du canvas.
        """
        self.canvas.delete(self.brick)
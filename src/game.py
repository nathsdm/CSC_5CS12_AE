class Game:
    """
    Classe de base pour les jeux.
    """
    def __init__(self):
        self.status : str = "playing" # playing, won or lost
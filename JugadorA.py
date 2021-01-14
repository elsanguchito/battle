import random
from Jugador import Player

class AutomaticPlayer(Player):
    """ AutomaticPlayer representa la computadora que un \
    el usuario jugará contra.
    """

    def __init__(self):
        """ Initializes the AutomaticPlayer class.
        """
        super().__init__()

    def guess_location(self):
        """Representa las conjeturas del jugador.
         Las conjeturas no se repetirán.
         Devoluciones:
             (x, y) coordenada de conjetura."""
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in self.selection_history:
                self.selection_history.append((x, y))
                return (x, y)

    def set_battleships(self):
        """ Traza todo el acorazado de AutomaticPlayer. Solo se debe llamar una vez. Trazarán los siguientes barcos:
        1. Longitud del acorazado: 5
        2. Longitud del acorazado: 4
        3. Longitud del acorazado: 3
        4. Longitud del acorazado: 2
        5. Longitud del acorazado: 1
        Actualiza la variable de objeto battleship_set, que es una lista de 5 elementos.
        Cada elemento representa el acorazado \
        usando el formato:
        (inicio_x, inicio_y, fin_x, fin_y, tamaño)
        """

        battleship_length = 1
        while battleship_length < 6:
            h_or_v = random.randint(0, 1) # Si es 0, el acorazado será horizontal. Si es 1, será vertical.
            validity = 0 # Obtención de una x y válida
            while validity == 0:
                x_head = random.randint(0, 9)
                y_head = random.randint(0, 9)
                if ((h_or_v == 0 and (x_head + battleship_length - 1 < 10)) or
                        (h_or_v == 1 and (y_head - battleship_length - 1 >= 0))):  # El barco está a bordo
                    validity = self.valid_location(self.placements, x_head, y_head, battleship_length, h_or_v)
                    if validity == 1:  # Agregar este acorazado a la placa interna y al conjunto battleship_set
                        self.update_internal_board(self.placements, x_head, y_head, battleship_length, h_or_v)
                        if h_or_v == 0:
                            self.battleship_set.append(
                                (x_head, y_head, x_head + battleship_length - 1, y_head, battleship_length))
                        else:
                            self.battleship_set.append(
                                (x_head, y_head, x_head, y_head - battleship_length + 1, battleship_length))
            battleship_length = battleship_length + 1
        return self.battleship_set



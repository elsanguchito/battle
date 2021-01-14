from Jugador import Player

class PersonPlayer(Player):
    """
PersonPlayer representa al ser humano contra el que jugará ComputerPlayer.
    """

    def __init__(self):
        """ Inicializa la clase PersonPlayer.
        """
        super().__init__()

    def set_battleship(self, x_head, y_head, battleship_length):
        """ Traza uno de los acorazados de PersonPlayer con tamaño: longitud comenzando en la coordenada (x_head, y_head).
        Agrega una lista de 5 elementos a la lista de ubicaciones. Cada elemento representa el acorazado usando el formato:
        (inicio_x, inicio_y, fin_x, fin_y, tamaño)

        """
        validity = 0
        h_or_v = -1
# -1 representa que la orientación del acorazado está indecisa
        if ((x_head + battleship_length - 1 < 10)):
            h_or_v = 0 # 0 representa que la orientación del acorazado es horizontal
            validity = self.valid_location(self.placements, x_head, y_head, battleship_length, h_or_v)
        elif ((y_head - battleship_length - 1 >= 0)):  # Ship is within board
            h_or_v = 1 # 1 representa que la orientación de los acorazados es vertical
            validity = self.valid_location(self.placements, x_head, y_head, battleship_length, h_or_v)
            
        if validity == 1: # Agregar este acorazado a la placa interna y al conjunto battleship_set
            self.update_internal_board(self.placements, x_head, y_head, battleship_length, h_or_v)
            if h_or_v == 0:
                self.battleship_set.append(
                    (x_head, y_head, x_head + battleship_length - 1, y_head, battleship_length))
            else:
                self.battleship_set.append(
                    (x_head, y_head, x_head, y_head - battleship_length + 1, battleship_length))

        return self.battleship_set

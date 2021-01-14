#Constantes
NEUTRAL = 0
HIT = 1
MISS = 2
SHIP = 3

'''

Un tablero es una cuadrícula estándar de 10 * 10 donde cada cuadrado puede tener un estado
'neutral', 'acertar', 'fallar' o 'enviar'.
'''
class Board:

    '''

Cree un objeto de tablero y establezca cada posición en el tablero en NEUTRO.
    '''
    def __init__(self):
        self.status = [[],[],[],[],[],[],[],[],[],[]]
        self.ships = []
        self.number_of_ships = 0

        for i in range(10):
            for j in range(10):
                self.status[i].append(NEUTRAL)

    '''

Devuelve Verdadero si no hay barcos en el tablero.
    '''
    def all_ships_sunk(self):
        return self.ships == []
            

    '''

Devuelve una tupla del estado del movimiento y una lista de
    las coordenadas golpean.
    '''
    def move(self, x, y):
        ans = []
        if (0 <= x <= 9) and (0 <= y <= 9):
            if self.status[x][y] != SHIP:
                self.status[x][y] = MISS
                return MISS, []
            else:
                for ship in self.ships:
                    if (x, y) in ship:
                        for coord in ship:
                            self.status[coord[0]][coord[1]] = HIT
                            ans.append(coord)
                        self.ships.remove(ship)
                        return HIT, ans
        return (None, [])


    '''
  
Devuelve las coordenadas inicial y final del barco. Si las dimensiones
    proporcionados no son válidos, devuelve ninguno.
    '''
    def board_add_ship(self, start_x, start_y, end_x, end_y, size):

        # Comprueba que las coordenadas estén dentro de los límites del tablero
        if not ((0 <= start_x <= 9) and (0 <= start_y <= 9) and \
                (0 <= end_y <= 9) and (0 <= end_x <= 9)):
            return

        # Comprueba que el barco esté en una fila o en una columna
        elif abs(start_x - end_x) > 1 and abs(start_y - end_y) > 1:
             return

        # Comprueba que las dimensiones proporcionadas coinciden con el tamaño del barco
        x_dist = abs(start_x - end_x) + 1
        y_dist = abs(start_y - end_y) + 1

        if (x_dist * y_dist) == size:
            if (start_x < end_x):
                start_pt_x = start_x
                end_pt_x = end_x
            else:
                start_pt_x = end_x
                end_pt_x = start_x

            if (start_y < end_y):
                start_pt_y = start_y
                end_pt_y = end_y
            else:
                start_pt_y = end_y
                end_pt_y = start_y

            self.ships.append([])
            for x in range(start_pt_x, end_pt_x + 1):
                for y in range(start_pt_y, end_pt_y + 1):
                    self.status[x][y] = SHIP
                    self.ships[self.number_of_ships].append((x, y))
            self.number_of_ships = self.number_of_ships + 1
            return (start_pt_x, end_pt_x, start_pt_y, end_pt_y)

        return

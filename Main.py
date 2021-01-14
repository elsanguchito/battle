import pygame
from JugadorA import*
from Mostrar_tablero import*
from Personajugador import*
from Estadisticas import*
import time
import random

FPS = 30
HEIGHT = 1000
WIDTH = 500
P_SHIPS = []
BORDER_WIDTH = 235
BORDER_HEIGHT = 35
REQ_SHIP_SIZE = 40
MAX_SCORE = 5
MOUSE_POS_X = 430
MOUSE_POS_Y = 130
RESTRICT_X = 775
RESTRICT_Y = 475
MARGIN = 5
SIZE = 30


class Start(pygame.sprite.Sprite):


    def __init__(self, auto, person, stats, vboard, vb_auto, vb_player, p_ships):

        super(Start, self).__init__()
        self.auto = auto
        self.stats = stats
        self.person = person
        self.vboard = vboard
        self.vb_auto = vb_auto
        self.vb_player = vb_player
        self.win = (False, "")
        self.player1_score = 0# el jugador humano es el jugador 1
        self.player2_score = 0 #computadora es el jugador 2
        self.turns = 0 # 0 significa el turno del jugador humano para jugar, 1 significa que es el turno de las computadoras.
        self.p_ships = p_ships # a list of ships
        self.guesses = 0
        

    def set_auto_ships(self):

        ships = self.auto.set_battleships()
        for enemy_ships in ships:
                self.vb_auto.add_ship(enemy_ships[0], enemy_ships[1],\
                                     enemy_ships[2], enemy_ships[3], enemy_ships[4])

    def set_person_ships(self):

        ships = self.p_ships
        for person_ships in ships:
                self.vb_player.add_ship(person_ships[0], person_ships[1],\
                                     person_ships[2], person_ships[3], person_ships[4])
          
                
    def play_ai(self):

        pos = self.auto.guess_location()
        no_go = self.update(self.vb_player, pos[0], pos[1])
        if no_go == None:
            no_go = []
        if no_go != []:
            self.player2_score = self.player2_score + 1
        self.auto.avoid_plots(no_go)
        
    def update(self, obj, coord_x, coord_y):

        no_go = obj.viewable_move(coord_x, coord_y)
        return no_go
                
        
    def display_score(self):

        font = pygame.font.SysFont(""'couriernew'"", 19)
        font.set_bold(True)
        mess_1 = "Jugador score: {}".format(self.player1_score)
        mess_2 = "IA score: {}".format(self.player2_score)
        txt1 = font.render(mess_1, True, (0, 128, 0))
        txt2 = font.render(mess_2, True, (0, 128, 0)) 
        self.vboard.blit(txt1, (150, 100))
        self.vboard.blit(txt2, (500, 100))

    def set_border(self):

        pygame.draw.rect(self.vboard, BLUE, pygame.Rect(10, 10, HEIGHT - BORDER_WIDTH, WIDTH - BORDER_HEIGHT), 3)    
        


    def display_stats(self):

        font = pygame.font.SysFont("agencyfb", 25)
        mess_1 = "Num. de barcos: "
        mess_2 = "Barcos Faltantes: "
        mess_3 = "Numero acertados: {}".format(self.guesses)
        txt1 = font.render(mess_1, True, (0, 127, 0))
        txt2 = font.render(mess_2, True, (0, 127, 0))
        txt3 = font.render(mess_3, True, (0, 127, 0))
        play_score_msg1 = font.render("Player1: {}  Computer: {}".format(MAX_SCORE, MAX_SCORE), True, (0, 127, 0))
        play_score_msg2 = font.render("Player1: {}  Computer: {}".format(MAX_SCORE - self.player1_score, MAX_SCORE - self.player2_score), True, (0, 127, 0))
        self.vboard.blit(txt1, (800, 100))
        self.vboard.blit(txt2, (800, 200))
        self.vboard.blit(txt3, (800, 300))
        self.vboard.blit(play_score_msg1, (810, 130))
        self.vboard.blit(play_score_msg2, (810, 230))

    def quit(self):

        pygame.quit()
        sys.exit()

#NOTA: este aspecto del archivo (clase de inicio) es principalmente para la pantalla de bienvenida de la clase de inicio.
class Begin:


    def __init__(self, player_board, user_board, person):

        self.player_board = player_board
        self.user_board = user_board
        self.person = person
        self.required_ships = [5, 4, 3, 2, 1]# número de barcos (5 barcos) necesarios para jugar el juego.
        self.num_set_ships = 0

    def show_required(self, color, index):

        x = 5
        for row in range(5):
            for column in range(x):
                if index == x:
                    pygame.draw.rect(self.player_board,
                                 color,
                                 pygame.Rect(800+(REQ_SHIP_SIZE * column), 200+(REQ_SHIP_SIZE * row), 30, 30))
                else:
                    pygame.draw.rect(self.player_board,
                                     WHITE,
                                     pygame.Rect(800+(REQ_SHIP_SIZE * column), 200+(REQ_SHIP_SIZE * row), 30, 30))
            x -= 1
            
    def set_player_ships(self, x_head, y_head, battleship_length):

        person = self.person.set_battleship(x_head, y_head, battleship_length)
        if(len(person) > 0):
            person_ships = person[-1]
            self.user_board.add_ship(person_ships[0], person_ships[1],\
                                         person_ships[2], person_ships[3], person_ships[4])
            P_SHIPS.append((person_ships[0], person_ships[1],\
                                         person_ships[2], person_ships[3], person_ships[4]))

    
    def display_info(self):

        title = pygame.font.SysFont("ocraextended", 40)
        font = pygame.font.SysFont("'couriernew'", 19)
        font.set_bold(True)
        main_title = title.render("Battle of the Titans", True, (0, 128, 0))
        self.player_board.blit(main_title, (145, 40))
        txt1 = font.render("1. Elige la posicion del barco", True, (0, 128, 0))
        txt2 = font.render("2. Presiona cualquier", True, (0, 128, 0))
        txt3 = font.render("tecla para iniciar", True, (0, 128, 0))
        self.player_board.blit(txt1, (50, 150))
        self.player_board.blit(txt2, (50, 250))
        self.player_board.blit(txt3, (50, 270))
        font = pygame.font.SysFont("couriernew", 17)
        mess_1 = "Barcos: "
        font.set_bold(True)
        txt1 = font.render(mess_1, True, (0, 127, 0))
        self.player_board.blit(txt1, (800, 150))
        
        

    def update(self, human_player, coord_x, coord_y):

        human_player.viewable_move(coord_x, coord_y)

    def set_border(self):

        pygame.draw.rect(self.player_board, BLUE, pygame.Rect(10, 10, HEIGHT - BORDER_WIDTH, WIDTH - BORDER_HEIGHT), 3)

    
def main():      
    pygame.init()
    DISPLAY=pygame.display.set_mode((1000,500),0,32)
    DISPLAY.fill(BLACK)
    pygame.display.set_caption("BattleShip--1.0")
    user_board = VisibleUserBoard(DISPLAY)
    person = PersonPlayer()

    begin = Begin(DISPLAY, user_board, person)
    begin.display_info()
    begin.set_border()
    begin.show_required(WHITE, 0)

    begin.num_set_ships = 0
    def mouse_event(event, start, size):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if MOUSE_POS_X <= mouse_pos[0] <= RESTRICT_X and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y:
                col = mouse_pos[0] - MOUSE_POS_X
                rw = mouse_pos[1] - MOUSE_POS_Y
                column = col // (size + MARGIN)
                row = rw // (size + MARGIN)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('jump.wav'))
                if len(begin.required_ships) > 0:
                    begin.set_player_ships(column, row, begin.required_ships[0])
                    popped_val = begin.required_ships.pop(0)
                    begin.show_required(RED, popped_val)
                    begin.num_set_ships += 1
            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Buzzer.wav'))
                
    pygame.mixer.music.load('look.wav')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and begin.num_set_ships >= 5:
                run = False
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.load('look.wav')
                pygame.mixer.music.play()
            n_event = mouse_event(event, begin, 30) # llamada función de evento del mouse
        pygame.display.update()
    
    

if __name__ == '__main__':
    def mouse_event(mouse_pos, start):

        if REQ_SHIP_SIZE <= mouse_pos[0] <= (RESTRICT_X - 390) and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y:
            col = mouse_pos[0] - REQ_SHIP_SIZE
            rw = mouse_pos[1] - MOUSE_POS_Y
            column = col // (SIZE + MARGIN)
            row = rw // (SIZE + MARGIN)
            no_go = start.update(start.vb_auto, column, row)
            if no_go != None and no_go != []:
                start.player1_score = start.player1_score + 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('jump.wav'))
            start.guesses += 1
            start.turns = 1
            
    stats = Stats()
    auto = AutomaticPlayer()
    person = PersonPlayer()
    main()
    
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    DISPLAY=pygame.display
    main_board = DISPLAY.set_mode((HEIGHT, WIDTH),0,32)
    main_board.fill(BLACK)
    DISPLAY.set_caption("BattleShip--1.0")
    user_board = VisibleUserBoard(main_board)
    enemy_board = VisibleEnemyBoard(main_board)
    
    start = Start(auto, person, stats, main_board, enemy_board, user_board, P_SHIPS);
    start.set_auto_ships()
    start.set_border()
    start.set_person_ships()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('look.wav'))
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    win = 0 #final del juego si es igual a 1

    running = True
    while running:
        #controlador de eventos
        for event in pygame.event.get():
            start.display_score()
            start.display_stats()
            if event.type==QUIT:
                start.quit()
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.load('look.wav')
                pygame.mixer.music.play()
            if win == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start.turns == 0:
                        m_event = mouse_event(mouse_pos, start)
                        if start.vb_auto.all_ships_sunk():
                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(315, 80, 40, 40))

                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(680, 80, 40, 40))

                            pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(800, 230, 300, 30))
                        

                            start.display_score()
                            start.display_stats()
                            title = pygame.font.SysFont("'couriernew'", 40)
                            title.set_bold(True)
                            main_title = title.render("Player Gana!", True, (0, 128, 0))
                            main_board.blit(main_title, (210, 40))
                            start.display_score()
                            start.display_stats()
                            win = 1
                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(960, 300, 40, 40))
                        
                    else:
                        start.play_ai()
                        if start.vb_player.all_ships_sunk():
                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(315, 80, 40, 40))

                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(680, 80, 40, 40))

                            pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(800, 230, 300, 30))
                        
                            start.display_score()
                            start.display_stats()
                            title = pygame.font.SysFont("'couriernew'", 40)
                            title.set_bold(True)
                            main_title = title.render("Computer gana!", True, (0, 128, 0))
                            main_board.blit(main_title, (175, 40))
                            start.display_score()
                            start.display_stats()
                            win = 1
                        pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(960, 300, 40, 40))
                        start.turns = 0

                    if (win == 0):
                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(315, 80, 40, 40))

                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(680, 80, 40, 40))

                        pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(800, 230, 300, 30))
                
        pygame.display.flip()
        clock.tick(FPS)
        
            

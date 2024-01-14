import pygame
from pygame.locals import *
from sys import exit 
from config import *
from random import randint
from utils import *

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SquareHunt")

        

        # 0 - menu inicial 
        # 1 - jogando
        # 2 - game over 
        self.system_state = 0

        # controle de seleção nos menus 
        self.menu_selection = 0
        self.max_menu_selection = 0
        self.menu_functions = []
        self.menu_options = []
        self.selected = False       # controla se o enter foi pressionado nos menus

        # variaveis de controle
        self.game_over = False

        self.running = True
        self.clock = pygame.time.Clock() 
        self.best_score = 0
        

        self.load_dependences() 
        self.start() 

    def start(self):
        pygame.init()
        # pygame.mixer.init()

        self.show_start_screen()
        # self.system_state = 1
        while self.running: 

            self.clock.tick(30)
            self.events()

            if self.system_state == 0: 
                self.show_start_screen()
            elif self.system_state == 2: 
                self.show_game_over_screen() 

            pygame.display.flip()

    def game_run(self): 
        self.system_state = SYSTEM_GAME_RUNNING
        running = True

        self.player_x = 0
        self.player_y = 0
        self.target_x = 145
        self.target_y = 145
        self.speed = INITIAL_SPEED
        self.actual_score = 0


        while running: 
            self.clock.tick(30)
            self.screen.fill(BACKGROUND_COLOR)
            self.game_events()

            self.target = pygame.draw.rect(self.screen, TARGET_COLOR, (self.target_x, self.target_y, TARGET_WIDTH, TARGET_HEIGHT))
            self.player = pygame.draw.rect(self.screen, PLAYER_COLOR, (self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

            if self.player.colliderect(self.target):
                self.actual_score += 1
                self.target_x, self.target_y = change_target_position()
                self.speed += 2
            

            if game_over(self.player):
                self.system_state = SYSTEM_GAME_OVER
                running = False
                if self.actual_score > self.best_score: self.best_score = self.actual_score
                self.show_game_over_screen() 

            self.show_text(
                f"SCORE: {self.actual_score}",
                30,
                SCORE_COLOR,
                80,
                30
            )
            self.show_text(
                f"BEST SCORE: {self.best_score}",
                30,
                SCORE_COLOR,
                80,
                50
            )

            pygame.display.flip()


    def game_events(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    self.target_x, self.target_y = change_target_position()

        if pygame.key.get_pressed()[K_w]:
            self.player_y = self.player_y - self.speed
        if pygame.key.get_pressed()[K_a]:
            self.player_x = self.player_x - self.speed
        if pygame.key.get_pressed()[K_s]:
            self.player_y = self.player_y + self.speed
        if pygame.key.get_pressed()[K_d]:
            self.player_x = self.player_x + self.speed


    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 
                exit()

    def show_text(self, texto, tamanho, cor, x, y): 
        fonte = pygame.font.Font(pygame.font.match_font('cabril'), tamanho)
        texto  = fonte.render(texto, False, cor)
        texto_rect = texto.get_rect() 
        texto_rect.center = (x, y)
        self.screen.blit(texto, texto_rect)

    def update_sprites(self):
        pass

    # cria todas as dependencias do game (spritesheet)
    def load_dependences(self): 
        pass



    def show_start_screen(self): 
        self.system_state = SYSTEM_START_MENU
        # self.menu_selection = 0
        # self.max_menu_selection = 3

        while self.system_state == SYSTEM_START_MENU: 
            self.clock.tick(30)
            self.screen.fill(BACKGROUND_COLOR)

            self.show_text(
                "SquareHunt",
                80, 
                (255, 255, 255), 
                WIDTH // 2,
                100
            )

            self.selection_screen_events() 
            self.show_selection_menu(
                ["SinglePlayer", "Multiplayer", "Records", "How to play?", "Quit"], 
                [self.game_run, self.neutre_method, self.neutre_method, self.neutre_method, self.exit]
            )

            pygame.display.flip()


    def show_game_over_screen(self): 
        self.system_state = SYSTEM_GAME_OVER
        # self.menu_selection = 0
        # self.max_menu_selection = 3

        while self.system_state == SYSTEM_GAME_OVER: 
            self.clock.tick(30)
            self.screen.fill(BACKGROUND_COLOR)

            self.show_text(
                "Game over!",
                80, 
                (255, 255, 255), 
                WIDTH // 2,
                100
            )

            self.selection_screen_events() 
            self.show_selection_menu(
                ["Play again", "Start Menu", "Quit"], 
                [self.game_run, self.show_start_screen, self.exit]
            )

            pygame.display.flip()

    def selection_screen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 
                exit()

            if event.type == KEYUP:
                if event.key == K_DOWN: self.menu_selection += 1 if self.menu_selection + 1 <= self.max_menu_selection else  0
                if event.key == K_UP:self.menu_selection -= 1 if self.menu_selection - 1 >= 0 else 0
                if event.key == K_KP_ENTER: self.selected = True
                print(self.menu_selection)

    # renderiza um menu com os nomes passados
    def show_selection_menu(self, list_option_names , option_functions):
        if self.selected:
            self.selected = False
            option = self.menu_selection
            self.menu_selection = 0
            option_functions[option]() 

        if len(list_option_names) == len(option_functions):
            # self.menu_selection = 0
            self.max_menu_selection = len(list_option_names) - 1

            for num, name in enumerate(list_option_names):
                ref = "> " if num == self.menu_selection else "  "
                
                self.show_text(
                f"{ref}{name}", 
                30, 
                (255, 255, 255), 
                WIDTH // 2,
                250 + 25 * num
            )


    @staticmethod
    def exit(): 
        pygame.quit() 
        exit()

    @staticmethod
    def neutre_method(message=''): 
        print(message)

Game()

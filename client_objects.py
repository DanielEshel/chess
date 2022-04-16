import pygame.font

from images import *
import chess_utilities
import chess_objects
import time
from graphic_objects import *
from utilities import *


class Graphics:
    board = None
    screen = None
    piece_images = {}

    def __init__(self, input_q, board, start, screen_size=(1000, 900)):
        """
        init the pygame graphic section
        :param screen_size: wanted size of screen
        :param input_q: queue for input
        """
        self.input_q = input_q
        self.screen_number = 1
        self.screen_size = screen_size
        self.end = False
        self.start = start
        self.colors = {
            "button_text": (201, 140, 112),
            "titles": (227, 181, 135),
            "button": (39, 54, 70),
            "button_hover": (90, 105, 121),
            "button_pressed": (49, 67, 87),
            "time_text": (0, 0, 0)
        }
        Graphics.screen = pygame.display.set_mode(self.screen_size)
        Graphics.board = board

        self.menu_buttons = {}
        self.game_buttons = {}
        self.loading_buttons = {}

        # starting loading screen
        self.screen.blit(starting_img, (0, 0))
        pygame.display.update()
        # create a font object.
        # 1st parameter is the font file which is available in pygame
        # 2nd parameter is size of the font
        pygame.font.init()

        self.fonts = [pygame.font.Font('fonts/TitilliumWeb-SemiBold.ttf', 26),
                      pygame.font.Font('fonts/TitilliumWeb-SemiBold.ttf', 50),
                      pygame.font.Font('fonts/Visage_Bold.otf', 200)]

        Graphics.piece_images = {}
        Graphics.set_images()
        self.build_buttons()

        self._main_loop()
        pygame.quit()

    def _main_loop(self):
        """
        handles the player input
        :return: none
        """
        # Initialize pygame
        pygame.init()

        while True:
            # if got a connection error
            if self.start[0] == 'f':
                self.connection_error()

            # if not
            elif self.start[0] == 's':
                # game screen
                if self.screen_number == 2:
                    self.game_loop()
                # menu screen
                elif self.screen_number == 1:
                    self.menu_loop()
            # end if session ended
            if self.end:
                return

    def connection_error(self):
        """
        handle disconnections of server
        :return: None
        """
        # set font
        font = self.fonts[1]

        # print background
        self.screen.blit(back_img, (0, 0))
        pygame.display.update()

        # draw retry button
        retry_button = get_key('R', self.loading_buttons)
        retry_button.draw()

        # draw text on screen
        text = font.render("can't connect to server", True, self.colors['titles'])
        text_rect = text.get_rect()
        text_rect.center = (500, 200)
        # blit text onto screen
        self.screen.blit(text, text_rect)

        # update pygame
        pygame.display.update()

        # button interactions loop
        while True:
            # if pressed a button (there's only one)
            if self.button_interactions([retry_button]) is not None:
                self.start[0] = 't'

                # starting loading screen
                self.screen.blit(starting_img, (0, 0))
                pygame.display.update()

                self.screen_number = 1
                return

            # return if session ended
            if self.end:
                return

    def game_loop(self):
        """
        main loop when in a game
        :return: None
        """
        # reset board at start of game
        self.board.reset()

        player = None
        opponent = None
        player_pieces = None
        piece_to_move = None
        cancel_button = None
        last_time = None

        while True:

            # if a connection error occurred
            if self.start[0] == 'f':
                self.connection_error()
                return

            # if exited pygame
            if self.end:
                return

            # if game ended
            if self.board.ended:
                # draw background of message
                pygame.draw.rect(self.screen, (218, 219, 221), (100, 300, 700, 350), 0, border_radius=15)

                # print game-ending message
                font = self.fonts[1]
                text = font.render(f"GAME ENDED", True, self.colors["titles"])
                text_rect = text.get_rect()
                text_rect.center = (450, 400)
                self.screen.blit(text, text_rect)
                text = font.render(f"{self.board.ended}", True, self.colors["titles"])
                text_rect = text.get_rect()
                text_rect.center = (450, 500)
                self.screen.blit(text, text_rect)

                pygame.display.update()
                time.sleep(3.5)

                # exit game loop if game ended
                self.screen_number = 1
                return

            # if in a game
            if self.board.orientation is not None and self.board.black is not None:
                # if game not initialized yet
                if player is None:
                    # get player and opponent
                    if self.board.orientation == 'w':
                        player = self.board.white
                        opponent = self.board.black
                    else:
                        player = self.board.black
                        opponent = self.board.white

                    player_pieces = player.pieces

                    self.build_game_screen()

                # if mouse is over the board
                pos = pygame.mouse.get_pos()
                if pos[0] in range(20, 820) and pos[1] in range(50, 850):

                    # handle board input (user making a move)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.end = True
                            return

                        elif event.type == pygame.MOUSEBUTTONUP:
                            print(self.screen_number)
                            # if in game:

                            if self.board.turn == self.board.orientation:
                                move_of_player = (pos[0] - 20) // 100, 7 - (pos[1] - 50) // 100
                                print(move_of_player)
                                # if there isn't a piece selected
                                if piece_to_move is None:
                                    # get piece to move
                                    selected_piece = chess_utilities.get_piece_on_square(move_of_player, player_pieces)
                                    if isinstance(selected_piece, chess_objects.Piece):
                                        piece_to_move = selected_piece

                                        self.screen.blit(chosen_square_img,
                                                         ((817 - (8 - selected_piece.place[0]) * 100),
                                                          (846 - (selected_piece.place[1] + 1) * 100)))
                                        pygame.display.update()

                                else:
                                    # can't move to a square you already have a piece on
                                    if not chess_utilities.get_piece_on_square(move_of_player, player_pieces):
                                        # try to make the move:
                                        old_place_of_piece = piece_to_move.place
                                        if chess_utilities.move(piece_to_move, move_of_player, self.board):
                                            # if this is the first move, change the started flag
                                            if not self.board.started:
                                                self.board.started = True
                                            # if move is valid, add it to the input queue
                                            move = 'M' + str(old_place_of_piece[0]) + str(
                                                old_place_of_piece[1]) + str(
                                                move_of_player[0]) + str(move_of_player[1])
                                            self.input_q.put(move)
                                    piece_to_move = None
                                    self.print_game()

                # if mouse is not over the board
                else:
                    # check and deal with button interactions:
                    pressed = self.button_interactions(self.game_buttons)
                    if pressed is not None:
                        command = self.game_buttons[pressed]

                        # if pressed offer draw
                        if command == 'DO':
                            print("\t\t\there2")
                            # swap to draw cancel button
                            pressed.is_shown = False
                            get_key('DC', self.game_buttons).draw()

                        # if pressed draw cancel
                        elif command == 'DC':
                            print("\t\t\t here")
                            # swap to draw offer button
                            pressed.is_shown = False
                            get_key('DO', self.game_buttons).draw()

                        # add button to input queue
                        self.input_q.put(command)

                        # if aborted the game, return to menu screen
                        if command == 'A':
                            self.screen_number = 1
                            return
                        # if resigned the game, print loosing msg
                        elif command == 'R':
                            self.board.ended = "You lost by resignation"

                # if draw-related stuff happened:
                if self.board.draw is not None:
                    # if opponent requested a draw
                    if self.board.draw == 'R':
                        # swap draw button with accept button
                        get_key('DO', self.game_buttons).is_shown = False
                        get_key('DA', self.game_buttons).draw()
                    # if opponent declined the draw
                    elif self.board.draw == 'C':
                        # swap cancel button with draw button
                        get_key('DC', self.game_buttons).is_shown = False
                        get_key('DA', self.game_buttons).is_shown = False
                        get_key('DO', self.game_buttons).draw()
                    self.board.draw = None

                # update time
                if self.board.started:
                    # only if game started
                    if last_time is None:
                        # if first time after game started
                        # draw draw-offer button
                        get_key("DO", self.game_buttons).draw()
                        # change abort button to resign
                        get_key('A', self.game_buttons).is_shown = False
                        get_key('R', self.game_buttons).draw()

                        last_time = time.time()
                    time_passed = int((time.time() - last_time)*10)
                    if time_passed >= 0.1:

                        if self.board.turn == player.color:
                            if player.time_left >= time_passed:
                                player.time_left -= time_passed
                            else:
                                player.time_left = 0
                        else:
                            if opponent.time_left >= time_passed:
                                opponent.time_left -= time_passed
                            else:
                                opponent.time_left = 0

                        last_time = time.time()

                self.update_game_times(player, opponent)

            else:
                # draw cancel button if doesn't exist
                if cancel_button is None:
                    # print background image
                    self.screen.blit(back_img, (0, 0))

                    font = self.fonts[1]
                    text = font.render("waiting for opponent...", True, self.colors['titles'])

                    text_rect = text.get_rect()
                    text_rect.center = (500, 300)
                    self.screen.blit(text, text_rect)

                    cancel_button = get_key('C', self.loading_buttons)
                    cancel_button.draw()

                # if pressed the button
                if self.button_interactions([cancel_button]):
                    # exit the game loop
                    self.screen_number = 1
                    # send exit game waiting
                    self.input_q.put('EGW')
                    return

                pygame.display.update()

            pygame.display.update()

    def update_game_times(self, player, opponent):
        """
        update the remaining times of the player and the opopnent
        :param player: player (user) object
        :param opponent: opponent player object
        :return: None
        """
        # refresh time on screen
        self.screen.blit(time_img, (20, 855))
        self.screen.blit(time_img, (20, 5))

        # get time of player
        if player.time_left is not None:
            time_minutes = int(player.time_left / 600)
            time_seconds = int((player.time_left - time_minutes * 600) / 10)
            time_remain = int(player.time_left % 10)
        else:
            return

        # set font of time
        font = self.fonts[0]

        # render the time text
        # present the tenths of a second if there are less than 15 seconds remaining
        if time_seconds > 15 or time_minutes > 0:
            text = font.render(f"{time_minutes}:{time_seconds}", True, self.colors["time_text"])
        else:
            text = font.render(f"{time_minutes}:{time_seconds}:{time_remain}", True, self.colors["time_text"])
        # center the text to a wanted position
        text_rect = text.get_rect()
        text_rect.center = (70, 875)
        # blit text on screen
        self.screen.blit(text, text_rect)

        # get time of opponent
        time_minutes = int(opponent.time_left / 600)
        time_seconds = int((opponent.time_left - time_minutes * 600) / 10)
        time_remain = int(opponent.time_left % 10)

        # render the time text
        # present the tenths of a second if there are less than 15 seconds remaining
        if time_seconds > 15 or time_minutes > 0:
            text = font.render(f"{time_minutes}:{time_seconds}", True, self.colors["time_text"])
        else:
            text = font.render(f"{time_minutes}:{time_seconds}:{time_remain}", True, self.colors["time_text"])
        # center the text to a wanted position
        text_rect = text.get_rect()
        text_rect.center = (70, 25)
        # blit text on screen
        self.screen.blit(text, text_rect)

        # update pygame display
        pygame.display.update()

    def build_game_screen(self):
        """
        build the game screen
        :return: None
        """
        # print board
        self.print_game()

        for button in self.game_buttons:
            button.is_shown = False

        # draw abort button
        get_key('A', self.game_buttons).draw()

    def menu_loop(self):
        """
        main loop of game-selection menu
        :return: None
        """
        # build the menu
        self.build_menu()

        while True:

            # if a connection error occurred
            if self.start[0] == 'f':
                self.connection_error()
                return

            # handle_button_interactions
            pressed = self.button_interactions(self.menu_buttons)

            # if a button was pressed
            if pressed is not None:
                # get command of button
                command = self.menu_buttons[pressed]
                # if game-starting commands
                if command[0] == 'P':
                    # upload input
                    self.input_q.put(command)
                    # move to game-screen
                    self.screen_number = 2
                    # exit menu screen
                    return

            # deal with game-ending
            if self.end:
                return

    def build_menu(self):
        """
        builds the starting menu
        :return: None
        """
        # print background
        self.screen.blit(back_img, (0, 0))
        pygame.display.update()

        # set font for headline
        font = self.fonts[2]
        # headline
        text = font.render(f"CHESS", True, self.colors["titles"], None)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (500, 150)
        self.screen.blit(text, textRect)

        # change font
        font = self.fonts[1]

        # subtitle
        text = font.render(f"SELECT TIME", True, self.colors['titles'], None)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (500, 450)
        self.screen.blit(text, textRect)

        # draw all of the menu buttons
        for button in self.menu_buttons:
            button.draw()

        pygame.display.update()

    def build_buttons(self):
        """
        build all of the button objects for the game
        :return: None
        """
        # select font for text
        font = self.fonts[1]

        # build menu buttons
        game_times = [1, 2, 3, 5, 10, 15, 30]
        x = 80
        y = 550
        space_between = 220
        # start of command of button
        command_start = "P0"
        for game_time in game_times:
            text = font.render(f"{game_time} min", True, self.colors['button_text'])
            # move to second row after 4 buttons
            if game_time == 10:
                x = 190
                y = 650
                command_start = 'P'
            # build the button into the dictionary
            self.menu_buttons[Button(surface=self.screen, color=self.colors['button'], x=x, y=y, text=text,
                                     width=180, height=80)] = f"{command_start}{game_time}"
            # increase space between buttons
            x += space_between

        # build game-screen buttons
        # abort button
        text = font.render(f"abort", True, self.colors["button_text"])
        self.game_buttons[Button(surface=self.screen, color=self.colors["button"], x=830, y=360, text=text,
                                 width=150, height=80)] = "A"
        # resign button
        text = font.render(f"resign", True, self.colors["button_text"])
        self.game_buttons[Button(surface=self.screen, color=self.colors["button"], x=830, y=360, text=text,
                                 width=150, height=80)] = "R"
        # draw-offer button
        text = font.render(f"draw", True, self.colors["button_text"])
        self.game_buttons[Button(surface=self.screen, color=self.colors["button"], x=830, y=460, text=text,
                                 width=150, height=80)] = "DO"
        # draw-accept button
        text = font.render(f"accept", True, self.colors["button_text"])
        self.game_buttons[Button(surface=self.screen, color=self.colors["button"], x=830, y=460, text=text,
                                 width=150, height=80)] = "DA"
        # draw-cancel button
        text = font.render(f"cancel", True, self.colors["button_text"])
        self.game_buttons[Button(surface=self.screen, color=self.colors["button"], x=830, y=460, text=text,
                                 width=150, height=80)] = "DC"

        # build loading buttons
        # retry button for connection error
        text = font.render("retry", True, self.colors["button_text"])
        self.loading_buttons[Button(color=self.colors["button"], x=410, y=410, width=180, height=80,
                                    surface=self.screen, text=text)] = 'R'
        # cancel button for game-waiting
        text = font.render("cancel", True, self.colors["button_text"])
        self.loading_buttons[Button(color=self.colors["button"], x=410, y=410, width=180, height=80,
                                    surface=self.screen, text=text)] = 'C'

    def button_interactions(self, buttons_on_screen):
        """
        handle button interactions
        :param buttons_on_screen: list of buttons that are showing on the screen
        :return: button object if pressed a button, None if didn't
        """
        mouse_pos = pygame.mouse.get_pos()

        # button hovering
        for button in buttons_on_screen:
            if button.is_over(mouse_pos):
                # if didn't change colors
                if button.current_color == button.color:
                    button.draw(self.colors["button_hover"])
            # if stopped hovering over the button
            elif button.is_shown and button.current_color != button.color:
                button.draw()

        for event in pygame.event.get():
            # if stopped pressing the button
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                # check if pressed a button
                for button in buttons_on_screen:
                    if button.is_over(mouse_pos):
                        # draw unpressed color
                        button.draw(self.colors["button_hover"])
                        # so you can see the button animation
                        time.sleep(0.05)
                        # return the button that was pressed
                        return button

            # if started pressing the button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if above a button
                for button in buttons_on_screen:
                    if button.is_over(mouse_pos):
                        button.draw(self.colors["button_pressed"])

            elif event.type == pygame.QUIT:
                self.end = True
                return

    @staticmethod
    def set_images():
        """
        set up the images of the pieces
        :return: None
        """
        # pawn images
        Graphics.piece_images[('b', 'p')] = black_pawn_img
        Graphics.piece_images[('w', 'p')] = white_pawn_img
        # rook images
        Graphics.piece_images[('b', 'r')] = black_rook_img
        Graphics.piece_images[('w', 'r')] = white_rook_img
        # knight images
        Graphics.piece_images[('b', 'kn')] = black_knight_img
        Graphics.piece_images[('w', 'kn')] = white_knight_img
        # bishop images
        Graphics.piece_images[('b', 'b')] = black_bishop_img
        Graphics.piece_images[('w', 'b')] = white_bishop_img
        # queen images
        Graphics.piece_images[('b', 'q')] = black_queen_img
        Graphics.piece_images[('w', 'q')] = white_queen_img
        # king images
        Graphics.piece_images[('b', 'k')] = black_king_img
        Graphics.piece_images[('w', 'k')] = white_king_img

    @staticmethod
    def print_game():
        """
        print board onto the screen
        :return: None
        """
        board_orientation = Graphics.board.orientation
        pieces = Graphics.board.white.pieces + Graphics.board.black.pieces

        if board_orientation == 'w':
            Graphics.screen.blit(board_img, (20, 50))
            for i in range(len(pieces)):
                for j in range(len(pieces[i])):
                    if pieces[i][j].alive:
                        Graphics.screen.blit(Graphics.piece_images[(pieces[i][j].color, pieces[i][j].type)],
                                             ((835 - (8 - pieces[i][j].place[0]) * 100),
                                             (865 - (pieces[i][j].place[1] + 1) * 100)))

        else:
            # Surface onto this Surface.
            Graphics.screen.blit(board_img, (20, 50))
            for i in range(len(pieces)):
                for j in range(len(pieces[i])):
                    if pieces[i][j].alive:
                        Graphics.screen.blit(Graphics.piece_images[(pieces[i][j].color, pieces[i][j].type)],
                                             ((835 - (8 - pieces[i][j].place[0]) * 100),
                                             (865 - (pieces[i][j].place[1] + 1) * 100)))
        pygame.display.update()




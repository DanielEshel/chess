import pygame

photos_directory = 'photos/'

# Title and Icon
pygame.display.set_caption(f"Chess")
logo = pygame.image.load(f'{photos_directory}logo.png')
pygame.display.set_icon(logo)

# board and pieces
board_img = pygame.image.load(f"{photos_directory}board.jpg")

black_bishop_img = pygame.image.load(f"{photos_directory}black_bishop.png")
white_bishop_img = pygame.image.load(f"{photos_directory}white_bishop.png")

black_king_img = pygame.image.load(f"{photos_directory}black_king.png")
white_king_img = pygame.image.load(f"{photos_directory}white_king.png")

black_knight_img = pygame.image.load(f"{photos_directory}black_knight.png")
white_knight_img = pygame.image.load(f"{photos_directory}white_knight.png")

black_pawn_img = pygame.image.load(f"{photos_directory}black_pawn.png")
white_pawn_img = pygame.image.load(f"{photos_directory}white_pawn.png")

black_queen_img = pygame.image.load(f"{photos_directory}black_queen.png")
white_queen_img = pygame.image.load(f"{photos_directory}white_queen.png")

black_rook_img = pygame.image.load(f"{photos_directory}black_rook.png")
white_rook_img = pygame.image.load(f"{photos_directory}white_rook.png")

# stuff shown on board
chosen_square_img = pygame.image.load(f"{photos_directory}chosen_square.png")
chosen_square2_img = pygame.image.load(f"{photos_directory}chosen_square2.png")
white_square_img = pygame.image.load(f"{photos_directory}white_square.png")
green_square_img = pygame.image.load(f"{photos_directory}green_square.jpg")

# other
time_img = pygame.image.load(f"{photos_directory}time_square.png")
starting_img = pygame.image.load(f"{photos_directory}starting_screen.png")
back_img = pygame.image.load(f"{photos_directory}back.png")








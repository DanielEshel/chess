import pygame


class Button:

    def __init__(self, color, x, y, width, height, text, surface):
        """
        initialize the button
        :param color: color of button
        :param x: position in x axis
        :param y: position in y axis
        :param width: width of button
        :param height: height of button
        :param text: text on button (font.render object)
        :param surface: screen button is displayed on
        """
        self.color = color
        self.current_color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.surface = surface
        self.is_shown = False

    def draw(self, hover_color=None):
        """
        draw the button
        :param hover_color: different color
        :return: None
        """
        # draw shadow
        pygame.draw.rect(self.surface, (30, 32, 37), (self.x+4, self.y+6, self.width, self.height), 0, border_radius=15)

        if hover_color:
            # draw the button
            pygame.draw.rect(self.surface, hover_color, (self.x, self.y, self.width, self.height), 0, border_radius=15)
            self.current_color = hover_color
        else:
            # draw the button with the regular color
            pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0, border_radius=15)
            self.current_color = self.color

        text_rect = self.text.get_rect()
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)

        self.surface.blit(self.text, text_rect)
        pygame.display.update()
        self.is_shown = True

    def is_over(self, mouse_pos):
        """
        if mouse position is over the button, draw an outline
        :param mouse_pos: position of mouse on screen
        :param self: button object
        :return: None
        """
        if self.is_shown:
            if mouse_pos[0] in range(self.x, self.x + self.width):
                if mouse_pos[1] in range(self.y, self.y + self.height):
                    return True
        return False





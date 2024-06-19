import pygame


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font,
        text: str,
        onclick_f,
    ) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._onclick_f = onclick_f
        self._already_pressed = False

        self._button_surface = pygame.Surface((self._width, self._height))
        self._button_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._button_surf = font.render(text, True, pygame.Color("black"))

        self._fill_colors = {
            "normal": pygame.Color("lightgoldenrod"),
            "hover": pygame.Color("lightgoldenrod1"),
            "pressed": pygame.Color("lightgoldenrod2"),
        }

    def process(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self._button_surface.fill(self._fill_colors["normal"])
        if self._button_rect.collidepoint(mouse_pos):
            self._button_surface.fill(self._fill_colors["hover"])
            if pygame.mouse.get_pressed()[0]:
                self._button_surface.fill(self._fill_colors["pressed"])
                if not self._already_pressed:
                    self._onclick_f()
                    self._already_pressed = True
            else:
                self._already_pressed = False

        self._button_surface.blit(
            self._button_surf,
            [
                self._button_rect.width / 2 - self._button_surf.get_rect().width / 2,
                self._button_rect.height / 2 - self._button_surf.get_rect().height / 2,
            ],
        )

        screen.blit(self._button_surface, self._button_rect)

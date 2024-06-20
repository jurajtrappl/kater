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
    ) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text

        self._button_surface = pygame.Surface((self._width, self._height))
        self._button_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._button_surf = font.render(text, True, pygame.Color("black"))

    @property
    def rect(self) -> pygame.Rect:
        return self._button_rect

    @property
    def text(self) -> str:
        return self._text

    def draw(self, screen: pygame.Surface) -> None:
        self._button_surface.fill(pygame.Color("gray"))
        self._button_surface.blit(
            self._button_surf,
            [
                self._button_rect.width / 2 - self._button_surf.get_rect().width / 2,
                self._button_rect.height / 2 - self._button_surf.get_rect().height / 2,
            ],

        )

        screen.blit(self._button_surface, self._button_rect)

    def invoke(self, game_state) -> None:
        game_state["clicked_sidebar_button"] = self._text
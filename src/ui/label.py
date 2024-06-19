import pygame

from engine.player import Player


class PlayerAttributeLabel:
    def __init__(
        self,
        x: int,
        y: int,
        font: pygame.font.Font,
        property_name: str,
        text_color: pygame.color.Color,
        text_f,
    ) -> None:
        self._x = x
        self._y = y
        self._font = font
        self._property_name = property_name
        self._text_color = text_color
        self._text_f = text_f

    def update(self, player: Player) -> None:
        self._property_value = getattr(player, self._property_name)

    def draw(self, screen: pygame.Surface) -> None:
        image = self._font.render(
            self._text_f(self._property_value), True, self._text_color
        )
        screen.blit(image, (self._x, self._y))

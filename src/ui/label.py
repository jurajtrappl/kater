import pygame

from engine.player import Player


class PlayerAttributeLabel:
    def __init__(
        self,
        x: int,
        y: int,
        property_name: str,
        text_color: pygame.color.Color,
    ) -> None:
        self._x = x
        self._y = y
        self._property_name = property_name
        self._text_color = text_color

    def update(self, player: Player) -> None:
        self._property_value = getattr(player, self._property_name)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        label_text = f"{self._property_name.capitalize()}: {self._property_value}"
        image = font.render(label_text, True, self._text_color)
        screen.blit(image, (self._x, self._y))

import pygame


class Image:
    def __init__(
        self, x: int, y: int, width: int, height: int, resource: str, text: str
    ):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._resource = resource
        self._text = text

    def draw(self, screen: pygame.surface.Surface, font: pygame.font.Font) -> None:
        image_surface = pygame.image.load("resources/" + self._resource)
        image_surface = pygame.transform.scale(
            image_surface, (self._width, self._height)
        )
        screen.blit(image_surface, (self._x, self._y))

        image_text = font.render(
            self._text, True, pygame.Color("black")
        )
        screen.blit(image_text, (self._x + 25, self._y + self._height + 25))

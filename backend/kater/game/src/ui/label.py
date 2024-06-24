import pygame

class ExploreActionLabel:
    def __init__(
        self,
        x: int,
        y: int,
        text_color: pygame.color.Color
    ) -> None:
        self._x = x
        self._y = y
        self._text_color = text_color

    def update(self, game_state) -> None:
        if not game_state["explore"]:
            self._text_value = "You are not exploring now."
        else:
            current_ticks = pygame.time.get_ticks()
            remaining_ticks = game_state["explore"]["end"] - current_ticks
            remaining_time = remaining_ticks // 1000
            self._text_value = f"Remaining time: {remaining_time} seconds"

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        image = font.render(self._text_value, True, self._text_color)
        screen.blit(image, (self._x, self._y))

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

    def update(self, game_state) -> None:
        self._property_value = getattr(game_state["player"], self._property_name)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        label_text = f"{self._property_name.capitalize()}: {self._property_value}"
        image = font.render(label_text, True, self._text_color)
        screen.blit(image, (self._x, self._y))
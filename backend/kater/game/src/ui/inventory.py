from itertools import zip_longest
import pygame

class InventoryGrid:
    def __init__(self, size, font) -> None:
        self._size = size
        self._font = font

    def update(self, game_state) -> None:
        self._inventory_items = sorted(
            game_state["player"].inventory, key=lambda x: x[0].name
        )

    def draw(self, content_area: pygame.Surface, font: pygame.font.Font) -> None:
        content_area.fill(pygame.Color("white"))

        self._font = self._font or font

        # make square slots for items
        rows, cols = self._size // 6, 6
        slot_width, slot_height = 100, 100
        padding = 50
        start_x, start_y = 300, 100
        item_rects = []
        for i in range(rows):
            for j in range(cols):
                item_rects.append(
                    pygame.Rect(
                        start_x + j * (slot_width + padding),
                        start_y + i * (slot_height + padding),
                        slot_width,
                        slot_height,
                    )
                )

        # draw the grid
        for item_rect, inventory_item in zip_longest(item_rects, self._inventory_items):
            pygame.draw.rect(content_area, pygame.Color("black"), item_rect, width=1)

            if inventory_item is None:
                continue

            item, quantity = inventory_item
            item_image_surface = pygame.image.load("resources/" + item.resource_path)
            item_image_surface = pygame.transform.scale(
                item_image_surface, (item_rect.width, item_rect.height)
            )

            quantity_text = self._font.render(
                f"{quantity}x {item.name}", True, pygame.Color("black")
            )

            content_area.blit(item_image_surface, item_rect.topleft)
            content_area.blit(quantity_text, (item_rect.left, item_rect.bottom))

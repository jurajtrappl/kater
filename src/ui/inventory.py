import pygame

from engine.player import Player


class InventoryGrid:
    def __init__(self, size, font) -> None:
        self._size = size
        self._font = font

        self._inventory_slots = []
        rows, cols = self._size // 4, 4
        slot_width, slot_height = 80, 80
        padding = 20
        start_x, start_y = 300, 100
        for i in range(rows):
            for j in range(cols):
                item_rect = pygame.Rect(
                    start_x + j * (slot_width + padding),
                    start_y + i * (slot_height + padding),
                    slot_width,
                    slot_height,
                )

                self._inventory_slots.append((item_rect, None, None))

    def update(self, player: Player) -> None:
        for index, (item, quantity) in enumerate(
            sorted(player.inventory, key=lambda x: x[0].name)
        ):
            item_rect, _, _ = self._inventory_slots[index]

            item_image_surface = pygame.image.load("resources/" + item.resource_path)
            item_image_surface = pygame.transform.scale(
                item_image_surface, (item_rect.width, item_rect.height)
            )

            quantity_text = self._font.render(
                f"{quantity}x {item.name}", True, pygame.Color("black")
            )
            self._inventory_slots[index] = (
                item_rect,
                item_image_surface,
                quantity_text,
            )

    def draw(self, content_area: pygame.Surface) -> None:
        content_area.fill(pygame.Color("white"))

        for item_rect, item_image_surface, quantity_text in self._inventory_slots:
            pygame.draw.rect(content_area, pygame.Color("black"), item_rect, width=1)

            if item_image_surface is None:
                continue

            content_area.blit(item_image_surface, item_rect.topleft)
            content_area.blit(quantity_text, (item_rect.left, item_rect.bottom))

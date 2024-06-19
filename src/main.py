from pathlib import Path
import random
from typing import List
import toml
import pygame
import sys

from engine.player import Player
from engine.events import *
from ui.inventory import InventoryGrid
from ui.button import Button
from ui.label import PlayerAttributeLabel


def main() -> None:
    """
    Game entry function.
    """

    # Load configuration.
    global CONFIG
    with open("config.toml", "r", encoding="utf-8") as f:
        CONFIG = toml.load(f)

    # Run configurations.
    global SCREEN, FONTS
    SCREEN, FONTS = configure_pygame()
    configure_engine()

    # For now, we only support one player in the game.
    player = Player(Path("example_players/player1"))

    # Create UI objects.
    global CONTENT_AREA
    (
        objects,
        top_horizontal_line,
        sidebar_vertical_line,
        CONTENT_AREA,
    ) = init_ui_objects(player)

    global GAME_STATE
    GAME_STATE = {"clicked_sidebar_button": "Inventory"}

    running = True
    while running:
        """
        1. Handle events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.save("example_players/player1")
                sys.exit()
            elif event.type == REFILL_ENERGY:
                player.energy = min(
                    player.energy + CONFIG["rates"]["base_energy_refill"],
                    CONFIG["caps"]["energy"],
                )
            elif event.type == REFILL_HITPOINTS:
                player.hitpoints = min(
                    player.hitpoints + CONFIG["rates"]["base_hitpoints_refill"],
                    CONFIG["caps"]["hitpoints"],
                )
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clicked_button = [
                    obj
                    for obj in objects["buttons"]
                    if isinstance(obj, Button) and obj.rect.collidepoint(pos)
                ]
                if clicked_button:
                    GAME_STATE["clicked_sidebar_button"] = clicked_button[0].text

        """
        2. Update objects.
        """
        for label in objects["labels"]:
            label.update(player)

        for obj in objects[GAME_STATE["clicked_sidebar_button"]]:
            obj.update(player)

        """
        3. Clear the screen.
        """
        SCREEN.fill(pygame.Color("white"))

        """
        4. Draw objects.
        """
        # Separate top menu and side bar from content.
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (0, 50), (SCREEN.get_width(), 50)
        )
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (170, 50), (170, SCREEN.get_height())
        )

        # Draw objects on screen (top menu labels + sidebar buttons).
        for obj in objects["labels"]:
            obj.draw(SCREEN, FONTS["player_attribute_font"])

        for obj in objects["buttons"]:
            obj.draw(SCREEN)

        # Draw the content area.
        SCREEN.blit(
            CONTENT_AREA, (sidebar_vertical_line.right, top_horizontal_line.bottom)
        )

        # Draw objects in content area.
        for obj in objects[GAME_STATE["clicked_sidebar_button"]]:
            obj.draw(CONTENT_AREA)

        """
        5. Update screen.
        """
        pygame.display.flip()


def configure_pygame():
    """
    Runs methods that correctly set up PyGame "stuff".
    Returns important objects used during the game.
    """

    pygame.init()
    screen = pygame.display.set_mode(CONFIG["display"]["size"])
    pygame.display.set_caption(CONFIG["display"]["caption"])

    pygame.font.init()
    fonts = {
        "player_attribute_font": pygame.font.SysFont(
            None, CONFIG["fonts"]["player_attribute_font_size"]
        ),
        "sidebar_font": pygame.font.SysFont(None, CONFIG["fonts"]["sidebar_font_size"]),
        "content_font": pygame.font.SysFont(None, CONFIG["fonts"]["content_font_size"]),
        "inventory_font": pygame.font.SysFont(
            None, CONFIG["fonts"]["inventory_font_size"]
        ),
    }

    return screen, fonts


def configure_engine():
    """
    Runs some global configurations of the game process.
    """

    # Reproducibility.
    random.seed(CONFIG["globals"]["seed"])

    # Add custom events.
    pygame.time.set_timer(REFILL_ENERGY, CONFIG["rates"]["energy"])
    pygame.time.set_timer(REFILL_HITPOINTS, CONFIG["rates"]["hitpoints"])


def init_ui_objects(player) -> List[object]:
    # 1. Visual separation.
    top_horizontal_line = pygame.draw.line(
        SCREEN, pygame.Color("black"), (0, 50), (SCREEN.get_width(), 50)
    )
    sidebar_vertical_line = pygame.draw.line(
        SCREEN, pygame.Color("black"), (170, 50), (170, SCREEN.get_height())
    )

    # 2. Content area.
    content_area = pygame.Surface(
        (
            SCREEN.get_width() - sidebar_vertical_line.width,
            SCREEN.get_height() - top_horizontal_line.height,
        )
    )

    # 3. Main attributes labels
    objects = {}
    energy_label = PlayerAttributeLabel(
        200,
        15,
        "energy",
        pygame.Color("yellow3"),
    )
    hitpoints_label = PlayerAttributeLabel(
        400,
        15,
        "hitpoints",
        pygame.Color("red"),
    )
    balance_label = PlayerAttributeLabel(
        600,
        15,
        "balance",
        pygame.Color("palegreen3"),
    )
    level_label = PlayerAttributeLabel(
        800,
        15,
        "level",
        pygame.Color("black"),
    )
    objects["labels"] = [energy_label, hitpoints_label, balance_label, level_label]

    # 4. Menu buttons.
    inventory_button = Button(
        10,
        70,
        150,
        50,
        FONTS["sidebar_font"],
        "Inventory",
    )
    travel_button = Button(
        10,
        130,
        150,
        50,
        FONTS["sidebar_font"],
        "Travel",
    )
    skills_button = Button(
        10,
        190,
        150,
        50,
        FONTS["sidebar_font"],
        "Skills",
    )
    explore_button = Button(
        10,
        250,
        150,
        50,
        FONTS["sidebar_font"],
        "Explore",
    )
    export_button = Button(10, 610, 150, 50, FONTS["sidebar_font"], "Export")
    objects["buttons"] = [
        inventory_button,
        travel_button,
        skills_button,
        explore_button,
        export_button,
    ]

    objects["Inventory"] = [
        InventoryGrid(CONFIG["inventory"]["size"], FONTS["inventory_font"])
    ]

    return (
        objects,
        top_horizontal_line,
        sidebar_vertical_line,
        content_area,
    )


if __name__ == "__main__":
    main()

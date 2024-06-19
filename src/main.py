"""
Kater
-----

Entry point.

Authors: [Trappl, Juraj;]

"""

from pathlib import Path
import random
from typing import Dict, List
import toml
import pygame

from engine.player import Player
from engine.events import *
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
    objects, top_horizontal_line, sidebar_vertical_line, content_area = init_ui_objects(
        player
    )

    running = True
    while running:
        # Poll for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # TODO: character save
                pygame.time.wait(500)
                running = False
                pygame.quit()
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

        draw_ui(content_area, objects, sidebar_vertical_line, top_horizontal_line)


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
    objects = []

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
    content_area.fill(pygame.Color("white"))

    # 3. Main attributes labels
    energy_label = PlayerAttributeLabel(
        200,
        15,
        FONTS["player_attribute_font"],
        player,
        "energy",
        pygame.Color("yellow3"),
        lambda value: f"Energy: {value}",
    )
    hitpoints_label = PlayerAttributeLabel(
        400,
        15,
        FONTS["player_attribute_font"],
        player,
        "hitpoints",
        pygame.Color("red"),
        lambda value: f"Hitpoints: {value}",
    )
    balance_label = PlayerAttributeLabel(
        600,
        15,
        FONTS["player_attribute_font"],
        player,
        "balance",
        pygame.Color("palegreen3"),
        lambda value: f"Balance: {value} $",
    )
    level_label = PlayerAttributeLabel(
        800,
        15,
        FONTS["player_attribute_font"],
        player,
        "level",
        pygame.Color("black"),
        lambda value: f"Level: {value}",
    )
    objects.extend([energy_label, hitpoints_label, balance_label, level_label])

    # 4. Menu buttons.
    inventory_button = Button(
        10,
        70,
        150,
        50,
        FONTS["sidebar_font"],
        "Inventory",
        show_inventory(content_area),
    )
    travel_button = Button(
        10,
        130,
        150,
        50,
        FONTS["sidebar_font"],
        "Travel",
        show_travel(content_area),
    )
    skills_button = Button(
        10,
        190,
        150,
        50,
        FONTS["sidebar_font"],
        "Skills",
        show_skills(content_area),
    )
    explore_button = Button(
        10,
        250,
        150,
        50,
        FONTS["sidebar_font"],
        "Explore",
        show_explore(content_area),
    )

    export_button = Button(
        10, 610, 150, 50, FONTS["sidebar_font"], "Export", lambda: None
    )
    objects.extend(
        [inventory_button, travel_button, skills_button, explore_button, export_button]
    )

    return objects, top_horizontal_line, sidebar_vertical_line, content_area


def draw_ui(content_area, objects, sidebar_vertical_line, top_horizontal_line):
    # Clear the screen.
    SCREEN.fill(pygame.Color("white"))

    # Separate top menu and side bar from content.
    pygame.draw.line(SCREEN, pygame.Color("black"), (0, 50), (SCREEN.get_width(), 50))
    pygame.draw.line(
        SCREEN, pygame.Color("black"), (170, 50), (170, SCREEN.get_height())
    )

    # Draw the content area.
    SCREEN.blit(content_area, (sidebar_vertical_line.right, top_horizontal_line.bottom))

    # Update the labels to reflect current player's properties.
    for obj in objects:
        obj.process(SCREEN)

    pygame.display.flip()


def show_inventory(content_area):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))

        # Inventory specific stuff.
        inventory_text = FONTS["content_font"].render(
            "Inventory Content", True, pygame.Color("black")
        )
        content_area.blit(inventory_text, (20, 20))

    return callback


def show_travel(content_area):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))

        # Travel specific stuff.
        travel_text = FONTS["content_font"].render(
            "Travel Content", True, pygame.Color("black")
        )
        content_area.blit(travel_text, (20, 20))

    return callback


def show_skills(content_area):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))

        # Skills specific stuff.
        skills_text = FONTS["content_font"].render(
            "Skills Content", True, pygame.Color("black")
        )
        content_area.blit(skills_text, (20, 20))

    return callback


def show_explore(content_area):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))

        # Explore specific stuff.
        explore_text = FONTS["content_font"].render(
            "Explore Content", True, pygame.Color("black")
        )
        content_area.blit(explore_text, (20, 20))

    return callback


if __name__ == "__main__":
    main()

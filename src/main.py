from pathlib import Path
import random
from typing import List
import toml
import pygame
import sys

from engine.player import Player
from engine.events import *
from ui.inventory import InventoryGrid
from ui.button import Button, SidebarButton
from ui.label import ExploreActionLabel, PlayerAttributeLabel


def main() -> None:
    """
    Game entry function.
    """

    # Load configuration.
    global CONFIG
    with open("config.toml", "r", encoding="utf-8") as f:
        CONFIG = toml.load(f)

    # Run configurations.
    global SCREEN, CLOCK, FONTS
    SCREEN, CLOCK, FONTS = configure_pygame()

    global GAME_STATE
    GAME_STATE = configure_engine()

    # Create UI objects.
    top_menu_objects, sidebar_objects, content_area_objects = init_ui_objects()

    running = True
    while running:
        """
        1. Handle events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_STATE["player"].save("example_players/player1")
                sys.exit()
            elif event.type == REFILL_ENERGY:
                GAME_STATE["player"].energy = min(
                    GAME_STATE["player"].energy + CONFIG["rates"]["base_energy_refill"],
                    CONFIG["caps"]["energy"],
                )
            elif event.type == REFILL_HITPOINTS:
                GAME_STATE["player"].hitpoints = min(
                    GAME_STATE["player"].hitpoints
                    + CONFIG["rates"]["base_hitpoints_refill"],
                    CONFIG["caps"]["hitpoints"],
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Check whether any sidebar menu button was clicked.
                clicked_sidebar_button = [
                    obj for obj in sidebar_objects if obj.rect.collidepoint(pos)
                ]
                if clicked_sidebar_button:
                    clicked_sidebar_button[0].onclick(GAME_STATE)

                clicked_content_button = [
                    obj
                    for obj in content_area_objects["Explore"]
                    if isinstance(obj, Button) and obj.rect.collidepoint(pos)
                ]
                if clicked_content_button:
                    clicked_content_button[0].onclick(GAME_STATE)
            elif event.type == SHORT_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"]["short_experience"]
                # TODO: add level up handling
            elif event.type == MEDIUM_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"][
                    "medium_experience"
                ]
                # TODO: add level up handling
            elif event.type == LONG_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"]["long_experience"]
                # TODO: add level up handling

        """
        2. Update objects.
        """
        for label in top_menu_objects:
            label.update(GAME_STATE)

        for obj in content_area_objects[GAME_STATE["clicked_sidebar_button"]]:
            if not isinstance(obj, Button):
                obj.update(GAME_STATE)

        """
        3. Clear the screen.
        """
        SCREEN.fill(pygame.Color("white"))

        """
        4. Draw objects.
        """
        # Draw objects in content area.
        for obj in content_area_objects[GAME_STATE["clicked_sidebar_button"]]:
            obj.draw(SCREEN, FONTS["content_font"])

        # Draw objects on screen (top menu labels + sidebar buttons).
        for obj in top_menu_objects:
            obj.draw(SCREEN, FONTS["player_attribute_font"])

        for obj in sidebar_objects:
            obj.draw(SCREEN, FONTS["sidebar_font"])

        # Separate top menu and side bar from content.
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (0, 50), (SCREEN.get_width(), 50)
        )
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (170, 50), (170, SCREEN.get_height())
        )

        """
        5. Update screen.
        """
        pygame.display.flip()

        CLOCK.tick(60)


def configure_pygame():
    """
    Runs methods that correctly set up PyGame "stuff".
    Returns important objects used during the game.
    """

    pygame.init()
    screen = pygame.display.set_mode(CONFIG["display"]["size"])
    pygame.display.set_caption(CONFIG["display"]["caption"])

    clock = pygame.time.Clock()

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

    return screen, clock, fonts


def configure_engine():
    """
    Runs some global configurations of the game process.
    """

    # Reproducibility.
    random.seed(CONFIG["globals"]["seed"])

    # Add custom events.
    pygame.time.set_timer(REFILL_ENERGY, CONFIG["rates"]["energy"])
    pygame.time.set_timer(REFILL_HITPOINTS, CONFIG["rates"]["hitpoints"])

    # For now, we only support one player in the game.
    player = Player(Path("example_players/player1"))
    game_state = {
        "clicked_sidebar_button": "Inventory",  # remembers what sidebar button was clicked, default is the Inventory
        "explore": None,  # remembers the time (in ticks) when an explore action was clicked (if there is one)
        "player": player,  # remembers the player
    }

    return game_state


def init_ui_objects() -> List[object]:
    # 1. Top menu labels
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
    experience_label = PlayerAttributeLabel(
        1000, 15, "experience", pygame.Color("purple")
    )
    top_menu_objects = [
        energy_label,
        hitpoints_label,
        balance_label,
        level_label,
        experience_label,
    ]

    # 2. Sidebar buttons.
    inventory_button = SidebarButton(10, 70, 150, 50, "Inventory")
    travel_button = SidebarButton(10, 130, 150, 50, "Travel")
    skills_button = SidebarButton(10, 190, 150, 50, "Skills")
    explore_button = SidebarButton(
        10,
        250,
        150,
        50,
        "Explore",
    )
    export_button = SidebarButton(10, 610, 150, 50, "Export")
    sidebar_objects = [
        inventory_button,
        travel_button,
        skills_button,
        explore_button,
        export_button,
    ]

    content_area_objects = {}
    content_area_objects["Inventory"] = [
        InventoryGrid(CONFIG["inventory"]["size"], FONTS["inventory_font"])
    ]
    content_area_objects["Explore"] = [
        Button(
            350,
            250,
            250,
            50,
            f'Short ({CONFIG["explore"]["short_duration"] // 1000}s, {CONFIG["explore"]["short_energy"]}e)',
            short_explore_onclick,
        ),
        Button(
            350,
            350,
            250,
            50,
            f'Medium ({CONFIG["explore"]["medium_duration"] // 1000}s, {CONFIG["explore"]["medium_energy"]}e)',
            medium_explore_onclick,
        ),
        Button(
            350,
            450,
            250,
            50,
            f'Long ({CONFIG["explore"]["long_duration"] // 1000}s, {CONFIG["explore"]["long_energy"]}e)',
            long_explore_onclick,
        ),
        ExploreActionLabel(750, 370, pygame.Color("black")),
    ]

    return top_menu_objects, sidebar_objects, content_area_objects


def short_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    game_state["player"].energy -= CONFIG["explore"]["short_energy"]
    game_state["explore"] = (
        pygame.time.get_ticks() + CONFIG["explore"]["short_duration"]
    )
    pygame.time.set_timer(SHORT_EXPLORE, CONFIG["explore"]["short_duration"], loops=1)


def medium_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    game_state["player"].energy -= CONFIG["explore"]["medium_energy"]
    game_state["explore"] = (
        pygame.time.get_ticks() + CONFIG["explore"]["medium_duration"]
    )
    pygame.time.set_timer(MEDIUM_EXPLORE, CONFIG["explore"]["medium_duration"], loops=1)


def long_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    game_state["player"].energy -= CONFIG["explore"]["long_energy"]
    game_state["explore"] = pygame.time.get_ticks() + CONFIG["explore"]["long_duration"]
    pygame.time.set_timer(LONG_EXPLORE, CONFIG["explore"]["long_duration"], loops=1)


if __name__ == "__main__":
    main()

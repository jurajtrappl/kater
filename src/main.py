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
    with open("config.toml", "r", encoding="utf-8") as f:
        config = toml.load(f)

    # For now, we only support one player in the game.
    player = Player(Path("example_players/player1"))

    # Run configurations.
    screen, player_attribute_font, sidebar_font, content_font = configure_pygame(config)
    configure_engine(config)

    # Create UI objects.
    objects, top_horizontal_line, sidebar_vertical_line, content_area = init_ui_objects(
        screen, player_attribute_font, sidebar_font, content_font, player
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
                    player.energy + config["rates"]["base_energy_refill"],
                    config["caps"]["energy"],
                )
            elif event.type == REFILL_HITPOINTS:
                player.hitpoints = min(
                    player.hitpoints + config["rates"]["base_hitpoints_refill"],
                    config["caps"]["hitpoints"],
                )

        draw_ui(
            screen, content_area, objects, sidebar_vertical_line, top_horizontal_line
        )


def configure_pygame(global_config: Dict[str, object]):
    """
    Runs methods that correctly set up PyGame "stuff".
    Returns important objects used during the game.
    """
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(global_config["display"]["size"])

    pygame.display.set_caption(global_config["display"]["caption"])

    player_attribute_font = pygame.font.SysFont(
        None, global_config["fonts"]["player_attribute_font_size"]
    )
    sidebar_font = pygame.font.SysFont(
        None, global_config["fonts"]["sidebar_font_size"]
    )
    content_font = pygame.font.SysFont(
        None, global_config["fonts"]["content_font_size"]
    )

    pygame.time.set_timer(REFILL_ENERGY, global_config["rates"]["energy"])
    pygame.time.set_timer(REFILL_HITPOINTS, global_config["rates"]["hitpoints"])

    return screen, player_attribute_font, sidebar_font, content_font


def configure_engine(global_config: Dict[str, object]):
    """
    Runs some global configurations of the game process.
    """

    # for reproducibility when we will use something random
    random.seed(global_config["globals"]["seed"])


def init_ui_objects(
    screen, player_attribute_font, sidebar_font, content_font, player
) -> List[object]:
    objects = []

    # 1. Visual separation.
    top_horizontal_line = pygame.draw.line(
        screen, pygame.Color("black"), (0, 50), (screen.get_width(), 50)
    )
    sidebar_vertical_line = pygame.draw.line(
        screen, pygame.Color("black"), (170, 50), (170, screen.get_height())
    )

    # 2. Content area.
    content_area = pygame.Surface(
        (
            screen.get_width() - sidebar_vertical_line.width,
            screen.get_height() - top_horizontal_line.height,
        )
    )
    content_area.fill(pygame.Color("white"))

    # 3. Main attributes labels
    energy_label = PlayerAttributeLabel(
        200,
        15,
        player_attribute_font,
        player,
        "energy",
        pygame.Color("yellow3"),
        lambda value: f"Energy: {value}",
    )
    hitpoints_label = PlayerAttributeLabel(
        400,
        15,
        player_attribute_font,
        player,
        "hitpoints",
        pygame.Color("red"),
        lambda value: f"Hitpoints: {value}",
    )
    balance_label = PlayerAttributeLabel(
        600,
        15,
        player_attribute_font,
        player,
        "balance",
        pygame.Color("palegreen3"),
        lambda value: f"Balance: {value} $",
    )
    level_label = PlayerAttributeLabel(
        800,
        15,
        player_attribute_font,
        player,
        "level",
        pygame.Color("black"),
        lambda value: f"Level: {value}",
    )
    objects.extend([energy_label, hitpoints_label, balance_label, level_label])

    # 4. Menu buttons.
    inventory_button = Button(10, 70, 150, 50, sidebar_font, "Inventory", show_inventory(content_area, content_font))
    travel_button = Button(10, 130, 150, 50, sidebar_font, "Travel", show_travel(content_area, content_font))
    skills_button = Button(10, 190, 150, 50, sidebar_font, "Skills", show_skills(content_area, content_font))
    explore_button = Button(10, 250, 150, 50, sidebar_font, "Explore", show_explore(content_area, content_font))

    export_button = Button(10, 610, 150, 50, sidebar_font, "Export", lambda: None)
    objects.extend(
        [inventory_button, travel_button, skills_button, explore_button, export_button]
    )

    return objects, top_horizontal_line, sidebar_vertical_line, content_area


def draw_ui(screen, content_area, objects, sidebar_vertical_line, top_horizontal_line):
    # Clear the screen.
    screen.fill(pygame.Color("white"))

    # Separate top menu and side bar from content.
    pygame.draw.line(screen, pygame.Color("black"), (0, 50), (screen.get_width(), 50))
    pygame.draw.line(
        screen, pygame.Color("black"), (170, 50), (170, screen.get_height())
    )

    # Draw the content area.
    screen.blit(content_area, (sidebar_vertical_line.right, top_horizontal_line.bottom))

    # Update the labels to reflect current player's properties.
    for obj in objects:
        obj.process(screen)

    pygame.display.flip()

def show_inventory(content_area, content_font):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))
        
        # Inventory specific stuff.
        inventory_text = content_font.render("Inventory Content", True, pygame.Color("black"))
        content_area.blit(inventory_text, (20, 20))

    return callback

def show_travel(content_area, content_font):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))
        
        # Travel specific stuff.
        travel_text = content_font.render("Travel Content", True, pygame.Color("black"))
        content_area.blit(travel_text, (20, 20))

    return callback

def show_skills(content_area, content_font):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))
        
        # Skills specific stuff.
        skills_text = content_font.render("Skills Content", True, pygame.Color("black"))
        content_area.blit(skills_text, (20, 20))

    return callback

def show_explore(content_area, content_font):
    def callback():
        # Clear content from any previous work.
        content_area.fill(pygame.Color("white"))
        
        # Explore specific stuff.
        explore_text = content_font.render("Explore Content", True, pygame.Color("black"))
        content_area.blit(explore_text, (20, 20))

    return callback

if __name__ == "__main__":
    main()

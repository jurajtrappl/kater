"""
Kater
-----

Entry point.

Authors: [Trappl, Juraj;]

"""

import argparse
from pathlib import Path
import random
from typing import Dict, List
import toml
import pygame

from engine.player import Player
from engine.events import *
from ui.button import Button
from ui.label import PlayerAttributeLabel

parser = argparse.ArgumentParser()
parser.add_argument(
    "--character_save", type=str, help="Path to character save to play."
)


def main(cmd_args: argparse.Namespace) -> None:
    """
    Game entry function.
    """

    # Load configuration.
    with open("config.toml", "r", encoding="utf-8") as f:
        config = toml.load(f)

    # For now, we only support one player in the game.
    character_save_path = Path(cmd_args.character_save)
    player = Player(character_save_path)

    # Run configurations.
    screen, _, font = configure_pygame(config)
    configure_engine(config)

    # Create UI objects.
    objects = init_ui_objects(font, player)
    
    running = True
    while running:
        screen.fill(pygame.Color("white"))

        # Poll for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # TODO: character save
                pygame.time.wait(500)
                pygame.quit()
                running = False
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

        for obj in objects:
            obj.process(screen)

        # Visual separation.
        pygame.draw.line(
            screen, pygame.Color("black"), (0, 50), (screen.get_width(), 50), 1
        )
        pygame.draw.line(
            screen, pygame.Color("black"), (100, 50), (100, screen.get_height()), 1
        )

        pygame.display.flip()


def configure_pygame(global_config: Dict[str, object]):
    """
    Runs methods that correctly set up PyGame "stuff".
    Returns important objects used during the game.
    """
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(global_config["display"]["size"])
    pygame.display.set_caption(global_config["display"]["caption"])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(
        None, global_config["fonts"]["player_attribute_font_size"]
    )

    pygame.time.set_timer(REFILL_ENERGY, global_config["rates"]["energy"])
    pygame.time.set_timer(REFILL_HITPOINTS, global_config["rates"]["hitpoints"])

    return screen, clock, font


def configure_engine(global_config: Dict[str, object]):
    """
    Runs some global configurations of the game process.
    """

    # for reproducibility when we will use something random
    random.seed(global_config["globals"]["seed"])

def init_ui_objects(font, player) -> List[object]:
    objects = []
    
    # Main attributes labels
    energy_label = PlayerAttributeLabel(
        100, 15, font, player, "energy", pygame.Color("yellow3"), lambda value: f"Energy: {value}"
    )
    hitpoints_label = PlayerAttributeLabel(
        350, 15, font, player, "hitpoints", pygame.Color("red"), lambda value: f"Hitpoints: {value}"
    )
    balance_label = PlayerAttributeLabel(
        600, 15, font, player, "balance", pygame.Color("palegreen3"), lambda value: f"Balance: {value} $"
    )
    level_label = PlayerAttributeLabel(
        850, 15, font, player, "level", pygame.Color("black"), lambda value: f"Level: {value}"
    )
    objects.extend([energy_label, hitpoints_label, balance_label, level_label])

    # TODO: Menu buttons.

    return objects

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    main(args)

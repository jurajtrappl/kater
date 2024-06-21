from pathlib import Path
import random
from typing import List
import toml
import pygame
import sys

from engine.item import Item
from engine.player import Player
from engine.events import *
from ui.image import Image
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
                    for obj in content_area_objects[
                        GAME_STATE["clicked_sidebar_button"]
                    ]
                    if isinstance(obj, Button) and obj.rect.collidepoint(pos)
                ]
                if clicked_content_button:
                    clicked_content_button[0].onclick(GAME_STATE)
            elif event.type == SHORT_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"]["experience"][
                    "short"
                ]
                # TODO: add level up handling
            elif event.type == MEDIUM_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"]["experience"][
                    "medium"
                ]
                # TODO: add level up handling
            elif event.type == LONG_EXPLORE:
                GAME_STATE["explore"] = None
                GAME_STATE["player"].experience += CONFIG["explore"]["experience"][
                    "long"
                ]
                # TODO: add level up handling
            elif event.type == COPPER_ORE_MINED:
                GAME_STATE["mining"] = None
                GAME_STATE["player"].experience += CONFIG["skills"]["mining"][
                    "experience"
                ]["copper_ore"]
                quantity = 1
                GAME_STATE["player"].inventory.add(
                    Item("Copper ore", "copper_ore.png"), quantity
                )

                # show new amount as sort of a notification
                GAME_STATE["blink_inventory_update_text"] = (FONTS["sidebar_font"].render(f"+{quantity}", True, pygame.Color("black")), 375, 310)
                pygame.time.set_timer(BLINK_INVENTORY_UPDATE_TEXT, 1000, loops=1)
            elif event.type == SILVER_ORE_MINED:
                GAME_STATE["mining"] = None
                GAME_STATE["player"].experience += CONFIG["skills"]["mining"][
                    "experience"
                ]["silver_ore"]
                quantity = 1
                GAME_STATE["player"].inventory.add(
                    Item("Silver ore", "silver_ore.png"), quantity
                )

                GAME_STATE["blink_inventory_update_text"] = (FONTS["sidebar_font"].render(f"+{quantity}", True, pygame.Color("black")), 375, 360)
                pygame.time.set_timer(BLINK_INVENTORY_UPDATE_TEXT, 1000, loops=1)
            elif event.type == BLINK_INVENTORY_UPDATE_TEXT:
                GAME_STATE["blink_inventory_update_text"] = None

        """
        2. Update objects.
        """
        for label in top_menu_objects:
            label.update(GAME_STATE)

        for obj in content_area_objects[GAME_STATE["clicked_sidebar_button"]]:
            if not isinstance(obj, Button) and not isinstance(obj, Image):
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
            obj.draw(SCREEN, FONTS[f'{GAME_STATE["clicked_sidebar_button"].lower()}_font'])

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

        if GAME_STATE["blink_inventory_update_text"] is not None:
            text, x, y = GAME_STATE["blink_inventory_update_text"]
            SCREEN.blit(text, (x, y))

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
        "skills_font": pygame.font.SysFont(None, CONFIG["fonts"]["skills_font_size"]),
        "explore_font": pygame.font.SysFont(None, CONFIG["fonts"]["explore_font_size"]),
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
        "explore": None,  # remembers the end time of clicked explore action (if there is one)
        "player": player,  # remembers the player,
        "mining": None,  # remembers the end time of clicked mining action (if there is one)
        "blink_inventory_update_text": None # shows a small amount of new items that were added to inventory shortly after the action was finished
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

    content_area_objects["Skills"] = [
        Image(250, 125, 100, 100, "mining_icon.png", "Mining"),
        Button(
            250,
            300,
            120,
            35,
            f'Copper ore ({CONFIG["skills"]["mining"]["energy"]["copper_ore"]}e, {CONFIG["skills"]["mining"]["duration"]["copper_ore"] // 1000}s)',
            mine_copper_ore_onclick,
        ),
        Button(
            250,
            350,
            120,
            35,
            f'Silver ore ({CONFIG["skills"]["mining"]["energy"]["silver_ore"]}e, {CONFIG["skills"]["mining"]["duration"]["silver_ore"] // 1000}s)',
            mine_silver_ore_onclick,
        ),
        Image(450, 125, 100, 100, "woodcutting_icon.png", "Woodcutting"),
        Button(
            450,
            300,
            100,
            35,
            f'Oak log ({CONFIG["skills"]["woodcutting"]["energy"]["oak_log"]}e, {CONFIG["skills"]["woodcutting"]["duration"]["oak_log"] // 1000}s)',
            chop_oak_log_onclick,
        ),
        Image(650, 125, 100, 100, "fishing_icon.png", "Fishing"),
        Button(
            650,
            300,
            100,
            35,
            f'Carp ({CONFIG["skills"]["fishing"]["energy"]["carp"]}e, {CONFIG["skills"]["fishing"]["duration"]["carp"] // 1000}s)',
            catch_carp_onclick,
        ),
        Image(850, 125, 100, 100, "herbalism_icon.png", "Herbalism"),
        Button(
            850,
            300,
            100,
            35,
            f'Mugwort ({CONFIG["skills"]["herbalism"]["energy"]["mugwort"]}e, {CONFIG["skills"]["herbalism"]["duration"]["mugwort"] // 1000}s)',
            pick_mugwort_onclick,
        ),
        Image(1050, 125, 100, 100, "divination_icon.png", "Divination"),
        Button(
            1050,
            300,
            100,
            35,
            f'Quartz ({CONFIG["skills"]["divination"]["energy"]["quartz"]}e, {CONFIG["skills"]["divination"]["duration"]["quartz"] // 1000}s)',
            gather_quartz_onclick,
        ),
    ]

    content_area_objects["Explore"] = [
        Button(
            350,
            250,
            250,
            50,
            f'Short ({CONFIG["explore"]["duration"]["short"] // 1000}s, {CONFIG["explore"]["energy"]["short"]}e)',
            short_explore_onclick,
        ),
        Button(
            350,
            350,
            250,
            50,
            f'Medium ({CONFIG["explore"]["duration"]["medium"] // 1000}s, {CONFIG["explore"]["energy"]["medium"]}e)',
            medium_explore_onclick,
        ),
        Button(
            350,
            450,
            250,
            50,
            f'Long ({CONFIG["explore"]["duration"]["long"] // 1000}s, {CONFIG["explore"]["energy"]["long"]}e)',
            long_explore_onclick,
        ),
        ExploreActionLabel(750, 370, pygame.Color("black")),
    ]

    return top_menu_objects, sidebar_objects, content_area_objects


def short_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    if game_state["player"].energy < CONFIG["explore"]["energy"]["short"]:
        return

    game_state["player"].energy -= CONFIG["explore"]["energy"]["short"]
    game_state["explore"] = (
        pygame.time.get_ticks() + CONFIG["explore"]["duration"]["short"]
    )
    pygame.time.set_timer(
        SHORT_EXPLORE, CONFIG["explore"]["duration"]["short"], loops=1
    )


def medium_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    if game_state["player"].energy < CONFIG["explore"]["energy"]["medium"]:
        return

    game_state["player"].energy -= CONFIG["explore"]["energy"]["medium"]
    game_state["explore"] = (
        pygame.time.get_ticks() + CONFIG["explore"]["duration"]["medium"]
    )
    pygame.time.set_timer(
        MEDIUM_EXPLORE, CONFIG["explore"]["duration"]["medium"], loops=1
    )


def long_explore_onclick(game_state):
    if game_state["explore"] is not None:
        return

    if game_state["player"].energy < CONFIG["explore"]["energy"]["long"]:
        return

    game_state["player"].energy -= CONFIG["explore"]["energy"]["long"]
    game_state["explore"] = (
        pygame.time.get_ticks() + CONFIG["explore"]["duration"]["long"]
    )
    pygame.time.set_timer(LONG_EXPLORE, CONFIG["explore"]["duration"]["long"], loops=1)


def mine_copper_ore_onclick(game_state):
    if game_state["mining"] is not None:
        return

    if game_state["player"].energy < CONFIG["skills"]["mining"]["energy"]["copper_ore"]:
        return

    game_state["player"].energy -= CONFIG["skills"]["mining"]["energy"]["copper_ore"]
    game_state["mining"] = (
        pygame.time.get_ticks() + CONFIG["skills"]["mining"]["duration"]["copper_ore"]
    )
    pygame.time.set_timer(
        COPPER_ORE_MINED, CONFIG["skills"]["mining"]["duration"]["copper_ore"], loops=1
    )

def mine_copper_ore_onclick(game_state):
    if game_state["mining"] is not None:
        return

    if game_state["player"].energy < CONFIG["skills"]["mining"]["energy"]["copper_ore"]:
        return

    game_state["player"].energy -= CONFIG["skills"]["mining"]["energy"]["copper_ore"]
    game_state["mining"] = (
        pygame.time.get_ticks() + CONFIG["skills"]["mining"]["duration"]["copper_ore"]
    )
    pygame.time.set_timer(
        COPPER_ORE_MINED, CONFIG["skills"]["mining"]["duration"]["copper_ore"], loops=1
    )

def mine_silver_ore_onclick(game_state):
    if game_state["mining"] is not None:
        return

    if game_state["player"].energy < CONFIG["skills"]["mining"]["energy"]["silver_ore"]:
        return

    game_state["player"].energy -= CONFIG["skills"]["mining"]["energy"]["silver_ore"]
    game_state["mining"] = (
        pygame.time.get_ticks() + CONFIG["skills"]["mining"]["duration"]["silver_ore"]
    )
    pygame.time.set_timer(
        SILVER_ORE_MINED, CONFIG["skills"]["mining"]["duration"]["silver_ore"], loops=1
    )

def chop_oak_log_onclick(game_state):
    pass

def catch_carp_onclick(game_state):
    pass

def pick_mugwort_onclick(game_state):
    pass

def gather_quartz_onclick(game_state):
    pass

if __name__ == "__main__":
    main()

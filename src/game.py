import asyncio

from pathlib import Path
import random
from typing import List
import pygame
import sys

from .engine import *
from .ui import *


async def main() -> None:
    """
    Game entry function.
    """

    # Load configuration.
    global CONFIG
    CONFIG = Config()

    # Run configurations.
    global SCREEN, CLOCK, FONTS
    SCREEN, CLOCK, FONTS = configure_pygame()

    global GAME_STATE
    GAME_STATE = configure_engine()

    # Create UI objects.
    top_menu, sidebar, content_area = init_ui_objects()

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
                    GAME_STATE["player"].energy + CONFIG.rates.base_energy_refill,
                    CONFIG.caps.energy,
                )
            elif event.type == REFILL_HITPOINTS:
                GAME_STATE["player"].hitpoints = min(
                    GAME_STATE["player"].hitpoints
                    + CONFIG.rates.base_hitpoints_refill,
                    CONFIG.caps.hitpoints,
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Check whether any sidebar menu button was clicked.
                clicked_sidebar_button = [
                    obj for obj in sidebar if obj.rect.collidepoint(pos)
                ]
                if clicked_sidebar_button:
                    clicked_sidebar_button[0].onclick()

                clicked_content_button = [
                    obj
                    for obj in content_area[GAME_STATE["clicked_sidebar_button"]]
                    if isinstance(obj, Button) and obj.rect.collidepoint(pos)
                ]
                if clicked_content_button:
                    clicked_content_button[0].onclick()
            elif event.type == EXPLORE_FINISHED:
                GAME_STATE["player"].experience += CONFIG.explore.experience[
                    GAME_STATE["explore"]["item"]
                ]
                GAME_STATE["explore"] = {}
            elif event.type in [
                ORE_MINED,
                LOG_CHOPPED,
                FISH_CAUGHT,
                HERB_PICKED,
                CRYSTAL_GATHERED,
            ]:
                event_i = [
                    ORE_MINED,
                    LOG_CHOPPED,
                    FISH_CAUGHT,
                    HERB_PICKED,
                    CRYSTAL_GATHERED,
                ].index(event.type)
                skill = CONFIG.skills[event_i]

                item_number = GAME_STATE["skill_action"][skill]["item"]
                item_name = getattr(CONFIG, skill).items[item_number]
                item_resource = "_".join(map(str.lower, item_name.split())) + ".png"
                quantity = 1

                GAME_STATE["player"].experience += getattr(CONFIG, skill).experience[
                    item_number
                ]
                GAME_STATE["player"].inventory.add(
                    Item(item_name, item_resource), quantity
                )

                # +1 notification
                GAME_STATE["blink_inventory_update_text"] = (
                    FONTS["sidebar_font"].render(
                        f"+{quantity}", True, pygame.Color("black")
                    ),
                    GAME_STATE["skill_action"][skill]["button_x"] + 125,
                    GAME_STATE["skill_action"][skill]["button_y"] + 10,
                )
                pygame.time.set_timer(BLINK_INVENTORY_UPDATE_TEXT, 1000, loops=1)

                GAME_STATE["skill_action"][skill] = {}
            elif event.type == BLINK_INVENTORY_UPDATE_TEXT:
                GAME_STATE["blink_inventory_update_text"] = None

        """
        2. Update objects.
        """
        for label in top_menu:
            label.update(GAME_STATE)

        for obj in content_area[GAME_STATE["clicked_sidebar_button"]]:
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
        for obj in content_area[GAME_STATE["clicked_sidebar_button"]]:
            obj.draw(
                SCREEN, FONTS[f'{GAME_STATE["clicked_sidebar_button"].lower()}_font']
            )

        # Draw objects on screen (top menu labels + sidebar buttons).
        for obj in top_menu:
            obj.draw(SCREEN, FONTS["player_attribute_font"])

        for obj in sidebar:
            obj.draw(SCREEN, FONTS["sidebar_font"])

        # Separate top menu and side bar from content.
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (0, 50), (SCREEN.get_width(), 50)
        )
        pygame.draw.line(
            SCREEN, pygame.Color("black"), (170, 50), (170, SCREEN.get_height())
        )

        # +quantity notifications
        if (
            GAME_STATE["blink_inventory_update_text"] is not None
            and GAME_STATE["clicked_sidebar_button"] == "Skills"
        ):
            text, x, y = GAME_STATE["blink_inventory_update_text"]
            SCREEN.blit(text, (x, y))

        """
        5. Update screen.
        """
        pygame.display.flip()

        CLOCK.tick(60)
        await asyncio.sleep(0)


def configure_pygame():
    """
    Runs methods that correctly set up PyGame "stuff".
    Returns important objects used during the game.
    """

    pygame.init()
    screen = pygame.display.set_mode(CONFIG.display.size)
    pygame.display.set_caption(CONFIG.display.caption)

    clock = pygame.time.Clock()

    fonts = init_fonts()

    return screen, clock, fonts


def configure_engine():
    """
    Runs some global configurations of the game process.
    """

    # Reproducibility.
    random.seed(CONFIG.globals.seed)

    # Add custom events.
    pygame.time.set_timer(REFILL_ENERGY, CONFIG.rates.energy)
    pygame.time.set_timer(REFILL_HITPOINTS, CONFIG.rates.hitpoints)

    # For now, we only support one player in the game.
    player = Player(Path("example_players/player1"))
    game_state = {
        "clicked_sidebar_button": "Inventory",  # remembers what sidebar button was clicked, default is the Inventory
        "explore": {},  # remembers the end time of clicked explore action (if there is one)
        "player": player,  # remembers the player,
        "skill_action": {skill: {} for skill in CONFIG.skills},
        "blink_inventory_update_text": None,  # shows a small amount of new items that were added to inventory shortly after the action was finished
    }

    return game_state


def init_ui_objects() -> List[object]:
    top_menu = [
        PlayerAttributeLabel(200 + i * 225, 15, attribute, pygame.Color(color))
        for i, (attribute, color) in enumerate(
            zip(
                ["hitpoints", "balance", "energy", "level"],
                ["red", "palegreen3", "yellow3", "black"],
            )
        )
    ]

    sidebar = [
        SidebarButton(GAME_STATE, 10, 70 + i * 60, 150, 50, name)
        for i, name in enumerate(CONFIG.sidebar)
    ]

    content_area = {}
    content_area["Inventory"] = [
        InventoryGrid(CONFIG.inventory.size, FONTS["inventory_font"])
    ]

    content_area["Skills"] = [
        Image(250 + i * 200, 125, 100, 100, f"{skill}_icon.png", skill.capitalize())
        for i, skill in enumerate(CONFIG.skills)
    ]
    content_area["Skills"].extend(
        [
            Button(
                250 + col * 200,
                300 + row * 50,
                120,
                35,
                f'{item} ({getattr(CONFIG, skill).energy[row]}e, {getattr(CONFIG, skill).duration[row] // 1000}s)',
                on_skill_action(skill, event, row, 250 + col * 200, 300 + row * 50),
            )
            for col, (skill, event) in enumerate(
                zip(
                    CONFIG.skills,
                    [
                        ORE_MINED,
                        LOG_CHOPPED,
                        FISH_CAUGHT,
                        HERB_PICKED,
                        CRYSTAL_GATHERED,
                    ],
                )
            )
            for row, item in enumerate(getattr(CONFIG, skill).items)
        ]
    )

    content_area["Explore"] = [ExploreActionLabel(750, 370, pygame.Color("black"))]
    content_area["Explore"].extend(
        [
            Button(
                350,
                250 + i * 100,
                250,
                50,
                f'{explore_type.capitalize()} ({CONFIG.explore.duration[i] // 1000}s, {CONFIG.explore.energy[i]}e)',
                on_explore(i),
            )
            for i, explore_type in enumerate(CONFIG.explore.items)
        ]
    )

    return top_menu, sidebar, content_area


def on_explore(item):
    def callback():
        if (
            GAME_STATE["explore"]
            or GAME_STATE["player"].energy < CONFIG.explore.energy[item]
        ):
            return

        GAME_STATE["explore"] = {
            "end": pygame.time.get_ticks() + CONFIG.explore.duration[item],
            "item": item,
        }
        GAME_STATE["player"].energy -= CONFIG.explore.energy[item]
        pygame.time.set_timer(
            EXPLORE_FINISHED, CONFIG.explore.duration[item], loops=1
        )

    return callback


def on_skill_action(skill, event, item, button_x, button_y):
    def callback():
        if (
            GAME_STATE["skill_action"][skill]
            or GAME_STATE["player"].energy < getattr(CONFIG, skill).energy[item]
        ):
            return

        GAME_STATE["player"].energy -= getattr(CONFIG, skill).energy[item]
        GAME_STATE["skill_action"][skill] = {
            "end": pygame.time.get_ticks() + getattr(CONFIG, skill).duration[item],
            "item": item,
            "button_x": button_x,
            "button_y": button_y,
        }
        pygame.time.set_timer(event, getattr(CONFIG, skill).duration[item], loops=1)

    return callback


if __name__ == "__main__":
    asyncio.run(main())

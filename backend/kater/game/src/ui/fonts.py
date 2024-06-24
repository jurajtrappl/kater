from pathlib import Path
import pygame
import sys
from typing import Dict


def init_fonts() -> Dict[str, pygame.font.Font]:
    pygame.font.init()

    fonts_path = Path(sys.path[0]) / "fonts"
    medieval_sharp_path = fonts_path / "MedievalSharp-xOZ5.ttf"

    return {
        "player_attribute_font": pygame.font.Font(medieval_sharp_path, 30),
        "sidebar_font": pygame.font.Font(medieval_sharp_path, 24),
        "content_font": pygame.font.Font(medieval_sharp_path, 28),
        "inventory_font": pygame.font.Font(medieval_sharp_path, 16),
        "skills_font": pygame.font.Font(medieval_sharp_path, 18),
        "explore_font": pygame.font.Font(medieval_sharp_path, 20),
    }

import pygame

# Basic attributes
REFILL_ENERGY = pygame.USEREVENT + 1
REFILL_HITPOINTS = pygame.USEREVENT + 2

# Explore actions
SHORT_EXPLORE = pygame.USEREVENT + 3
MEDIUM_EXPLORE = pygame.USEREVENT + 4
LONG_EXPLORE = pygame.USEREVENT + 5

# Skills - Mining
COPPER_ORE_MINED = pygame.USEREVENT + 6
SILVER_ORE_MINED = pygame.USEREVENT + 7

# UI stuff
BLINK_INVENTORY_UPDATE_TEXT = pygame.USEREVENT + 8
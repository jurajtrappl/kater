toml_copy = {
    "sidebar": ["Inventory", "Travel", "Skills", "Explore", "Export"],
    "skills": ["mining", "woodcutting", "fishing", "herbalism", "divination"],
    "caps": {
        "energy": 100,  # max limit of energy
        "hitpoints": 100,  # max hitpoints
        "level": 100,  # max level
    },
    "display": {"size": [1280, 720], "caption": "Kater"},
    "fonts": {
        "player_attribute_font_size": 36,
        "sidebar_font_size": 24,
        "content_font_size": 28,
        "inventory_font_size": 16,
        "skills_font_size": 18,
        "explore_font_size": 20,
    },
    "globals": {"seed": 38},  # for reproducibility
    "rates": {
        "base_energy_refill": 1,  # how much energy is going to refill per 1 time unit
        "base_hitpoints_refill": 1,  # how much hitpoints is going to refill per 1 time unit
        "energy": 1000,  # 1 energy per 1 second
        "hitpoints": 1000,  # 1 hitpoints per 1 second
    },
    "inventory": {"size": 12},
    "mining": {
        "items": ["Copper Ore", "Silver Ore"],
        "energy": [5, 10],
        "duration": [5000, 10000],
        "experience": [1, 2],
    },
    "woodcutting": {
        "items": ["Oak Log", "Maple Log"],
        "energy": [5, 10],
        "duration": [5000, 10000],
        "experience": [1, 2],
    },
    "fishing": {
        "items": ["Carp", "Salmon"],
        "energy": [5, 10],
        "duration": [5000, 10000],
        "experience": [1, 2],
    },
    "herbalism": {
        "items": ["Mugwort", "Thistle"],
        "energy": [5, 10],
        "duration": [5000, 10000],
        "experience": [1, 2],
    },
    "divination": {
        "items": ["Quartz", "Jade"],
        "energy": [5, 10],
        "duration": [5000, 10000],
        "experience": [1, 2],
    },
    "explore": {
        "energy": [10, 20, 30],
        "duration": [5000, 10000, 15000],
        "experience": [10, 20, 30],
    },
}


class ConfigCaps:
    def __init__(self):
        self.energy = 100  # max limit of energy
        self.hitpoints = 100  # max hitpoints
        self.level = 100  # max level


class ConfigDisplay:
    def __init__(self):
        self.size = [1280, 720]
        self.caption = "Kater"


class ConfigFonts:
    def __init__(self) -> None:
        self.player_attribute_font_size = 36
        self.sidebar_font_size = 24
        self.content_font_size = 28
        self.inventory_font_size = 16
        self.skills_font_size = 18
        self.explore_font_size = 20


class ConfigGlobals:
    def __init__(self):
        self.seed = 38  # for reproducibility


class ConfigRates:
    def __init__(self) -> None:
        self.base_energy_refill = (
            1  # how much energy is going to refill per 1 time unit
        )
        self.base_hitpoints_refill = (
            1  # how much hitpoints is going to refill per 1 time unit
        )
        self.energy = 1000  # 1 energy per 1 second
        self.hitpoints = 1000  # 1 hitpoints per 1 second


class ConfigInventory:
    def __init__(self) -> None:
        self.size = 12


class ConfigSkill:
    def __init__(self, items, energy, duration, experience):
        self.items = items
        self.energy = energy
        self.duration = duration
        self.experience = experience


class ConfigAction:
    def __init__(self, energy, duration, experience):
        self.energy = energy
        self.duration = duration
        self.experience = experience


class Config:
    def __init__(self):
        self.sidebar = ["Inventory", "Travel", "Skills", "Explore", "Export"]
        self.skills = ["mining", "woodcutting", "fishing", "herbalism", "divination"]

        self.caps = ConfigCaps()
        self.display = ConfigDisplay()
        self.fonts = ConfigFonts()
        self.globals = ConfigGlobals()
        self.rates = ConfigRates()
        self.inventory = ConfigInventory()

        self.mining = ConfigSkill(
            items=["Copper Ore", "Silver Ore"],
            energy=[5, 10],
            duration=[5000, 10000],
            experience=[1, 2],
        )
        self.woodcutting = ConfigSkill(
            items=["Oak Log", "Maple Log"],
            energy=[5, 10],
            duration=[5000, 10000],
            experience=[1, 2],
        )
        self.fishing = ConfigSkill(
            items=["Carp", "Salmon"],
            energy=[5, 10],
            duration=[5000, 10000],
            experience=[1, 2],
        )
        self.herbalism = ConfigSkill(
            items=["Mugwort", "Thistle"],
            energy=[5, 10],
            duration=[5000, 10000],
            experience=[1, 2],
        )

        self.divination = ConfigSkill(
            items=["Quartz", "Jade"],
            energy=[5, 10],
            duration=[5000, 10000],
            experience=[1, 2],
        )

        self.explore = ConfigAction(
            energy=[10, 20, 30], duration=[5000, 10000, 15000], experience=[10, 20, 30]
        )

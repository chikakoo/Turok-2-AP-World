import settings
import typing
from . import components as components
from worlds.AutoWorld import World
from BaseClasses import MultiWorld
from Options import OptionError
from . import items, locations, web_world
from .item_table import ITEM_NAME_TO_ID
from . import options as turok2_options
from .turok2_seed import gen_turok2_seed
from .options import PrimagenGoal

class Turok2Settings(settings.Group):
    class Turok2Path(settings.FilePath):
        """
        Path to the Turok 2 executable.
        """
        is_exe = True
        description = "Turok 2 Executable"
    turok2_path: Turok2Path = Turok2Path(
        "C:/Program Files (x86)/Steam/steamapps/common/Turok 2 - Seeds of Evil/Turok2.exe")

class Turok2World(World):
    """
    Turok 2 is an FPS about fighting genetically modified dinosaurs and other creatures.
    This is specifially for the 2017 Nightdive remaster.
    """        
    game = "Turok 2"
    web = web_world.Turok2WebWorld()

    options_dataclass = turok2_options.Turok2Options
    options: turok2_options.Turok2Options
    settings: typing.ClassVar[Turok2Settings]

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = ITEM_NAME_TO_ID
    item_name_groups = items.get_item_name_groups()
    origin_region_name = "Hub"

    def __init__(self, multiworld: MultiWorld, player: int):
        """Initialize the instance variables for started/exluded levels"""
        super().__init__(multiworld, player)
        self.starting_levels = []
        self.excluded_levels = []

    def generate_early(self) -> None:
        """Sets up starting/excluded levels and validates options"""
       
        # Ensure there is a goal
        if self.options.primagen_goal == PrimagenGoal.option_none and self.options.level_goal == 0:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Goal not set. Please choose a goal from `primagen_goal` or `level_goal`.")
        
        # If there's a level goal, it must be reachable
        if self.options.level_goal > self.options.accessible_level_count:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Not enough levels to reach the goal. Adjust `level_goal`, or `accessible_level_count`.")
        
        # You can't start with more levels than you can access
        if self.options.starting_level_count > self.options.accessible_level_count:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                "Starting with too many levels. Adjust `starting_level_count` or `accessible_level_count`.")

        # You can't start with levels that will be excluded
        if not self.options.starting_level_pool.value.isdisjoint(self.options.excluded_levels.value):
            raise OptionError(f"Turok 2 for {self.player_name}: "
                "Cannot start with excluded levels. Adjust `starting_level_pool` or `excluded_levels`.")

        # The sum of excluded and accessible levels can't exceed the max number of levels
        max_levels = 6
        if (len(self.options.excluded_levels.value) + self.options.accessible_level_count) > max_levels:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                "Excluding too many levels. Adjust `excluded_levels` or `accessible_level_count`.")
        
        self.initialize_levels()

    def initialize_levels(self) -> None:
        """Computes the starting and excluded levels, which can vary per world"""
        level_name_to_number = {
            "Port of Adia": 1,
            "River of Souls": 2,
            "Death Marshes": 3,
            "Lair of the Blind Ones": 4,
            "Hive of the Mantids": 5,
            "Primagen's Lightship": 6
        }
        all_levels = list(level_name_to_number.values())
        
        # Initial set of excluded levels
        excluded_levels = [
            level_name_to_number[name]
            for name in self.options.excluded_levels.value
        ]

        # Starting levels - choose from the pool first
        starting_target = self.options.starting_level_count
        priority_starting = [
            level_name_to_number[name]
            for name in self.options.starting_level_pool.value
        ] 
        self.random.shuffle(priority_starting)
        starting_levels = priority_starting[:starting_target]

        # Fill the rest as needed
        additional_levels_needed = starting_target - len(starting_levels)
        if additional_levels_needed > 0:
            level_pool = [
                level for level in all_levels
                if level not in excluded_levels 
                and level not in starting_levels
            ]
            self.random.shuffle(level_pool)
            starting_levels.extend(level_pool[:additional_levels_needed])

        # Add the rest of the excluded levels
        max_levels = 6
        total_excluded = max_levels - self.options.accessible_level_count
        additional_levels_needed = total_excluded - len(excluded_levels)
        if additional_levels_needed > 0:
            level_pool = [
                level for level in all_levels
                if level not in excluded_levels 
                and level not in starting_levels
            ]
            self.random.shuffle(level_pool)
            excluded_levels.extend(level_pool[:additional_levels_needed])

        # Assign the world's instance variables
        self.starting_levels = starting_levels
        self.excluded_levels = excluded_levels

    def create_regions(self) -> None:
        """Creates all regions/locations/events and the completion condition"""
        locations.create_regions_and_entrances(self)
        locations.create_locations(self)
        locations.create_events(self)
        locations.create_completion_condition(self)

    def set_rules(self) -> None:
        """Sets all rules for getting to regions/locations"""
        locations.apply_entrance_rules(self)
        locations.apply_location_rules(self)

    def create_items(self) -> None:
        """Creates items and adds them to the pool"""
        items.create_all_items(self)
            
    def create_item(self, name: str) -> items.Turok2Item:
        """Creates an item for the world"""
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        """Gets a random filler item"""
        return items.get_random_filler_item_name(self)
        
    def generate_output(self, output_directory: str) -> None:
        gen_turok2_seed(self, output_directory)
    
    """
    def fill_hook(self,
        progitempool: List["Item"],
        usefulitempool: List["Item"],
        filleritempool: List["Item"],
        fill_locations: List["Location"]) -> None:
            progitempool.sort(key = lambda item: item.player == self.player and (item.name == "Shredder" or item.name == "Mag 60" or item.name == "Tek Bow"))
    """
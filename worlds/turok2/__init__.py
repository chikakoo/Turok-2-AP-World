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
       
        if self.options.primagen_goal == PrimagenGoal.option_none and self.options.level_goal == 0:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Goal not set. Please choose a goal from `primagen_goal` or `level_goal`.")
        
        max_levels = 6
        num_excluded = min(self.options.excluded_level_count, max_levels - self.options.starting_level_count)
        if self.options.level_goal > 0 and (self.options.level_goal > max_levels - num_excluded):
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Too many levels excluded to reach goal. Please adjust `excluded_level_count`, or `level_goal`.")
        
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

        # Starting level priority pool
        starting_target = self.options.starting_level_count
        priority_starting = [
            level_name_to_number[name]
            for name in self.options.starting_level_priority_pool
        ]
        self.random.shuffle(priority_starting)
        starting_levels = priority_starting[:starting_target]
        
        # Fill the rest as needed
        additional_levels_needed = starting_target - len(starting_levels)
        if additional_levels_needed > 0:
            starting_priority_set = set(starting_levels)
            excluded_priority_set = {
                level_name_to_number[name]
                for name in self.options.excluded_level_priority_pool
            }
            remaining_pool = [
                level for level in all_levels
                if level not in starting_levels
            ]
            self.random.shuffle(remaining_pool)

            # Force the excluded priority levels (that are not starting priority levels) to be last
            remaining_pool = sorted(
                remaining_pool,
                key=lambda level: (
                    level in excluded_priority_set
                    and level not in starting_priority_set
                )
            )
            starting_levels.extend(remaining_pool[:additional_levels_needed])

        self.starting_levels = starting_levels

        # Excluded level priority pool
        excluded_target = self.options.excluded_level_count
        priority_excluded = []
        for name in self.options.excluded_level_priority_pool:
            level = level_name_to_number[name]
            if level not in self.starting_levels:
                priority_excluded.append(level)
        self.random.shuffle(priority_excluded)
        excluded_levels = priority_excluded[:excluded_target]

        # Fill the rest as needed
        additional_levels_needed = excluded_target - len(excluded_levels)
        if additional_levels_needed > 0:
            remaining_pool = [
                level for level in all_levels
                if level not in self.starting_levels
                and level not in excluded_levels
            ]
            self.random.shuffle(remaining_pool)
            excluded_levels.extend(remaining_pool[:additional_levels_needed])

        self.excluded_levels = excluded_levels

        print(f"STARTING: {starting_levels}")
        print(f"EXCLUDED: {excluded_levels}")

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
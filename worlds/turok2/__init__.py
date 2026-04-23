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
        max_levels = 6

        if self.options.primagen_goal == PrimagenGoal.option_none and self.options.level_goal == 0:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Goal not set. Please choose a goal from `primagen_goal` or `level_goal`.")
        
        if not set(self.options.starting_levels).isdisjoint(self.options.excluded_levels):
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Cannot include and exclude the same level. Please fix `starting_levels` or `excluded_levels`.")
        
        starting_level_count = max(len(self.options.starting_levels.value), self.options.starting_level_count)
        excluded_level_count = max(len(self.options.excluded_levels.value), self.options.excluded_level_count)
        if (starting_level_count + excluded_level_count) > max_levels:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Exceeded level count. Please fix `(random_)starting_levels` or `(random_)excluded_levels`.")
        
        if self.options.level_goal > 0 and (self.options.level_goal > (max_levels - excluded_level_count)):
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Too many levels excluded to reach goal. Please fix `(random_)excluded_levels` or `level_goal`.")
        
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
        levels = list(level_name_to_number.values())

        self.excluded_levels = [level_name_to_number[level_name] for level_name in self.options.excluded_levels]
        self.starting_levels = [level_name_to_number[level_name] for level_name in self.options.starting_levels]

        num_levels_to_exclude = self.options.excluded_level_count - len(self.excluded_levels)
        if num_levels_to_exclude > 0:
            remaining_levels = [
                level for level in levels 
                if level not in self.excluded_levels
                and level not in self.starting_levels # So we don't accidently exclude an explicit starting level!
            ]
            self.random.shuffle(remaining_levels)
            self.excluded_levels.extend(remaining_levels[:num_levels_to_exclude])

        num_levels_to_add = self.options.starting_level_count - len(self.starting_levels)
        if num_levels_to_add > 0:
            remaining_levels = [
                level for level in levels 
                if level not in self.starting_levels
                and level not in self.excluded_levels
            ]
            self.random.shuffle(remaining_levels)
            self.starting_levels.extend(remaining_levels[:num_levels_to_add])

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
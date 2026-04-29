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
from collections import Counter, defaultdict

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
        """
        Initialize instance variables
        - starting_levels: What levels are started with
        - excluded_levels: What level locations to exclude
        - item_distributions; Dict from ItemType to counts of vanilla item types
        """
        super().__init__(multiworld, player)
        self.starting_levels = []
        self.excluded_levels = []
        self.item_distributions = defaultdict(int)

    def generate_early(self) -> None:
        """Sets up starting/excluded levels and validates options"""
       
        # Ensure there is a goal
        if self.options.primagen_goal == PrimagenGoal.option_none and self.options.level_goal == 0:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Goal not set. Please choose a goal from `primagen_goal` or `level_goal`.")
        
        # Level validation setup
        max_levels = 6
        starting_random_options, starting_specific_levels = self.parse_level_option(self.options.starting_levels.value)
        excluded_random_options, excluded_specific_levels = self.parse_level_option(self.options.excluded_levels.value)

        starting_level_count = len(starting_random_options) + len(starting_specific_levels)
        excluded_level_count = len(excluded_random_options) + len(excluded_specific_levels)
        accessible_level_count = max_levels - excluded_level_count

        # You must start with at least one level
        if starting_level_count == 0:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Starting levels must have at least one entry. Adjust `starting_levels`.")

        # You must be able to reach your level goal
        if self.options.level_goal > accessible_level_count:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Not enough levels to reach the goal. Adjust `level_goal` or `excluded_levels`.")
        
        # You can't start with more levels than you can access
        if starting_level_count > accessible_level_count:
            raise OptionError(f"Turok 2 for {self.player_name}: "
                f"Starting + excluded level count is more than {max_levels}. Adjust `starting_levels` or `excluded_levels`.")

        # You can't start with levels that will be excluded
        if not starting_specific_levels.isdisjoint(excluded_specific_levels):
            raise OptionError(f"Turok 2 for {self.player_name}: "
                "Starting levels cannot be excluded. Adjust `starting_levels` or `excluded_levels`.")
        
        self.initialize_levels()

    @staticmethod
    def parse_level_option(level_option: list[str]) -> tuple[list[str], set[int]]:
        """
        Parses the level option and returns the following in a tuple:
        - A list of all the random options (since they can be duplicates)
        - A set of all the levels, in their integer form
        """
        level_name_to_number = {
            "Port of Adia": 1,
            "River of Souls": 2,
            "Death Marshes": 3,
            "Lair of the Blind Ones": 4,
            "Hive of the Mantids": 5,
            "Primagen's Lightship": 6
        }
        random_choices = ["Random", "RandomEarly", "RandomLate"]

        random_options = [
            level for level in level_option
            if level in random_choices
        ]
        specific_level_options = set([
            level_name_to_number[level] 
            for level in level_option 
            if level not in random_choices
        ])

        return (random_options, specific_level_options)

    def initialize_levels(self) -> None:
        """Computes the starting and excluded levels, which can vary per world"""

        def pick_levels(
            self,
            count: int,
            level_pool: list[int],
            deprioritized: set[int] | None = None) -> list[int]:
            """
            Helper to pick levels for each random category, deprioriting those
            in the given set.
            """
            if count == 0:
                return []

            self.random.shuffle(level_pool)

            if deprioritized:
                level_pool.sort(key=lambda level: level in deprioritized)

            chosen_levels = level_pool[:count]
            del level_pool[:count]
            return chosen_levels

        # Setup
        starting_random_options, starting_specific_levels = self.parse_level_option(self.options.starting_levels.value)
        excluded_random_options, excluded_specific_levels = self.parse_level_option(self.options.excluded_levels.value)

        # Initialize starting and excluded with their specific levels, removing them from the pool
        self.starting_levels = list(starting_specific_levels)
        self.excluded_levels = list(excluded_specific_levels)
        level_pool = [
            level for level in [1, 2, 3, 4, 5, 6]
            if level not in self.starting_levels
            and level not in self.excluded_levels
        ]

        # Add the random levels to the lists
        starting_option_counts = Counter(starting_random_options)
        excluded_option_counts = Counter(excluded_random_options)
        early_levels = {1, 2, 3}
        late_levels = {4, 5, 6}
        
        # Early/Starting first, so early starts are guaranteed
        # Then Late/Excluded so harder levels can be excluded
        self.starting_levels.extend(
            pick_levels(self, starting_option_counts.get("RandomEarly", 0), level_pool, deprioritized=late_levels))
        self.excluded_levels.extend(
            pick_levels(self, excluded_option_counts.get("RandomLate", 0), level_pool, deprioritized=early_levels))

        # It's slightly easier to exclude early than to start late, so these go in this order
        self.excluded_levels.extend(
            pick_levels(self, excluded_option_counts.get("RandomEarly", 0), level_pool, deprioritized=late_levels))
        self.starting_levels.extend(
            pick_levels(self, starting_option_counts.get("RandomLate", 0), level_pool, deprioritized=early_levels))
        
        # These two can go in whatever order
        self.starting_levels.extend(
            pick_levels(self, starting_option_counts.get("Random", 0), level_pool))
        self.excluded_levels.extend(
            pick_levels(self, excluded_option_counts.get("Random", 0), level_pool))

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
        return items.get_random_filler_item_name()
        
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
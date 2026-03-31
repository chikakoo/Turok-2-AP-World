import settings
import typing
from . import components as components
from worlds.AutoWorld import World
from . import items, locations, web_world
from .item_table import ITEM_NAME_TO_ID
from . import options as turok2_options
from .turok2_seed import gen_turok2_seed

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
    origin_region_name = "PoA Start"
    
    def create_regions(self) -> None:
        locations.create_regions_and_entrances(self)
        locations.create_locations(self)
        locations.create_events(self)
        locations.create_completion_condition(self)

    def set_rules(self) -> None:
        locations.apply_entrance_rules(self)
        locations.apply_location_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)
            
    def create_item(self, name: str) -> items.Turok2Item:
        return items.create_item_with_correct_classification(self, name)
        
    def get_filler_item_name(self) -> str:
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
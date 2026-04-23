import os
import io
import zipfile
import Utils
from worlds.Files import APPlayerContainer
from typing import TYPE_CHECKING
from .locations import LOCATION_TABLE
from .items import ITEM_TABLE, ItemType, APMessageType
from .options import PrimagenGoal, PrimagenKeys

if TYPE_CHECKING:
    from . import Turok2World
    
class Turok2Container(APPlayerContainer):
    game: str = 'Turok 2'

    def __init__(self, rando_replacements: str, ap_settings: str, 
                base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.rando_replacements = rando_replacements
        self.ap_settings = ap_settings
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path)
        self.patch_file_ending = ".apturok2"
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Writes the contents of the patch_data into rando.kpf, so the player
        can drop it off in their Turok 2 mod folder.
        """
        kpf_buffer = io.BytesIO()
        with zipfile.ZipFile(kpf_buffer, "w", zipfile.ZIP_DEFLATED) as kpf_zip:
            kpf_zip.writestr("rando/randoReplacements.as", self.rando_replacements)
            kpf_zip.writestr("rando/apSettings.as", self.ap_settings)
            
        opened_zipfile.writestr("rando.kpf", kpf_buffer.getvalue())
        super().write_contents(opened_zipfile)
        
def gen_turok2_seed(self: "Turok2World", output_directory: str):
    seed_name = self.multiworld.seed_name
    ap_version = Utils.__version__
    
    mod_name = f"AP-{seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + ap_version + ".zip")
    mod = Turok2Container(
        get_angelscript(self),
        get_settings_string(self),
        mod_dir, 
        output_directory, 
        self.player,
        self.multiworld.get_file_safe_player_name(self.player))
    mod.write()

def get_angelscript(self: "Turok2World") -> str:
    """
    Gets the AngelScript code for all location replacements.
    """
    return get_angelscript_from_filled_locations(self) + get_angelscript_for_ammo(self)
    
def get_angelscript_from_filled_locations(self: "Turok2World") -> str:
    """
    Gets the AngelScript code needed for the mod to place the correct
    actors for the randomized locations.
    """
    angelscript_snippets = []
    for location in self.multiworld.get_filled_locations(self.player):
        # This is an event, so we don't care about it
        if location.address is None:
            continue

        location_name = location.name
        location_id = LOCATION_TABLE[location_name]["ap_id"]

        # Add the appropriate kind of snippet based on the type
        type = LOCATION_TABLE[location_name]["type"]
        if type in (ItemType.SWITCH.value, ItemType.MISSION_OBJECTIVE.value):
            location_tag_id = LOCATION_TABLE[location_name]["tag_id"]
            snippet = f"AddActionObject(\"{location_name}\", {location_id}, {location_tag_id}"
        else:
            location_position = LOCATION_TABLE[location_name]["position"]
            snippet = f"AddReplacement(\"{location_name}\", {location_id}, \"{location_position}\""
        
        # If the item is for this world, the actor id should be the last parameter
        if location.item and location.item.player == self.player:
            snippet += f", {ITEM_TABLE[location.item.name]["actor_id"]});"
        # Else, it should be the location name and player name (so we can display it on pickup)
        else:
            if location.item.advancement:
                is_progression = "true"
            else:
                is_progression = "false"
            player_name = self.multiworld.get_player_name(location.item.player)
            snippet += f", \"{player_name}'s {location.item.name}\", {is_progression});"
        
        angelscript_snippets.append(snippet)
        
    return "\n".join(angelscript_snippets)

def get_angelscript_for_ammo(self: "Turok2World") -> str:
    """
    If we are shuffling weapons (but not ammo), we need to force all static ammo to be random.
    This gets the AngelScript needed to replace that ammo.

    Use the negative version of the location id so we can still manage whether the item has
    been collected. This will tell the mod to still replace the item, and to tell it that
    it isn't an AP check.
    """
    if not self.options.weapon_sanity or self.options.ammo_sanity:
        return ""
    
    angelscript_snippets = []
    actor_id = ITEM_TABLE["Random Ammo Pack"]["actor_id"]
    for loc_name, loc_info in LOCATION_TABLE.items():
        if loc_info.get("type", -1) == ItemType.AMMO.value:
            loc_position = loc_info.get("position")
            loc_id = loc_info.get("ap_id") * -1
            snippet = f"AddReplacement(\"{loc_name}\", {loc_id}, \"{loc_position}\", {actor_id});"
            angelscript_snippets.append(snippet)

    return "\n" + "\n".join(angelscript_snippets)
    
def get_settings_string(self: "Turok2World") -> str:
    """
    Sets up the macro file with any settings the game needs to know:
    - OPTION_GOAL_PRIMAGEN_LAIR: Whether entering the lair is the goal
    - OPTION_GOAL_DEFEAT_PRIMAGEN: Whether defeating the Primagen is the goal
    - OPTION_GOAL_LEVELS: How many levels is the goal
    - OPTION_GOAL_LEVELS_GIVE_PRIMAGEN_KEYS: Whether reaching the level goal should give all primagen keys
    - OPTION_WEAPON_SANITY: Whether weapons shuffled (used for replacing ammo spawns)
    - OPTION_PROGRESSIVE_WARPS: The strength of progressive warps - 0 if it is off
    - OPTION_EXCLUDED_LEVELS: What levels will never be accessible
    - OPTION_RANDOM_AMMO_MIN: The min percentage of random ammo you can get
    - OPTION_RANDOM_AMMO_MAX: The max percentage of random ammo you can get
    - OPTION_STARTING_INVENTORY_ITEMS: An array of ints containing starting inventory items
    - OPTION_STARTING_WEAPONS: An array of ints containing starting weapons
    - OPTION_LEVEL_KEY_PACKS: Receive all level keys at once when getting one of them
    """
    # Defaults - will result in no goal
    primagen_lair_is_goal = "false"
    defeat_primagen_is_goal = "false"
    level_goal = self.options.level_goal
    levels_give_primagen_keys = "false"
    weapon_sanity = "false"
    progressive_warps = 0
    level_key_packs = "false"

    # Set whether levels give primagen keys
    if self.options.primagen_keys == PrimagenKeys.option_levels:
        levels_give_primagen_keys = "true"

    # Set what the goal map is
    if self.options.primagen_goal == PrimagenGoal.option_get_to_lair:
        primagen_lair_is_goal = "true"
    elif self.options.primagen_goal == PrimagenGoal.option_defeat:
        defeat_primagen_is_goal = "true"

    # Weapon and ammo locations
    if self.options.weapon_sanity:
        weapon_sanity = "true"

    # Progressive warps
    if self.options.progressive_warps:
        progressive_warps = self.options.progressive_warp_strength

    # Level key packs
    if self.options.level_key_packs:
        level_key_packs = "true"

    # Starting inventory
    inventory_item_ids = []
    weapon_item_ids = []
    for item in self.multiworld.precollected_items[self.player]:
        item_data = ITEM_TABLE[item.name]
        if item_data.get("msg_type") == APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value:
            inventory_item_ids.append(item_data["actor_id"])
        elif item_data.get("type") == ItemType.WEAPON.value:    
            weapon_item_ids.append(item_data["actor_id"])

    def format_starting_items_macro(name: str, values: list[int]) -> str:
        if values:
            joined = ", ".join(str(v) for v in values)
            return f"#define {name} {joined}\n"
        else:
            return f"#define {name}\n"

    return (f"#define OPTION_GOAL_PRIMAGEN_LAIR {primagen_lair_is_goal}\n" +
        f"#define OPTION_GOAL_DEFEAT_PRIMAGEN {defeat_primagen_is_goal}\n" +
        f"#define OPTION_GOAL_LEVELS {level_goal}\n" +
        f"#define OPTION_GOAL_LEVELS_GIVE_PRIMAGEN_KEYS {levels_give_primagen_keys}\n" +
        f"#define OPTION_WEAPON_SANITY {weapon_sanity}\n" +
        f"#define OPTION_PROGRESSIVE_WARPS {progressive_warps}\n" +
        format_starting_items_macro("OPTION_EXCLUDED_LEVELS", self.excluded_levels) +
        f"#define OPTION_RANDOM_AMMO_MIN {self.options.min_random_ammo_percent}\n" +
        f"#define OPTION_RANDOM_AMMO_MAX {self.options.max_random_ammo_percent}\n" +
        format_starting_items_macro("OPTION_STARTING_INVENTORY_ITEMS", inventory_item_ids) +
        format_starting_items_macro("OPTION_STARTING_WEAPONS", weapon_item_ids) +
        f"#define OPTION_LEVEL_KEY_PACKS {level_key_packs}")

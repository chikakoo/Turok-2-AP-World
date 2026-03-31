from __future__ import annotations
import json
import pkgutil
import importlib.resources as resources
from typing import TYPE_CHECKING
from BaseClasses import Location, Region
from worlds.generic.Rules import set_rule
from .options import Goal, PrimagenLair, GameLogicDifficulty, WeaponLogicDifficulty
from . import items
from .items import ItemType

if TYPE_CHECKING:
    from . import Turok2World

class Turok2Location(Location):
    game = "Turok 2"

LOCATION_TABLE = json.loads(
    pkgutil.get_data(__name__, "data/locations.json").decode()
)
LOCATION_NAME_TO_ID = {
    name: data["ap_id"] for name, data in LOCATION_TABLE.items()
}

def load_all_region_data():
    """
    Loads all regions from the "level" files in the data path.
    """
    all_regions = []
    data_package = __package__ + ".data"

    for file in resources.files(data_package).iterdir():
        if file.name.startswith("level") and file.name.endswith(".json"):
            data = json.loads(file.read_text())
            all_regions.extend(data.get("regions", []))

    return all_regions

def create_regions_and_entrances(world: Turok2World) -> None:
    """
    Creates regions and connects them together based on the json data.
    Includes putting a "rule_json" property in the table to construct the rules later on.
    """
    regions = load_all_region_data()
    region_map = {}

    # Create all regions
    for region_data in regions:
        region_name = region_data["name"]
        region = Region(region_name, world.player, world.multiworld)
        region_map[region_name] = region
        world.multiworld.regions.append(region)

    # Connect the regions with entrances
    for region_data in regions:
        from_region = region_map[region_data["name"]]

        for exit_data in region_data.get("exits", []):
            to_region = region_map[exit_data["to"]]

            entrance_name = f"{from_region.name} -> {to_region.name}"
            entrance = from_region.connect(
                to_region,
                entrance_name
            )
            entrance.rule_json = exit_data.get("rule")
            
def create_locations(world: Turok2World) -> None:
    """
    Creates the locations by looking at all of the regions defined in the json data.
    Includes putting a "rule" property in the table to construct the rules later on.
    """
    for loc_name, loc_info in LOCATION_TABLE.items():
        # Exclude relevent locations if not shuffled
        item_type = loc_info.get("type", -1)
        if not world.options.include_health_locations and item_type == ItemType.HEALTH.value:
            continue
        if (not world.options.include_weapon_and_ammo_locations and
            (item_type == ItemType.AMMO.value or item_type == ItemType.WEAPON.value)):
            continue
        if not world.options.include_life_force_locations and item_type == ItemType.LIFE_FORCE.value:
            continue
        if not world.options.include_mission_item_locations and item_type == ItemType.MISSION_ITEM.value:
            continue
        # TODO: When Nuke Parts can be vanilla, we'd disable their locations here
        
        region_obj = world.get_region(loc_info["region"])
        location = Turok2Location(
            world.player,
            loc_name,
            loc_info["ap_id"],
            region_obj
        )
        region_obj.locations.append(location)
            
def create_events(world: Turok2World) -> None:
    """
    Creates events in regions from the JSON data.
    Each event can optionally have a rule, which is parsed and applied.
    """
    for region_data in load_all_region_data():
        region_name = region_data["name"]
        region_obj = world.get_region(region_name)

        for event_name, event_info in region_data.get("events", {}).items():
            # Do NOT add events that will not be relevent
            if event_info.get("rule") == "vanilla_mission_items" and world.options.include_mission_item_locations:
                continue

            rule_func = None
            if "rule" in event_info:
                rule_func = build_rule(event_info["rule"], world)

            region_obj.add_event(
                event_info.get("location_name"),
                item_name=event_name,
                rule=rule_func,
                location_type=Turok2Location,
                item_type=items.Turok2Item,
            )

def create_completion_condition(world: Turok2World):
    """
    Creates the completion condition based on the goal setting.
    - Primagen: The primagen goal - can be getting to it, or defeating it
    - Levels: The number of levels to complete for the goal
    """
    # Levels goal - just check number of levels
    if world.options.goal == Goal.option_levels:
        world.multiworld.completion_condition[world.player] = \
            lambda state: state.has("Level Complete", world.player, world.options.levels_goal)

    # Primagen goal (the lair is in the Hub, so always check for that)
    elif world.options.goal == Goal.option_primagen:
        # If there's levels also, check the keys and the level goal count
        if world.options.primagen_lair == PrimagenLair.option_levels:
            world.multiworld.completion_condition[world.player] = \
                lambda state: (state.can_reach_region("Hub", world.player) and
                    state.has("Level Complete", world.player, world.options.levels_goal) and
                    state.has_group_unique("Primagen Key", world.player, 6))
        # Otherwise, we just need to check for keys
        else:
            world.multiworld.completion_condition[world.player] = \
                lambda state: (state.can_reach_region("Hub", world.player) and
                    state.has_group_unique("Primagen Key", world.player, 6))
    
def apply_location_rules(world: Turok2World):
    """
    Apply rules that need to go on locations based on locationRules.json
    """
    location_rules = json.loads(
        pkgutil.get_data(__name__, "data/locationRules.json").decode()
    )
    for loc_name, rule in location_rules.items():
        location = world.get_location(loc_name)
        if location is None:
            #TODO: print instead of raise in the final version
            raise Exception(f"Could not apply location rule to location: {loc_name}")
        rule_func = build_rule(rule, world)
        set_rule(location, rule_func)

def apply_entrance_rules(world: Turok2World) -> None:
    """
    Set the rules grabbed from the json earlier for for each entrance.
    """
    for region in world.multiworld.get_regions(world.player):
        for entrance in region.exits:
            rule_json = getattr(entrance, "rule_json", None)

            if rule_json is not None:
                rule = build_rule(rule_json, world)
                set_rule(entrance, rule)
        
def build_rule(rule_json, world: Turok2World):
    """
    Builds the rule, given the json.
    Supports specific functions, and/or, and has, which will check for items or categories.
    - See NAMED_RULES for the specific functions supported.
    """
    # Named rule (no parameters)
    if isinstance(rule_json, str):
        if rule_json not in NAMED_RULES:
            raise Exception(f"Unknown named rule: {rule_json}")
        return NAMED_RULES[rule_json](world)
    
    # Named rule (with parameters)
    if isinstance(rule_json, dict):
        # Named rule with parameters
        if len(rule_json) == 1:
            rule_name, rule_args = next(iter(rule_json.items()))
            if rule_name in NAMED_RULES:
                return NAMED_RULES[rule_name](world, rule_args)

    if "and" in rule_json:
        subrules = [build_rule(r, world) for r in rule_json["and"]]
        return make_and_rule(subrules)

    if "or" in rule_json:
        subrules = [build_rule(r, world) for r in rule_json["or"]]
        return make_or_rule(subrules)

    if "has" in rule_json:
        return build_has_rule(rule_json["has"], world)
        
    raise Exception(f"Unknown rule: {rule_json}")
    
def make_and_rule(subrules):
    """Makes the 'and' rule."""
    return lambda state: all(rule(state) for rule in subrules)
    
def make_or_rule(subrules):
    """Makes the 'or' rule."""
    return lambda state: any(rule(state) for rule in subrules)
    
def build_has_rule(has_data, world: Turok2World):
    """
    Checks whether the player...
    - Has the given item, if passed a string
    - Has all the given items, if passed a list
    - Has the given count of items, if given an "item" object
    - Has the given count of unique items of the given category, if given a "category" object
    """
    player = world.player
    
    # Simple case: the string or string array is passed directly
    if isinstance(has_data, str):
        return lambda state: state.has(has_data, player)
        
    if isinstance(has_data, list):
        if not all(isinstance(x, str) for x in has_data):
            raise Exception(f"'has' list must contain only strings: {has_data}")
        return lambda state: state.has_all(has_data, player)
        
    # Complex case: "has" is an object
    item = has_data.get("item")
    count = has_data.get("count", 1)
    category = has_data.get("category")
    
    if item:
        return lambda state: state.has(item, player, count)
    if category:
        return compute_category_rule(world, category, count)
        
    raise Exception(f"Invalid 'has' rule: {has_data}")

def compute_category_rule(world: Turok2World, category: str, count: int = 1):
    """
    Checks whether the player has the given count of unique items of the given category
    """
    return lambda state: state.has_group_unique(category, world.player, count)

def advanced_game_logic(world: Turok2World):
    """Checks advanced game logic is on."""
    enabled = world.options.game_logic_difficulty == GameLogicDifficulty.option_advanced
    return lambda state: enabled
    
def advanced_weapon_logic(world: Turok2World):
    """Checks advanced weapon logic is on."""
    enabled = world.options.weapon_logic_difficulty == WeaponLogicDifficulty.option_advanced
    return lambda state: enabled

def weapon_requirement(world: Turok2World, args: dict):
    """
    Checks whether the weapon requirements are met (categories and count).
    Returns true if weapons are not randomized, as it's assumed the game's given weapons are enough.
    """
    if not world.options.include_weapon_and_ammo_locations:
        return lambda state: True

    category = args.get("category")
    if not category:
        raise Exception("weapon_requirement missing 'category'")

    count = args.get("count", 1)
    return compute_category_rule(world, category, count)
    
def vanilla_mission_items(world: Turok2World):
    """Checks whether mission items in their vanilla locations."""
    is_vanilla = not world.options.include_mission_item_locations
    return lambda state: is_vanilla
    
def mission_item_requirement(world: Turok2World, args: dict):
    """
    Checks mission items. Returns True if we aren't shuffling them because the game logic should work here.
    """
    if world.options.include_mission_item_locations:
        count = args.get("count", 1)
        item = args.get("item")
        return lambda state: state.has(item, world.player, count)
    
    return lambda state: True

    # Vanilla, so check all the needed events
    # This will check that we have at least "count" number of events in the list
    # This is meant to cover whether we can progress with any of the items
    #event_items = args.get("event_items", [])
    #return lambda state: all(state.has(event, player) for event in event_items)
    
NAMED_RULES = {
    "advanced_game_logic": advanced_game_logic,
    "advanced_weapon_logic": advanced_weapon_logic,
    "weapon_requirement": weapon_requirement,
    "vanilla_mission_items": vanilla_mission_items,
    "mission_item_requirement": mission_item_requirement
}
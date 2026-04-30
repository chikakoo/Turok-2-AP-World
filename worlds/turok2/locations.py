from __future__ import annotations
import json
import re
import pkgutil
import math
import importlib.resources as resources
from typing import TYPE_CHECKING
from BaseClasses import Location, Region
from worlds.generic.Rules import set_rule
from .options import PrimagenGoal, RandomizePrimagenKeys, NukeBehavior, \
    RandomizeHealthPickups, RandomizeAmmoPickups, RandomizeLifeForces, FillerDistribution
from . import items
from .items import ItemType, WeightedItemGroup, ITEM_TYPE_TO_GROUP

if TYPE_CHECKING:
    from . import Turok2World

class Turok2Location(Location):
    game = "Turok 2"

def _load_all_location_data():
    """
    Loads all regions from the "locations_level" files in the data path.
    Sets the level number on each location for later use.
    """
    all_locations = {}
    data_package = __package__ + ".data"

    for file in resources.files(data_package).iterdir():
        if file.name.startswith("locations_level") and file.name.endswith(".json"):
            # Extract the level number from the file name
            match = re.search(r"locations_level(\d+)", file.name)
            level = int(match.group(1)) if match else -1
            
            # Inject the level into each location
            data = json.loads(file.read_text())
            for _, loc_data in data.items():
                loc_data["level"] = level
                all_locations.update(data)

    return all_locations

LOCATION_TABLE = _load_all_location_data()
LOCATION_NAME_TO_ID = {
    name: data["ap_id"] for name, data in LOCATION_TABLE.items()
}

def load_all_region_data(world: Turok2World):
    """
    Loads all regions from the "level" files in the data path.
    """
    all_regions = []
    data_package = __package__ + ".data"

    for file in resources.files(data_package).iterdir():
        if file.name.startswith("level") and file.name.endswith(".json"):
            data = json.loads(file.read_text())
            if data.get("level", -1) in world.excluded_levels:
                continue

            all_regions.extend(data.get("regions", []))

    return all_regions

def create_regions_and_entrances(world: Turok2World) -> None:
    """
    Creates regions and connects them together based on the json data.
    Includes putting a "rule_json" property in the table to construct the rules later on.
    """
    regions = load_all_region_data(world)
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
            if exit_data.get("level", -1) in world.excluded_levels:
                continue

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
    """
    def add_location(world: Turok2World,  loc_name: str, loc_info) -> None:
        """
        Adds the given location to the world.
        Also adds the appropriate info to the category/item weights dictionaries.
        """
        region_obj = world.get_region(loc_info["region"])
        location = Turok2Location(
            world.player,
            loc_name,
            loc_info["ap_id"],
            region_obj
        )
        region_obj.locations.append(location)

        # Assign item weights and distributions to support the vanilla options
        item_type_raw = loc_info.get("type", None)
        if item_type_raw is not None:
            item_type = ItemType(item_type_raw)
            if world.options.filler_distribution == FillerDistribution.option_vanilla:
                world.vanilla_item_counts[item_type] += 1
    
    def try_add_location(world: Turok2World, loc_name: str, loc_info: dict) -> bool:
        """
        Determines whether a location should be included based on the settings and its type.
        Returns whether it was included.
        
        If this is a location that can have a % of checks added, this will always return false
        but add the entry to the appropriate world instance variable.
        """
        item_type = loc_info.get("type", None)
        item_group = ITEM_TYPE_TO_GROUP.get(ItemType(item_type), None)

        if item_type == ItemType.WEAPON.value:
            return world.options.randomize_weapons
        if item_type == ItemType.AMMO.value:
            world.ammo_pickup_locations.append((loc_name, loc_info))
            return False
        if item_group == WeightedItemGroup.HEALTH:
            world.health_pickup_locations.append((loc_name, loc_info))
            return False
        if item_group == WeightedItemGroup.LIFE_FORCE:
            world.life_force_locations.append((loc_name, loc_info))
            return False
        if item_type == ItemType.MISSION_ITEM.value:
            return world.options.randomize_mission_items
        if item_type == ItemType.NUKE_PART.value:
            return world.options.nuke_behavior in (
                NukeBehavior.option_disabled,
                NukeBehavior.option_nuke_part_hunt,
                NukeBehavior.option_weapon_pickup
            )
        if item_type == ItemType.SWITCH.value:
            return world.options.randomize_switches
        if item_type == ItemType.MISSION_OBJECTIVE.value:
            return world.options.randomize_mission_objectives

        return True
    
    def resolve_locations_with_option(
        world,
        locations: list[tuple[str, dict]],
        option: int,
        special_names: dict[str, int],
        filters: dict[int, callable] = None) -> list[tuple[str, dict]]:
        """
        Resolves a list of locations based on a NamedRange-style option.
        - locations: [(loc_name, loc_info)]
        - option: The option value
        - special_names: The option's special_range_names
        - filters: Optional mapping of special option values -> filter functions
        """
        filters = filters or {}
        NONE = special_names.get("none")
        ALL = special_names.get("all")

        if option == NONE:
            return []
        if option == ALL:
            return list(locations)
        if option in filters:
            return [loc for loc in locations if filters[option](loc)]

        return select_percentage(world, locations, option)
    
    def add_ammo_locations(world: Turok2World) -> None:
        """
        Adds all the ammo locations to the loction list.
        If it's a % fill, adds the appropriate percentage of locations.
        """
        selected = resolve_locations_with_option(
            world,
            world.ammo_pickup_locations,
            world.options.randomize_ammo_pickups.value,
            RandomizeAmmoPickups.special_range_names
        )

        for loc_name, loc_info in selected:
            world.included_ammo_pickup_locations.append((loc_name, loc_info))
            add_location(world, loc_name, loc_info)

    def add_health_locations(world: Turok2World) -> None:
        """
        Adds all the health locations to the loction list.
        If it's a % fill, adds the appropriate percentage of locations.
        """
        special = RandomizeHealthPickups.special_range_names
        filters = {
            special["full_and_ultra_only"]:
                lambda loc: loc[1]["type"] in (ItemType.FULL_HEALTH.value, ItemType.ULTRA_HEALTH.value)
        }

        selected = resolve_locations_with_option(
            world,
            world.health_pickup_locations,
            world.options.randomize_health_pickups.value,
            special,
            filters
        )

        for loc_name, loc_info in selected:
            add_location(world, loc_name, loc_info)

    def add_life_force_locations(world: Turok2World) -> None:
        """
        Adds all the life froce locations to the loction list.
        If it's a % fill, adds the appropriate percentage of locations.
        """
        special = RandomizeLifeForces.special_range_names
        filters = {
            special["yellow_only"]: lambda loc: loc[1]["type"] == ItemType.LIFE_FORCE_1.value,
            special["red_only"]: lambda loc: loc[1]["type"] == ItemType.LIFE_FORCE_10.value,
        }
        selected = resolve_locations_with_option(
            world,
            world.life_force_locations,
            world.options.randomize_life_forces.value,
            special,
            filters
        )

        for loc_name, loc_info in selected:
            add_location(world, loc_name, loc_info)
    
    def select_percentage(world, items, percent):
        """
        Selects a random percentage of values from the given list of items.
        """
        count = round(len(items) * percent / 100)
        shuffled = list(items)
        world.random.shuffle(shuffled)
        return shuffled[:count]
            
    for loc_name, loc_info in LOCATION_TABLE.items():
        if loc_info["level"] in world.excluded_levels:
            continue

        if try_add_location(world, loc_name, loc_info):
            add_location(world, loc_name, loc_info)

    add_ammo_locations(world)
    add_health_locations(world)
    add_life_force_locations(world)
    
def create_events(world: Turok2World) -> None:
    """
    Creates events in regions from the JSON data.
    Each event can optionally have a rule, which is parsed and applied.
    """
    for region_data in load_all_region_data(world):
        region_name = region_data["name"]
        region_obj = world.get_region(region_name)

        for event_info in region_data.get("events", []):
            rule_func = None
            if "rule" in event_info:
                rule_func = build_rule(event_info["rule"], world)

            event_name = event_info.get("name")
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

    Levels: The number of levels the player needs to clear.
    Primagen Keys: The number of primagen keys needed for the goal.
                   This is 6 if the primagen is required, and 0 otherwise.
    """
    level_goal = world.options.level_goal
    primagen_keys_needed = []

    if (world.options.primagen_goal != PrimagenGoal.option_none and
        world.options.randomize_primagen_keys != RandomizePrimagenKeys.option_levels):
        primagen_keys_needed = [
            "Primagen Key 1",
            "Primagen Key 2",
            "Primagen Key 3",
            "Primagen Key 4",
            "Primagen Key 5",
            "Primagen Key 6"
        ]

    world.multiworld.completion_condition[world.player] = \
        lambda state: (state.has("Level Complete", world.player, level_goal) and 
            state.has_all(primagen_keys_needed, world.player))
    
def apply_location_rules(world: Turok2World):
    """
    Apply rules that need to go on locations based on locationRules.json
    """
    location_rules = json.loads(
        pkgutil.get_data(__name__, "data/locationRules.json").decode()
    )
    for loc_name, rule in location_rules.items():
        try:
            location = world.get_location(loc_name)
            rule_func = build_rule(rule, world)
            set_rule(location, rule_func)
        except:
            # This could happen if it's an excluded location, which is fine
            pass

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

def has_level_keys(world: Turok2World, args: dict):
    """
    Checks whether the specified number of level keys are obtained for a given level.
    If level key packs are used, will only check if one key is obtained.
    """
    count = 1 if world.options.level_key_packs else args.get("count", 1)
    item = args.get("item")
    return lambda state: state.has(item, world.player, count)

def weapon_requirement(world: Turok2World, args: dict):
    """
    Checks whether the weapon requirements are met (categories and count).
    Returns true if weapons are not randomized, as it's assumed the game's given weapons are enough.
    """
    if not world.options.randomize_weapons:
        return lambda state: True

    category = args.get("category")
    if not category:
        raise Exception("weapon_requirement missing 'category'")

    count = args.get("count", 1)
    return compute_category_rule(world, category, count)
    
def mission_item_requirement(world: Turok2World, args: dict):
    """
    Checks mission items. Returns True if we aren't shuffling them because the game logic should work here.
    """
    if world.options.randomize_mission_items:
        count = args.get("count", 1)
        item = args.get("item")
        return lambda state: state.has(item, world.player, count)
    
    return lambda state: True

def not_guaranteed_torpedo_launcher(world: Turok2World):
    """Checks whether the Torpedo Launcher is in logic"""
    not_guaranteed_torpedo_launcher = not world.options.guarantee_torpedo_launcher
    return lambda state: not_guaranteed_torpedo_launcher

def weapons_not_randomized(world: Turok2World):
    """Checks whether weapons are not randomized"""
    weapons_not_randomized = not world.options.randomize_weapons
    return lambda state: weapons_not_randomized

def progressive_warp(world: Turok2World, args: dict):
    """
    Validates the progressive warp item.
    - If the setting is off, returns True
    - Else checks whether the right number of progressive items exist

    Expects...
    - count: The base count of required progressive warps to pass through here
    - level: The level this is for (to retrieve the matching item)
    """
    if not world.options.progressive_warps:
        return lambda state: True

    strength = max(world.options.progressive_warp_strength, 1)
    count = math.ceil(args.get("count", 1) / strength)
    level = args.get("level", -1)
    if level == -1:
        raise Exception("progressive_warp missing level!")
    
    item = f"Progressive Warp L{level}"
    return lambda state: state.has(item, world.player, count)

NAMED_RULES = {
    "has_level_keys": has_level_keys,
    "weapon_requirement": weapon_requirement,
    "mission_item_requirement": mission_item_requirement,
    "not_guaranteed_torpedo_launcher": not_guaranteed_torpedo_launcher,
    "weapons_not_randomized": weapons_not_randomized,
    "progressive_warp": progressive_warp
}
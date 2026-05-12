from __future__ import annotations
import math
from .item_table import *
from typing import TYPE_CHECKING, Iterable
from BaseClasses import Item
from .options import NukeBehavior, PrimagenGoal, RandomizePrimagenKeys, RandomizeTalismans, FillerDistribution
from collections import Counter, defaultdict

if TYPE_CHECKING:
    from . import Turok2World

class Turok2Item(Item):
    game = "Turok 2"

def get_item_name_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}

    for name, data in ITEM_TABLE.items():
        for group in data.get("groups", []):
            groups.setdefault(group, set()).add(name)

    return groups
    
def get_random_filler_item_name(world: Turok2World) -> str:
    """
    world.py will use this to generate filler items.
    Any non-vanilla pickups items will be generated from this.
    """
    fallback_item = "Life Force 1"
    category_pairs = [
        (WeightedItemGroup.HEALTH, world.options.filler_health_weight),
        (WeightedItemGroup.AMMO, world.options.filler_ammo_weight),
        (WeightedItemGroup.LIFE_FORCE, world.options.filler_life_force_weight)
    ]
    names, weights = prepare_weights(category_pairs)
    if not names:
        return fallback_item

    category = world.random.choices(names, weights=weights, k=1)[0]
    if category == WeightedItemGroup.AMMO:
        item = get_random_ammo_item_name()
    elif category == WeightedItemGroup.HEALTH:
        item = get_random_health_pickup_item_name(world)
    elif category == WeightedItemGroup.LIFE_FORCE:
        item = get_random_life_force_item_name(world)
    else:
        item = fallback_item

    if item:
        return item

    return fallback_item
    
def create_item_with_correct_classification(world: Turok2World, name: str) -> Turok2Item:
    """
    Creates an item by name. This is here in case we ever need to change the
    classification of any item based on the options the player chooses.
    """
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    
    # The torpedo launcher is not progressive if we aren't including it in logic
    if name == "Torpedo Launcher" and not world.options.guarantee_torpedo_launcher:
        classification = ItemClassification.useful

    return Turok2Item(
        name,
        classification,
        ITEM_NAME_TO_ID[name],
        world.player
    )
    
def force_local_items(
    world: Turok2World,
    itempool: list[Item],
    item_types: list[int],
    type_string: str,
    percentage: int) -> None:
    """
    Forces the percentage of items in the item pool of the given types to be placed in this world.
    """
    items = [
        item for item in itempool
        if ITEM_TABLE[item.name].get("type", None) in item_types
    ]
    world.random.shuffle(items)

    count = int(len(items) * percentage / 100)
    selected_items = items[:count]
    
    for item in selected_items:
        item.name += " (L)" # Hack to use the local version
        
    print(f"Forced {count} items of type {type_string} locally for Player {world.player}")

def force_local_weapons(world: Turok2World, itempool: list[Item]):
    """
    Forces the percentage of weapons to be placed in this world.
    """
    weapons = [
        item for item in itempool
        if ITEM_TABLE[item.name].get("type", -1) == ItemType.WEAPON.value
    ]
    
    count = int(len(weapons) * world.options.local_weapon_percentage / 100)
    for weapon in world.random.sample(weapons, k=count):
        world.options.local_items.value.add(weapon.name)
        
    print(f"Forced {count} {ItemType.WEAPON} items locally for Player {world.player}")

def force_early_weapon(world: Turok2World, itempool: list[Item]):
    """
    If force_early_weapon is on, force it as one of the local early items.
    """
    if not world.options.force_early_weapon or not world.options.randomize_weapons:
        return
        
    def is_valid_early_weapon(item_name: str) -> bool:
        data = ITEM_TABLE[item_name]
        groups = data.get("groups", [])
        return "Early Weapon" in groups 

    weapon_items = [
        item for item in itempool
        if is_valid_early_weapon(item.name)
    ]

    weapon = world.random.choices(weapon_items, k=1)[0]
    world.multiworld.local_early_items[world.player][weapon.name] = 1

    print(f"Early weapon {weapon.name} for Player {world.player}")

def compute_warp_distributions(world: Turok2World) -> dict[int, int]:
    """
    Randomly distributes the starting progressive warps across starting levels.
    If there are more starting warps than available, it will max it out.
    """
    if world.starting_levels:
        candidate_levels = [
            level for level in world.starting_levels
            if level not in world.excluded_levels
        ]
    else:
        candidate_levels = [1]

    # Set up the max number of warps a level can have
    level_caps = {}
    strength = max(world.options.progressive_warp_strength, 1)
    for data in ITEM_TABLE.values():
        if data.get("type") == ItemType.PROGRESSIVE_WARP.value:
            level = data.get("level", -1)
            count = data.get("count", 1)
            cap = math.ceil(count / strength)

            if level in candidate_levels:
                level_caps[level] = cap

    # Randomly distribute the progressive warps
    remaining = world.options.starting_progressive_warps
    warp_distributions = {level: 0 for level in candidate_levels}
    levels = list(candidate_levels)
    while remaining > 0 and levels:
        level = world.random.choice(levels)

        if warp_distributions[level] < level_caps.get(level, 0):
            warp_distributions[level] += 1
            remaining -= 1
        else:
            # This level is full, remove it from selection
            levels.remove(level)

    return warp_distributions

def create_progression_items(world: Turok2World, itempool: list[Item]) -> None:
    """
    Creates all progression items and adds them to the pool or precollects as necessary.
    """
    warp_distributions = compute_warp_distributions(world)
    for name, data in get_required_seed_items(world):
        count = data.get("count", 1)
        item_type = data.get("type")
        level = data.get("level", -1)
        precollect_count = 0

        # Handle level key packs and precollect necessary level keys
        if item_type == ItemType.LEVEL_KEY.value:
            if world.options.level_key_packs:
                count = 1
            if level in world.starting_levels:
                precollect_count = count

        # Assign the correct counts for progressive warps
        elif item_type == ItemType.PROGRESSIVE_WARP.value:
            strength = max(world.options.progressive_warp_strength, 1)
            count = math.ceil(count / strength)
            precollect_count = warp_distributions.get(level, 0)

        # Add the number of weapons to the pool based on the progressive ammo setting
        elif item_type == ItemType.WEAPON.value and not data.get("exclude_from_ammo_upgrades", False):
            count = world.options.progressive_weapon_ammo_upgrades

        # Start with talismans if necessary
        elif item_type == ItemType.TALISMAN.value:
            if (world.options.randomize_talismans == RandomizeTalismans.option_vanilla_start_with_if_level_excluded and
                level in world.excluded_levels):
                precollect_count = 1

        # Start with primagen keys if necessary
        elif item_type == ItemType.PRIMAGEN_KEY.value:
            if (world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_vanilla_start_with_if_level_excluded and
                level in world.excluded_levels):
                precollect_count = 1

        # Include the appropriate number of nuke parts for excluded levels
        # vanilla in pool: One in pool per excluded level
        # vanilla start with: Precollect one in pool per excluded level
        # else: Normal count (this would be the nuke hunt, where all are in the pool)
        elif item_type == ItemType.NUKE_PART.value:
            if world.options.nuke_behavior == NukeBehavior.option_vanilla_in_pool_if_level_excluded:
                count = len(world.excluded_levels)
            elif world.options.nuke_behavior == NukeBehavior.option_vanilla_start_with_if_level_excluded:
                count = len(world.excluded_levels)
                precollect_count = count

        # Precollect or append to pool as necessary
        for i in range(count):
            if i < precollect_count:
                world.multiworld.push_precollected(world.create_item(name))
            else:
                itempool.append(world.create_item(name))

def get_required_seed_items(world: Turok2World):
    """
    All items required to be in the seed.
    These are all weapons, and all inventory items, depending on settings
    """
    def include_item(name, data):
        is_level_excluded = data.get("level", -1) in world.excluded_levels

        # Talismans
        if data["type"] == ItemType.TALISMAN.value:
            in_pool = world.options.randomize_talismans == RandomizeTalismans.option_in_pool or \
                (is_level_excluded and 
                 world.options.randomize_talismans == RandomizeTalismans.option_vanilla_in_pool_if_level_excluded)
            start_with = is_level_excluded and \
                world.options.randomize_talismans == RandomizeTalismans.option_vanilla_start_with_if_level_excluded
            return in_pool or start_with
        
        # Primagen keys
        if data["type"] == ItemType.PRIMAGEN_KEY.value:
            needed_for_goal = (world.options.primagen_goal != PrimagenGoal.option_none and
                world.options.randomize_primagen_keys != RandomizePrimagenKeys.option_levels)
            in_pool = world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_in_pool or \
                (is_level_excluded and 
                 world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_vanilla_in_pool_if_level_excluded)
            start_with = is_level_excluded and \
                world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_vanilla_start_with_if_level_excluded
            return needed_for_goal and (in_pool or start_with)
        
        # Nuke
        if data["type"] == ItemType.NUKE_PART.value:
            return world.options.nuke_behavior == NukeBehavior.option_nuke_part_hunt or \
                world.options.nuke_behavior == NukeBehavior.option_vanilla_in_pool_if_level_excluded or \
                world.options.nuke_behavior == NukeBehavior.option_vanilla_start_with_if_level_excluded

        # Any other item with an excluded level should never be included
        if is_level_excluded:
            return False

        # Nuke item special cases
        if name == "Nuke":
            return world.options.nuke_behavior == NukeBehavior.option_weapon_pickup
        
        # Level keys
        if data["type"] == ItemType.LEVEL_KEY.value:
            return True
        
        # Eagle feathers
        if data["type"] == ItemType.EAGLE_FEATHER.value:
            return world.options.randomize_eagle_feathers
        
        # Mission items
        if data["type"] == ItemType.MISSION_ITEM.value:
            return world.options.randomize_mission_items
        
        # Weapons
        if data["type"] == ItemType.WEAPON.value:
            return world.options.randomize_weapons
        
        # Progressive warps
        if data["type"] == ItemType.PROGRESSIVE_WARP.value:
            return world.options.progressive_warps

        return False

    return [
        (name, data)
        for name, data in ITEM_TABLE.items()
        if include_item(name, data)
    ]

def handle_vanilla_locations(world: Turok2World) -> None:
    """
    Places certain vanilla progressive items in their correct locations.
    This is done so the tracker can more accurately tell what the next thing to do is.

    Currently done with feathers, talismans, and Primagen keys.
    """
    place_feathers = not world.options.randomize_eagle_feathers
    place_talismans = \
        (world.options.randomize_talismans == RandomizeTalismans.option_vanilla_in_pool_if_level_excluded or
        world.options.randomize_talismans == RandomizeTalismans.option_vanilla_start_with_if_level_excluded)
    place_primagen_keys = \
        (world.options.primagen_goal != PrimagenGoal.option_none and
        (world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_vanilla_in_pool_if_level_excluded or
        world.options.randomize_primagen_keys == RandomizePrimagenKeys.option_vanilla_start_with_if_level_excluded))

    if 1 not in world.excluded_levels:
        if place_primagen_keys:
            world.get_location("[1-4] Primagen Key Leap - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 1"))

    if 2 not in world.excluded_levels:
        if place_feathers:
            world.get_location("[2-8] Feather Ledge - Eagle Feather") \
                .place_locked_item(world.create_item("Level 2 Eagle Feather"))
        
        if place_talismans:
            world.get_location("[2-Talisman] Talisman - Leap of Faith") \
                .place_locked_item(world.create_item("Leap of Faith"))
            
        if place_primagen_keys:
            world.get_location("[2-8] Primagen Key River Leaps - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 2"))

    if 3 not in world.excluded_levels:
        if place_feathers:
            world.get_location("[3-6] Talisman Portal Wall - Eagle Feather") \
                .place_locked_item(world.create_item("Level 3 Eagle Feather"))
        
        if place_talismans:
            world.get_location("[3-Talisman] Talisman - Breath of Life") \
                .place_locked_item(world.create_item("Breath of Life"))
            
        if place_primagen_keys:
            world.get_location("[3-3] Primagen Key - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 3"))
            
    if 4 not in world.excluded_levels:
        if place_feathers:
            world.get_location("[4-4] Top - Eagle Feather") \
                .place_locked_item(world.create_item("Level 4 Eagle Feather"))
            
        if place_talismans:
            world.get_location("[4-Talisman] Talisman - Heart of Fire") \
                .place_locked_item(world.create_item("Heart of Fire"))
            
        if place_primagen_keys:
                world.get_location("[4-1] Primagen Key - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 4"))
            
    if 5 not in world.excluded_levels:
        if place_feathers:
            world.get_location("[5-6] Feather - Eagle Feather") \
                .place_locked_item(world.create_item("Level 5 Eagle Feather"))
            
        if place_talismans:
            world.get_location("[5-Talisman] Talisman - Whispers") \
                .place_locked_item(world.create_item("Whispers"))
            
        if place_primagen_keys:
            world.get_location("[5-10] Eye of Truth Path - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 5"))
    
    if 6 not in world.excluded_levels:          
        if place_feathers:
            world.get_location("[6-4c] Outer Path - Eagle Feather") \
                .place_locked_item(world.create_item("Level 6 Eagle Feather"))
            
        if place_talismans:
            world.get_location("[6-Talisman] Talisman - Eye of Truth") \
                .place_locked_item(world.create_item("Eye of Truth"))
            
        if place_primagen_keys:
            world.get_location("[6-Hub] Center - Primagen Key") \
                .place_locked_item(world.create_item("Primagen Key 6"))

def prepare_weights(pairs: Iterable[tuple]) -> tuple[list, list[int]]:
    """
    Returns a dictionary of value to weight given a list of pairs.
    """
    pairs = [(name, weight) for name, weight in pairs if weight > 0]
    if not pairs:
        return [], []

    names = [name for name, _ in pairs]
    weights = [weight for _, weight in pairs]
    return names, weights

def get_random_ammo_item_name() -> str:
    """
    Gets a random ammo pickup based on the weight settings.
    """
    return "Random Ammo Pack"
    
def get_random_health_pickup_item_name(world: Turok2World) -> str | None:
    """
    Gets a random health pickup based on the weight settings.
    """
    health_pickups = [
        ("Silver Health", world.options.silver_health_weight),
        ("Blue Health", world.options.blue_health_weight),
        ("Full Health", world.options.full_health_weight),
        ("Ultra Health", world.options.ultra_health_weight)
    ]
    
    names, weights = prepare_weights(health_pickups)
    if not names:
        return None
        
    return world.random.choices(names, weights=weights, k=1)[0]
        
def get_random_life_force_item_name(world: Turok2World) -> str | None:
    """
    Gets a random life force based on the weight settings.
    """
    life_forces = [
        ("Life Force 1", world.options.life_force_1_weight),
        ("Life Force 10", world.options.life_force_10_weight)
    ]

    names, weights = prepare_weights(life_forces)
    if not names:
        return None
    
    return world.random.choices(names, weights=weights, k=1)[0]

def generate_filler_items(world: Turok2World, needed_number_of_filler_items: int, itempool: list[Item]) -> None:
    """
    Generates the filler item pool based on the options.
    Traps are a percentage of the filler item pool.
    Uses vanilla-like distributions if applicable for item types and subtypes.
    """
    def generate_vanilla_non_trap_filler(
        world: Turok2World, 
        number_of_filler_slots: int) -> list[Item]:
        """
        Adds the vanilla items whose locations were randomized back into the pool.
        Will proportionately adjust the counts if traps now eat up too many slots.
        """
        # Filter relevant item types from the items the world collected
        valid_item_counts = {
            item_type: count
            for item_type, count in world.vanilla_item_counts.items()
            if ITEM_TYPE_TO_GROUP.get(item_type) in {
                WeightedItemGroup.HEALTH,
                WeightedItemGroup.AMMO,
                WeightedItemGroup.LIFE_FORCE
            }
            and count > 0
        }

        if not valid_item_counts or number_of_filler_slots <= 0:
            return []

        total_items = sum(valid_item_counts.values())

        # Compute how many items we need to add, scaling down if traps ate up too many slots
        if number_of_filler_slots >= total_items:
            scale = 1.0
        else:
            scale = number_of_filler_slots / total_items

        allocated = {}
        for item_type, count in valid_item_counts.items():
            allocated[item_type] = math.floor(count * scale)

        result = []

        # If vanilla, add the items to the pool as is
        if world.options.filler_distribution == FillerDistribution.option_vanilla:
            for item_type, count in allocated.items():
                item_name = ITEM_TYPE_TO_NAME[item_type]
                for _ in range(count):
                    result.append(world.create_item(item_name))

        # If using custom weights, get a random item based on the weight
        else:
            for item_type, count in allocated.items():
                group = ITEM_TYPE_TO_GROUP.get(item_type)
                for _ in range(count):
                    if group == WeightedItemGroup.AMMO:
                        item_name = get_random_ammo_item_name()
                    elif group == WeightedItemGroup.HEALTH:
                        item_name = get_random_health_pickup_item_name(world)
                    elif group == WeightedItemGroup.LIFE_FORCE:
                        item_name = get_random_life_force_item_name(world)
                    else:
                        continue

                    if item_name:
                        result.append(world.create_item(item_name))

        return result

    def get_random_trap_item_name(world: Turok2World) -> str | None:
        """
        Gets a random trap name to add to the item pool based on the weights.
        """
        traps = [
            ("Enemy Trap", world.options.enemy_trap_weight),
            ("Damage Trap", world.options.damage_trap_weight),
            ("Spam Trap", world.options.spam_trap_weight)
        ]
        traps = [(name, weight) for name, weight in traps if weight > 0]
        
        if not traps:
            return None
        
        names = [name for name, _ in traps]
        weights = [weight for _, weight in traps]
        return world.random.choices(names, weights=weights, k=1)[0]
    
    def generate_traps(world, count) -> list[str]:
        """
        Generates a list of trap names generated based on the weight option.
        """
        result = []
        for _ in range(count):
            trap = get_random_trap_item_name(world)
            if trap:
                result.append(world.create_item(trap))

        return result
    
    trap_percent = world.options.trap_percentage / 100
    trap_count = round(needed_number_of_filler_items * trap_percent)
    non_trap_count = needed_number_of_filler_items - trap_count

    # If we're using custom distribution, then get_random_filler_item_name handles this
    if world.options.filler_distribution != FillerDistribution.option_custom:
        itempool += generate_vanilla_non_trap_filler(world, non_trap_count)
    itempool += generate_traps(world, trap_count)

def create_all_items(world: Turok2World) -> None:
    """
    Creates all of the items that will go into the item pool.
    There must be exactly as many items as locations.
    """
    itempool: list[Item] = []
    
    # Populate the local items
    for name, data in ITEM_TABLE.items():
        if data.get("is_local"):
            world.options.local_items.value.add(name)

    # Create all progression items
    create_progression_items(world, itempool)

    def compute_needed_number_of_filler_items(world: Turok2World, itempool: list[Item]) -> int:
        """Gets the number of locations to fill out."""
        number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
        number_of_items = len(itempool)
        return max(0, number_of_unfilled_locations - number_of_items)
    
    # Handle vanilla locations, which places locked items or gives them to you if the level is excluded
    # Do this before filler so we don't overfill with items
    handle_vanilla_locations(world)

    # Fill the world with computed filler items
    needed_number_of_filler_items = compute_needed_number_of_filler_items(world, itempool)
    generate_filler_items(world, needed_number_of_filler_items, itempool)
    
    # Fill out the rest of the pool (calls get_random_filler_item_name) and force some to be local
    needed_number_of_filler_items = compute_needed_number_of_filler_items(world, itempool)
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    force_local_items(
        world, 
        itempool, 
        [ItemType.SILVER_HEALTH.value, ItemType.BLUE_HEALTH.value, ItemType.FULL_HEALTH.value, ItemType.ULTRA_HEALTH.value],
        "Health",
        world.options.local_health_percentage)
    force_local_items(world, itempool, [ItemType.AMMO.value], "Ammo", world.options.local_ammo_percentage)
    force_local_weapons(world, itempool)
    force_early_weapon(world, itempool)
    
    world.multiworld.itempool += itempool

    #debug_print_summary(world, itempool)

def map_ap_item_to_game(ap_item_id: str) -> tuple[int, int]:
    """
    Maps the given AP item id to the game so that the appropriate message
    type and actor id can be sent.
    
    If the item is not mapped returns NONE so the game will ignore the item.
    """
    _, item = ID_TO_ITEM.get(ap_item_id, (None, None))
    
    if not item:
        print(f"Unknown AP item id {ap_item_id}")
        return APMessageType.AP_MSGTYPE_NONE.value, 0
        
    return item["msg_type"], item.get("actor_id", 0)

def debug_print_summary(world: Turok2World, itempool: list[Item]) -> None:
    """
    Print out the item pool by type for debugging.
    """
    print(f"Vanilla filler items found for player {world.player}:")
    for item, count in world.vanilla_item_counts.items():
        print(f"{item.name}: {count}")

    print(f"Item pool summary for player {world.player}:")
    item_counts: dict[str, int] = Counter()
    total_items = len(itempool)

    for item in itempool:
        item_counts[item] += 1

    for item, count in item_counts.items():
        percentage = (count / total_items) * 100
        print(f"{item.name}: {count} ({percentage:.1f}%)")
 
from __future__ import annotations
import math
from .item_table import *
from typing import TYPE_CHECKING, Counter
from BaseClasses import Item
from .options import NukeBehavior, PrimagenGoal, PrimagenKeys

if TYPE_CHECKING:
    from . import Turok2World
    
TRAPS_BY_CATEGORY = {}

class Turok2Item(Item):
    game = "Turok 2"

def get_item_name_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}

    for name, data in ITEM_TABLE.items():
        for group in data.get("groups", []):
            groups.setdefault(group, set()).add(name)

    return groups

def get_required_seed_items(world: Turok2World):
    """
    All items required to be in the seed.
    These are all weapons, and all inventory items, depending on settings
    """
    def include_item(name, data):
        # Nuke item special cases
        if name == "Nuke":
            return world.options.nuke_behavior == NukeBehavior.option_weapon_pickup
        
        if data["type"] == ItemType.NUKE_PART.value:
            return world.options.nuke_behavior == NukeBehavior.option_nuke_part_hunt
        
        # Level keys
        if data["type"] == ItemType.LEVEL_KEY.value:
            return world.options.include_level_key_locations
        
        # Eagle feathers
        if data["type"] == ItemType.EAGLE_FEATHER.value:
            return world.options.include_eagle_feather_locations
        
        # Talismans
        if data["type"] == ItemType.TALISMAN.value:
            return world.options.include_talisman_locations
        
        # Mission items
        if data["type"] == ItemType.MISSION_ITEM.value:
            return world.options.include_mission_item_locations
        
        # Primagen keys
        if data["type"] == ItemType.PRIMAGEN_KEY.value:
            return (world.options.primagen_goal != PrimagenGoal.option_none and
                world.options.primagen_keys == PrimagenKeys.option_in_pool)
        
        # Weapons
        if data["type"] == ItemType.WEAPON.value:
            return world.options.weapon_sanity
        
        # Ammo
        if data["type"] == ItemType.AMMO.value:
            return world.options.ammo_sanity
        
        # Progressive warps
        if data["type"] == ItemType.PROGRESSIVE_WARP.value:
            return world.options.progressive_warps

        return False

    return [
        (name, data)
        for name, data in ITEM_TABLE.items()
        if include_item(name, data)
    ]
    
def get_random_filler_item_name(world: Turok2World) -> str:
    """
    world.py will use this to generate filler items.
    This will generate a random filler by the item weights set in the options.
    """
    categories = [
        (ItemType.SILVER_HEALTH.value, world.options.junk_item_pool_health_weight),
        (ItemType.AMMO.value, world.options.junk_item_pool_ammo_weight),
        (ItemType.LIFE_FORCE_1.value, world.options.junk_item_pool_life_force_weight),
        (ItemType.TRAP.value, world.options.junk_item_pool_trap_weight)
    ]
    category_names = [name for name, _ in categories]
    category_weights = [weight for _, weight in categories]
    
    # Pick a category
    chosen_category = world.random.choices(category_names, weights=category_weights, k=1)[0]

    # Pick an item from that category
    if chosen_category == ItemType.SILVER_HEALTH.value:
        return get_random_health_pickup_item_name(world)
    elif chosen_category == ItemType.AMMO.value:
        return "Random Ammo Pack"
    elif chosen_category == ItemType.TRAP.value:
        return get_random_trap_item_name(world)
    else:
        # Acts as the fallback
        return get_random_life_force_item_name(world)
    
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

def get_random_trap_item_name(world: Turok2World) -> str | None:
    """
    Gets a random trap name to add to the item pool.
    First, chooses the category based on the options.
    Next, chooses the specific item by weighing the different game models.
    """
    # Choose the trap category
    categories = [
        (TrapType.ENEMY.value, world.options.enemy_trap_weight),
        (TrapType.DAMAGE.value, world.options.damage_trap_weight),
        (TrapType.SPAM.value, world.options.spam_trap_weight)
    ]
    categories = [(name, weight) for name, weight in categories if weight > 0]
    
    if not categories:
        return None
    
    category_names = [name for name, _ in categories]
    category_weights = [weight for _, weight in categories]
    category = world.random.choices(category_names, weights=category_weights, k=1)[0]
    
    # Choose the trap item (the model that will appear in the game)
    items = TRAPS_BY_CATEGORY[category]
    if not items:
        return None
    
    names = [name for name, _ in items]
    weights = [data.get("weight", 1) for _, data in items]
    
    return world.random.choices(names, weights=weights, k=1)[0]
    
def get_random_life_force_item_name(world: Turok2World) -> str:
    """
    Gets a random life force based on the weight settings.
    """
    life_forces = [
        ("Life Force 1", world.options.life_force_1_weight),
        ("Life Force 10", world.options.life_force_10_weight)
    ]
    names = [name for name, _ in life_forces]
    weights = [weight for _, weight in life_forces]
    return world.random.choices(names, weights=weights, k=1)[0]
    
def get_random_health_pickup_item_name(world: Turok2World) -> str:
    """
    Gets a random health pickup based on the weight settings.
    """
    health_pickups = [
        ("Silver Health", world.options.silver_health_weight),
        ("Blue Health", world.options.blue_health_weight),
        ("Full Health", world.options.full_health_weight),
        ("Ultra Health", world.options.ultra_health_weight)
    ]
    names = [name for name, _ in health_pickups]
    weights = [weight for _, weight in health_pickups]
    return world.random.choices(names, weights=weights, k=1)[0]
    
def force_local_items(
    world: Turok2World,
    itempool: list[Item],
    item_types: list[int],
    type_string: str,
    percentage: int):
    """
    Forces the percentage of items in the item pool of the given types to be placed in this world.
    """
    items = [
        item for item in itempool
        if ITEM_TABLE[item.name].get("type", -1) in item_types
    ]
    count = int(len(items) * percentage / 100)
    selected_items = items[:count]
    
    for item in selected_items:
        item.name += " (L)" # Uses the local version, should change back in post_fill
        
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
    if not world.options.force_early_weapon or not world.options.weapon_sanity:
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

def place_locked_items(world: Turok2World) -> None:
    """
    Places certain vanilla progressive items in their correct locations.
    This is done so the tracker can more accurately tell what the next thing to do is.

    Currently done with level keys, feathers, talismans, and Primagen keys.
    """
    if not world.options.include_level_key_locations:
        world.get_location("[1-2] Hall - Level Key") \
            .place_locked_item(world.create_item("Level 2 Key"))
        world.get_location("[1-2] Upper Water - Level Key") \
            .place_locked_item(world.create_item("Level 2 Key"))
        world.get_location("[1-8] After Gate - Level Key up Ladder") \
            .place_locked_item(world.create_item("Level 2 Key"))

        world.get_location("[1-4] Ground - Level Key") \
            .place_locked_item(world.create_item("Level 3 Key"))
        world.get_location("[1-9] Below Oblivion - Level Key up Ladder") \
            .place_locked_item(world.create_item("Level 3 Key"))
        world.get_location("[1-9] Fountain Building F2 - Level Key in Center") \
            .place_locked_item(world.create_item("Level 3 Key"))

        world.get_location("[2-3] Level Key Loop - Level Key") \
            .place_locked_item(world.create_item("Level 4 Key"))
        world.get_location("[2-7] Fountain Path - Level Key") \
            .place_locked_item(world.create_item("Level 4 Key"))
        world.get_location("[2-8] Level Key Path - Level Key") \
            .place_locked_item(world.create_item("Level 4 Key"))

        world.get_location("[3-1] Across Double Logs - Level Key") \
            .place_locked_item(world.create_item("Level 5 Key"))
        world.get_location("[3-2] After Marsh Path - Level Key") \
            .place_locked_item(world.create_item("Level 5 Key"))
        world.get_location("[3-8] Raptor Rooms - Level Key") \
            .place_locked_item(world.create_item("Level 5 Key"))

        world.get_location("[4-3] Level Key Trap - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))
        world.get_location("[4-8] Level Key Trap - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))
        world.get_location("[4-6] Level Key Trap - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))
        
        world.get_location("[5-2] Level Key - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))
        world.get_location("[5-5] Level Key - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))
        world.get_location("[5-7] After Main Generator - Level Key") \
            .place_locked_item(world.create_item("Level 6 Key"))

    if not world.options.include_eagle_feather_locations:
        world.get_location("[2-8] Feather Ledge - Eagle Feather") \
            .place_locked_item(world.create_item("Level 2 Eagle Feather"))
        world.get_location("[3-6] Talisman Portal Wall - Eagle Feather") \
            .place_locked_item(world.create_item("Level 3 Eagle Feather"))
        world.get_location("[4-4] Top - Eagle Feather") \
            .place_locked_item(world.create_item("Level 4 Eagle Feather"))
        world.get_location("[5-6] Feather - Eagle Feather") \
            .place_locked_item(world.create_item("Level 5 Eagle Feather"))
        world.get_location("[6-4c] Outer Path - Eagle Feather") \
            .place_locked_item(world.create_item("Level 6 Eagle Feather"))
        
    if not world.options.include_talisman_locations:
        world.get_location("[2-Talisman] Talisman - Leap of Faith").place_locked_item(world.create_item("Leap of Faith"))
        world.get_location("[3-Talisman] Talisman - Breath of Life").place_locked_item(world.create_item("Breath of Life"))
        world.get_location("[4-Talisman] Talisman - Heart of Fire").place_locked_item(world.create_item("Heart of Fire"))
        world.get_location("[5-Talisman] Talisman - Whispers").place_locked_item(world.create_item("Whispers"))
        world.get_location("[6-Talisman] Talisman - Eye of Truth").place_locked_item(world.create_item("Eye of Truth"))

    if (world.options.primagen_goal != PrimagenGoal.option_none and
        world.options.primagen_keys == PrimagenKeys.option_vanilla):
        world.get_location("[1-4] Primagen Key Leap - Primagen Key").place_locked_item(world.create_item("Primagen Key 1"))
        world.get_location("[2-8] Primagen Key River Leaps - Primagen Key").place_locked_item(world.create_item("Primagen Key 2"))
        world.get_location("[3-3] Primagen Key - Primagen Key").place_locked_item(world.create_item("Primagen Key 3"))
        world.get_location("[4-1] Primagen Key - Primagen Key").place_locked_item(world.create_item("Primagen Key 4"))
        world.get_location("[5-10] Eye of Truth Path - Primagen Key").place_locked_item(world.create_item("Primagen Key 5"))
        world.get_location("[6-Hub] Center - Primagen Key").place_locked_item(world.create_item("Primagen Key 6"))

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
    
    # Populate the traps dictionary
    for name, data in TRAPS.items():
        trap_type = data["trap_type"]
        if trap_type is None:
            continue
        TRAPS_BY_CATEGORY.setdefault(trap_type, []).append((name, data))

    # Add all the required items to the pool (weapons and inventory items)
    for name, data in get_required_seed_items(world):
        count = data.get("count", 1)
        if data.get("type") == ItemType.PROGRESSIVE_WARP.value:
            strength = max(world.options.progressive_warp_strength, 1)
            count = math.ceil(count / strength)
        for i in range(count):
            if name == "Progressive Warp L1" and world.options.starting_progressive_warps > i:
                world.multiworld.push_precollected(world.create_item(name))
            else:
                itempool.append(world.create_item(name))
         
    # Fill the world with fillers
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    number_of_items = len(itempool)
    needed_number_of_filler_items = max(0, number_of_unfilled_locations - number_of_items)
    
    # Fill out the rest of the pool (calls get_random_filler_item_name) and force some to be local
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    force_local_items(
        world, 
        itempool, 
        [ItemType.SILVER_HEALTH.value, ItemType.BLUE_HEALTH.value, ItemType.FULL_HEALTH.value, ItemType.ULTRA_HEALTH.value],
        "Health",
        world.options.local_health_percentage)
    force_local_items(world, itempool, [ItemType.AMMO], "Ammo", world.options.local_ammo_percentage)
    force_local_weapons(world, itempool)
    
    # Force the early weapon, if the setting is on
    force_early_weapon(world, itempool)

    # Place locked locations, based on whether certain items are vanilla
    place_locked_items(world)
    
    world.multiworld.itempool += itempool
    
    """
    Print out the item pool by type for debugging
    Leave this commented out in released versions
    """
    
    item_counts: dict[str, int] = Counter()
    total_items = len(itempool)

    for item in itempool:
        item_counts[item] += 1

    print(f"Item pool summary for player {world.player}:")
    for item, count in item_counts.items():
        percentage = (count / total_items) * 100
        print(f"{item.name}: {count} ({percentage:.1f}%)")
    
    
def map_ap_item_to_game(ap_item_id) -> tuple[int, int]:
    """
    Maps the given AP item id to the game so that the appropriate message
    type and actor id can be sent.
    
    If the item is not mapped returns NONE so the game will ignore the item.
    """
    name, item = ID_TO_ITEM.get(ap_item_id, (None, None))
    
    if not item:
        print(f"Unknown AP item id {ap_item_id}")
        return APMessageType.AP_MSGTYPE_NONE.value, 0
        
    return item["msg_type"], item.get("actor_id", 0)
 
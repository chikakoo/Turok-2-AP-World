from __future__ import annotations
from .item_table import *
from collections import Counter
from typing import TYPE_CHECKING, Callable
from BaseClasses import Item, ItemClassification
from .client.ap_memory_constants import APMessageType
from .options import NukeBehavior, Goal, PrimagenLair

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
        if name == "Nuke Part":
            return world.options.nuke_behavior == NukeBehavior.option_nuke_part_hunt
        
        # Mission items depend on the setting (they are also inventory items, so do this first)
        if data["type"] == ItemType.MISSION_ITEM.value:
            return world.options.include_mission_item_locations
        
        # Inventory items
        if data["type"] == ItemType.PRIMAGEN_KEY.value:
            return (world.options.goal == Goal.option_primagen and 
                world.options.primagen_lair != PrimagenLair.option_keys_vanilla)
        
        if data["msg_type"] == APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value:
            return True
        
        # Other weapons depend on whether they are shuffled
        if data["type"] == ItemType.WEAPON.value:
            return world.options.include_weapon_and_ammo_locations

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
        (ItemType.HEALTH.value, world.options.junk_item_pool_health_weight),
        (ItemType.AMMO.value, world.options.junk_item_pool_ammo_weight),
        (ItemType.LIFE_FORCE.value, world.options.junk_item_pool_life_force_weight),
        (ItemType.TRAP.value, world.options.junk_item_pool_trap_weight)
    ]
    category_names = [name for name, _ in categories]
    category_weights = [weight for _, weight in categories]
    
    # Pick a category
    chosen_category = world.random.choices(category_names, weights=category_weights, k=1)[0]

    # Pick an item from that category
    if chosen_category == ItemType.HEALTH.value:
        return get_random_health_pickup_item_name(world)
    elif chosen_category == ItemType.AMMO.value:
        return get_random_ammo_pickup_item_name(world)
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
    
    # TODO: Change this when level 4 exists
    if name == "Torpedo Launcher":
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
    Gets a random life force.
    """
    names = list(LIFE_FORCES.keys())
    weights = [data.get("weight", 1) for data in LIFE_FORCES.values()]
    return world.random.choices(names, weights=weights, k=1)[0]
    
def get_random_health_pickup_item_name(world: Turok2World) -> str:
    """
    Gets a random health pickup.
    """
    names = list(HEALTH_PICKUPS.keys())
    weights = [data.get("weight", 1) for data in HEALTH_PICKUPS.values()]
    return world.random.choices(names, weights=weights, k=1)[0]
    
def get_random_ammo_pickup_item_name(world: Turok2World) -> str:
    """
    Gets a random ammo pickup. There's currently only one, so just return it.
    """
    return "Random Ammo Pack"
    
def add_items_to_itempool(
    world: Turok2World,
    itempool: list[Item],
    number_of_unfilled_locations: int,
    percentage_sum: int,
    item_fill_percent: int,
    get_item_name_function: Callable[[Turok2World], str | None]):
    """
    Adds items to the item pool based on the percentage sum, and the percent given.
    If the sum if > 100, treat the percent as a ratio of the given sum. 
    Otherwise, use it as the percent.
    """
    if item_fill_percent <= 0:
        return
    
    if percentage_sum > 100:
        ratio = item_fill_percent / percentage_sum
    else:
        ratio = item_fill_percent / 100.0
    
    # Any rounding error will be lower than expected, which is okay
    count = int(number_of_unfilled_locations * ratio)
    
    for _ in range(count):
        name = get_item_name_function(world)
        if name:
            itempool.append(world.create_item(name))
    
def force_local_items(world: Turok2World, itempool: list[Item], item_type: int, percentage: int):
    """
    Forces the percentage of items in the item pool of the given type to be placed in this world.
    """
    items = [
        item for item in itempool
        if ITEM_TABLE[item.name].get("type", -1) == item_type
    ]
    count = int(len(items) * percentage / 100)
    selected_items = items[:count]
    
    for item in selected_items:
        item.name += " (L)" # Uses the local version, should change back in post_fill
        
    print(f"Forced {count} {ItemType(item_type)} items locally for Player {world.player}")

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


def force_early_weapons(world: Turok2World, itempool: list[Item]):
    """
    If we are randomizing weapons, force 3 early in the seed.
    If force_early_weapon is on, force it in the first map locally.
    """
    if not world.options.include_weapon_and_ammo_locations:
        return
        
    def is_valid_early_weapon(item_name: str) -> bool:
        data = ITEM_TABLE[item_name]
        groups = data.get("groups", [])
        return "Early Weapon" in groups 

    weapon_items = [
        item for item in itempool
        if is_valid_early_weapon(item.name)
    ]

    for index, weapon in enumerate(world.random.sample(weapon_items, k=3)):
        if index == 0 and world.options.force_early_weapon:
            starting_locations = [
                loc for loc in world.multiworld.get_unfilled_locations(world.player)
                if loc.parent_region.name == world.origin_region_name
                and loc.address is not None
                and not loc.locked
                and loc.item is None
            ]
            location = world.random.choice(starting_locations)
            location.place_locked_item(weapon)
            itempool.remove(weapon)
        else:
            world.multiworld.early_items[world.player][weapon.name] = 1

        print(f"Early weapon {weapon.name} for Player {world.player}")

def force_early_key_items(world: Turok2World):
    """
    Forces the Beacon Power Cells early, since you will always want them early.
    """
    world.multiworld.early_items[world.player]["Beacon Power Cell"] = 3

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
        for _ in range(data.get("count", 1)):
            itempool.append(world.create_item(name))
         
    # Fill the world with fillers
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    number_of_items = len(itempool)
    needed_number_of_filler_items = max(0, number_of_unfilled_locations - number_of_items)
    
    percentage_sum_of_minimum_items = (
        world.options.minimum_health_percent + 
        world.options.minimum_ammo_percent + 
        world.options.minimum_life_force_percent)
        
    add_items_to_itempool(
        world,
        itempool,
        needed_number_of_filler_items,
        percentage_sum_of_minimum_items,
        world.options.minimum_health_percent,
        get_random_health_pickup_item_name)
    add_items_to_itempool(
        world,
        itempool,
        needed_number_of_filler_items,
        percentage_sum_of_minimum_items,
        world.options.minimum_ammo_percent,
        get_random_ammo_pickup_item_name)
    add_items_to_itempool(
        world,
        itempool,
        needed_number_of_filler_items,
        percentage_sum_of_minimum_items,
        world.options.minimum_life_force_percent,
        get_random_life_force_item_name)
    
    # Recompute the number of filler items needed
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    number_of_items = len(itempool)
    needed_number_of_filler_items = max(0, number_of_unfilled_locations - number_of_items)
    
    # Fill out the rest of the pool (calls get_random_filler_item_name) and force some to be local
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    force_local_items(world, itempool, ItemType.HEALTH.value, world.options.local_health_percentage)
    force_local_items(world, itempool, ItemType.AMMO.value, world.options.local_ammo_percentage)
    force_local_weapons(world, itempool)
    
    # Force 3 early weapons, and make one in the first area if the setting ison
    force_early_weapons(world, itempool)
    force_early_key_items(world)
    
    world.multiworld.itempool += itempool
    
    """
    Print out the item pool by type for debugging
    Leave this commented out in released versions
    """
    
    type_counts: dict[ItemType, int] = Counter()
    total_items = len(itempool)

    for item in itempool:
        item_type = ItemType(ITEM_TABLE[item.name]["type"])
        type_counts[item_type] += 1

    print(f"Item pool summary for player {world.player}:")
    for item_type, count in type_counts.items():
        percentage = (count / total_items) * 100
        print(f"{item_type.name}: {count} ({percentage:.1f}%)")
    
    
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
 
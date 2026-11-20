from enum import Enum
from BaseClasses import  ItemClassification
from .client.ap_memory_constants import APMessageType

class ItemType(Enum):
    """Types used to filter the item table."""
    LIFE_FORCE_1 = 0
    LIFE_FORCE_10 = 1
    BLUE_HEALTH = 2
    SILVER_HEALTH = 3
    FULL_HEALTH = 4
    ULTRA_HEALTH = 5
    AMMO = 6
    LEVEL_KEY = 7
    PRIMAGEN_KEY = 8
    EAGLE_FEATHER = 9
    TALISMAN = 10
    NUKE_PART = 11
    MISSION_ITEM = 12
    WEAPON = 13
    TRAP = 14
    PROGRESSIVE_WARP = 15

    # Technically not items, but will still be used in the location table the same way
    SWITCH = 16
    MISSION_OBJECTIVE = 17
    ENEMY_SOUL = 18
    ENEMY_SOUL_KILL = 19
    LEVEL_COMPLETED = 20
    EVENT = 99 # Will not provide a real check - used for tracking purposes
    
class EnemyType(Enum):
    """Types used to identify enemies (used for the AP kill check id)."""
    RAPTOID = 1
    ENDTRAIL = 2
    COMPY = 3
    RAPTOR = 4

    LEAPER = 5
    SPIDER_HATCHLING = 6
    DEADMAN = 7
    LORD_OF_THE_DEAD = 8
    SISTER_OF_DESPAIR = 9

    WAR_CLUB = 10
    GUNNER = 11
    JUGGERNAUT = 12
    CAVE_WORM = 13
    WASP = 14

    BLIND_SENTINEL = 15
    GUARDIAN = 16
    NALA = 17
    CAVE_SPIDER = 18
    FIREBORN = 19

    DRONE = 20
    WORKER = 21
    MITE = 22
    SOLDIER = 23

    BIO_BOT = 24
    TROOPER = 25
    ELITE_GUARD = 26

    FLESH_SENTINEL = 27
    DEATH_GUARD = 28
    LORD_OF_THE_FLESH = 29

class WeightedItemGroup(Enum):
    """Types used to identify item groups that are related so weights can be applied."""
    NONE = 0
    LIFE_FORCE = 1
    HEALTH = 2
    AMMO = 3

ITEM_TYPE_TO_GROUP = {
    ItemType.LIFE_FORCE_1: WeightedItemGroup.LIFE_FORCE,
    ItemType.LIFE_FORCE_10: WeightedItemGroup.LIFE_FORCE,

    ItemType.SILVER_HEALTH: WeightedItemGroup.HEALTH,
    ItemType.BLUE_HEALTH: WeightedItemGroup.HEALTH,
    ItemType.FULL_HEALTH: WeightedItemGroup.HEALTH,
    ItemType.ULTRA_HEALTH: WeightedItemGroup.HEALTH,

    ItemType.AMMO: WeightedItemGroup.AMMO
}

ITEM_TYPE_TO_NAME = {
    ItemType.LIFE_FORCE_1: "Life Force 1",
    ItemType.LIFE_FORCE_10: "Life Force 10",

    ItemType.SILVER_HEALTH: "Silver Health",
    ItemType.BLUE_HEALTH: "Blue Health",
    ItemType.FULL_HEALTH: "Full Health",
    ItemType.ULTRA_HEALTH: "Ultra Health",

    ItemType.AMMO: "Random Ammo Pack"
}

class TrapType(Enum):
    """
    Trap types, so we can choose traps based on their weights.
    """
    ENEMY = 0
    DAMAGE = 1
    SPAM = 2
    
ITEM_TABLE = {
    # Pickups (including local health)
    "Life Force 1": {
        "id": 100000, 
        "actor_id": 1705,
        "type": ItemType.LIFE_FORCE_1.value,
        "weighted_group": WeightedItemGroup.LIFE_FORCE,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Life Force 10": {
        "id": 100001, 
        "actor_id": 1706, 
        "type": ItemType.LIFE_FORCE_10.value,
        "weighted_group": WeightedItemGroup.LIFE_FORCE,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    
    "Silver Health": {
        "id": 100002,
        "actor_id": 1701,
        "type": ItemType.SILVER_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Blue Health": {
        "id": 100003,
        "actor_id": 1702,
        "type": ItemType.BLUE_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Full Health": {
        "id": 100004,
        "actor_id": 1703,
        "type": ItemType.FULL_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Ultra Health": {
        "id": 100005,
        "actor_id": 1704,
        "type": ItemType.ULTRA_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Silver Health (L)": {
        "id": 100102,
        "actor_id": 1701,
        "type": ItemType.SILVER_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Blue Health (L)": {
        "id": 100103,
        "actor_id": 1702,
        "type": ItemType.BLUE_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Full Health (L)": {
        "id": 100104,
        "actor_id": 1703,
        "type": ItemType.FULL_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Ultra Health (L)": {
        "id": 100105,
        "actor_id": 1704,
        "type": ItemType.ULTRA_HEALTH.value,
        "weighted_group": WeightedItemGroup.HEALTH,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    
    # Ammo (and local ammo)
    "Random Ammo Pack": {
        "id": 400000,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
        "weighted_group": WeightedItemGroup.AMMO,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_AMMO.value,
        "class": ItemClassification.filler
    },
    "Random Ammo Pack (L)": {
        "id": 400100,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
        "weighted_group": WeightedItemGroup.AMMO,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_AMMO.value,
        "class": ItemClassification.filler,
        "is_local": True
    },

    # Inventory items
    "Level 1 Key": {
        "id": 200000,
        "actor_id": 4300,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 1
    },
    "Level 2 Key": {
        "id": 200001,
        "actor_id": 4310,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 2
    },
    "Level 3 Key": {
        "id": 200002,
        "actor_id": 4320,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 3
    },
    "Level 4 Key": {
        "id": 200003,
        "actor_id": 4330,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 4
    },
    "Level 5 Key": {
        "id": 200004,
        "actor_id": 4340,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 5
    },
    "Level 6 Key": {
        "id": 200005,
        "actor_id": 4350,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 6,
        "level": 6
    },
    
    "Primagen Key 1": {
        "id": 200006,
        "actor_id": 4360,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 2": {
        "id": 200007,
        "actor_id": 4361,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 2,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 3": {
        "id": 200008,
        "actor_id": 4362,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 3,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 4": {
        "id": 200009,
        "actor_id": 4363,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 4,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 5": {
        "id": 200010,
        "actor_id": 4364,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 5,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 6": {
        "id": 200011,
        "actor_id": 4365,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "level": 6,
        "groups": ["Primagen Key"]
    },
    
    "Level 2 Eagle Feather": {
        "id": 200012,
        "actor_id": 4402,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 2
    },
    "Level 3 Eagle Feather": {
        "id": 200013,
        "actor_id": 4400,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 3
    },
    "Level 4 Eagle Feather": {
        "id": 200014,
        "actor_id": 4404,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 4
    },
    "Level 5 Eagle Feather": {
        "id": 200015,
        "actor_id": 4403,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 5
    },
    "Level 6 Eagle Feather": {
        "id": 200016,
        "actor_id": 4401,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 6
    },
    
    "Leap of Faith": {
        "id": 200017,
        "actor_id": 4382,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 2
    },
    "Breath of Life": {
        "id": 200018,
        "actor_id": 4380,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 3
    },
    "Heart of Fire": {
        "id": 200019,
        "actor_id": 4384,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 4
    },
    "Whispers": {
        "id": 200020,
        "actor_id": 4383,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 5
    },
    "Eye of Truth": {
        "id": 200021,
        "actor_id": 4381,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1,
        "level": 6
    },
    
    "Nuke Part": {
        "id": 200022,
        "actor_id": 4500,
        "type": ItemType.NUKE_PART.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.useful,
        "count": 6
    },
    
    # Mission Items
    "Power Cell": {
        "id": 200100,
        "actor_id": 4200,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 1
    },
    "Gate Key": {
        "id": 200200,
        "actor_id": 4030,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 2,
        "level": 2
    },
    "Graveyard Key": {
        "id": 200201,
        "actor_id": 4025,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 2,
        "level": 2
    },
    "L3 Satchel Charge": {
        "id": 200300,
        "actor_id": 4100,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 3
    },
    "Cave Door Key": {
        "id": 200400,
        "actor_id": 4020,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 7,
        "level": 4
    },
    "L4 Satchel Charge": {
        "id": 200401,
        "actor_id": 4111,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3,
        "level": 4
    },
    "L5 Satchel Charge": {
        "id": 200500,
        "actor_id": 4110,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 4,
        "level": 5
    },
    "Ion Capacitor": {
        "id": 200600,
        "actor_id": 4231,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 16,
        "level": 6
    },
    "Blue Laser Cell": {
        "id": 200601,
        "actor_id": 4230,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 4,
        "level": 6
    },
    "Red Laser Cell": {
        "id": 200602,
        "actor_id": 4229,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 4,
        "level": 6
    },

    # Progressive Warps
    "Progressive Warp L1": {
        "id": 201001,
        "actor_id": 201001,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 9,
        "level": 1
    },
    "Progressive Warp L2": {
        "id": 201002,
        "actor_id": 201002,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 11,
        "level": 2
    },
    "Progressive Warp L3": {
        "id": 201003,
        "actor_id": 201003,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 8,
        "level": 3
    },
    "Progressive Warp L4": {
        "id": 201004,
        "actor_id": 201004,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 10,
        "level": 4
    },
    "Progressive Warp L5": {
        "id": 201005,
        "actor_id": 201005,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 10,
        "level": 5
    },
    "Progressive Warp L6": {
        "id": 201006,
        "actor_id": 201006,
        "type": ItemType.PROGRESSIVE_WARP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 13,
        "level": 6
    },
    
    # Weapons
    "War Blade": {
        "id": 300000,
        "actor_id": 2001,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "exclude_from_ammo_upgrades": True,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Tek Bow": {
        "id": 300001,
        "actor_id": 2002,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon", "Sniper Weapon"]
    },
    "Pistol": {
        "id": 300002,
        "actor_id": 2004,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Mag 60": {
        "id": 300003,
        "actor_id": 2005,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Tranquilizer Gun": {
        "id": 300004,
        "actor_id": 2006,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Charge Dart Rifle": {
        "id": 300005,
        "actor_id": 2007,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Shotgun": {
        "id": 300006,
        "actor_id": 2008,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Shredder": {
        "id": 300007,
        "actor_id": 2009,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Plasma Rifle": {
        "id": 300008,
        "actor_id": 2010,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon", "Sniper Weapon"]
    },
    "Firestorm Cannon": {
        "id": 300009,
        "actor_id": 2011,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Sunfire Pod": {
        "id": 300010,
        "actor_id": 2012,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Cerebral Bore": {
        "id": 300011,
        "actor_id": 2014,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "P.F.M. Layer": {
        "id": 300012,
        "actor_id": 2015,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Grenade Launcher": {
        "id": 300013,
        "actor_id": 2016,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Scorpion Launcher": {
        "id": 300014,
        "actor_id": 2017,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Flame Thrower": {
        "id": 300015,
        "actor_id": 2110,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "groups": ["Barrier Weapon"]
    },
    "Razor Wind": {
        "id": 300016,
        "actor_id": 2111,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression,
        "count": 1,
        "exclude_from_ammo_upgrades": True,
        "groups": ["Barrier Weapon"]
    },
    "Harpoon Gun": {
        "id": 300017,
        "actor_id": 2100,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": []
    },
    "Torpedo Launcher": {
        "id": 300018,
        "actor_id": 2101,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.progression, # Needed in Level 4
        "count": 1,
        "groups": []
    },
    "Nuke": {
        "id": 300019,
        "actor_id": 2112,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "exclude_from_ammo_upgrades": True,
        "groups": []
    },

    # Enemy Souls
    "Raptoid Soul": {
        "id": 400200,
        "actor_id": 400200,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Endtrail Soul": {
        "id": 400201,
        "actor_id": 400201,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Compy Soul": {
        "id": 405000,
        "actor_id": 405000,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Raptor Soul": {
        "id": 400300,
        "actor_id": 400300,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Leaper Soul": {
        "id": 401000,
        "actor_id": 401000,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Spider Hatchling Soul": {
        "id": 400502,
        "actor_id": 400502,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Deadman Soul": {
        "id": 400800,
        "actor_id": 400800,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Lord of the Dead Soul": {
        "id": 400803,
        "actor_id": 400803,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Sister of Despair Soul": {
        "id": 400804,
        "actor_id": 400804,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "War Club Soul": {
        "id": 400600,
        "actor_id": 400600,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Gunner Soul": {
        "id": 400602,
        "actor_id": 400602,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Juggernaut Soul": {
        "id": 400603,
        "actor_id": 400603,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Cave Worm Soul": {
        "id": 400505,
        "actor_id": 400505,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Wasp Soul": {
        "id": 400604,
        "actor_id": 400604,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Blind Sentinel Soul": {
        "id": 400500,
        "actor_id": 400500,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Guardian Soul": {
        "id": 400501,
        "actor_id": 400501,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Nala Soul": {
        "id": 400507,
        "actor_id": 400507,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Cave Spider Soul": {
        "id": 400503,
        "actor_id": 400503,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Fireborn Soul": {
        "id": 400203,
        "actor_id": 400203,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Drone Soul": {
        "id": 400709,
        "actor_id": 400709,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Worker Soul": {
        "id": 400708,
        "actor_id": 400708,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Mite Soul": {
        "id": 400707,
        "actor_id": 400707,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Soldier Soul": {
        "id": 400710,
        "actor_id": 400710,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Bio-Bot Soul": {
        "id": 400901,
        "actor_id": 400901,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Trooper Soul": {
        "id": 400900,
        "actor_id": 400900,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Elite Guard Soul": {
        "id": 400902,
        "actor_id": 400902,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Flesh Sentinel Soul": {
        "id": 400400,
        "actor_id": 400400,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Death Guard Soul": {
        "id": 400401,
        "actor_id": 400401,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Lord of the Flesh Soul": {
        "id": 400402,
        "actor_id": 400402,
        "type": ItemType.ENEMY_SOUL.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },

    # Traps
    "Enemy Trap": {
        "id": 900000,
        "actor_id": 900000,
        "type": ItemType.TRAP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    },
    "Damage Trap": {
        "id": 900010,
        "actor_id": 900010,
        "type": ItemType.TRAP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    },
    "Spam Trap": {
        "id": 900020,
        "actor_id": 900020,
        "type": ItemType.TRAP.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    },

    # Events
    "Cave Door Key Used": {
        "id": 1000000,
        "actor_id": 0, # So the mod doesn't give anything
        "type": ItemType.EVENT.value,
        "msg_type": APMessageType.AP_MSGTYPE_NONE,
        "class": ItemClassification.progression
    },
    "Primagen Key Switch Pressed": {
        "id": 1000001,
        "actor_id": 0, # So the mod doesn't give anything
        "type": ItemType.EVENT.value,
        "msg_type": APMessageType.AP_MSGTYPE_NONE,
        "class": ItemClassification.progression
    }
}

ENEMY_NAMES = [
    "Raptoid",
    "Endtrail",
    "Compy",
    "Raptor",
    "Leaper",
    "Spider Hatchling",
    "Deadman",
    "Lord of the Dead",
    "Sister of Despair",
    "War Club",
    "Gunner",
    "Juggernaut",
    "Cave Worm",
    "Wasp",
    "Blind Sentinel",
    "Guardian",
    "Nala",
    "Cave Spider",
    "Fireborn",
    "Drone",
    "Worker",
    "Mite",
    "Soldier",
    "Bio-Bot",
    "Trooper",
    "Elite Guard",
    "Flesh Sentinel",
    "Death Guard",
    "Lord of the Flesh"
]

ITEM_NAME_TO_ID = {
    name: data["id"]
    for name, data in ITEM_TABLE.items()
}

ID_TO_ITEM = {
    data["id"]: (name, data)
    for name, data in ITEM_TABLE.items()
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    name: data["class"]
    for name, data in ITEM_TABLE.items()
}

TRAPS = {
    name: data
    for name, data in ITEM_TABLE.items()
    if data["type"] == ItemType.TRAP.value
}

LIFE_FORCES = {
    name: data
    for name, data in ITEM_TABLE.items()
    if data["type"] == ItemType.LIFE_FORCE_1.value or data["type"] == ItemType.LIFE_FORCE_10.value
}

HEALTH_PICKUPS = {
    name: data
    for name, data in ITEM_TABLE.items()
    if (not data.get("is_local") and (
        data["type"] == ItemType.SILVER_HEALTH.value or
        data["type"] == ItemType.BLUE_HEALTH.value or
        data["type"] == ItemType.FULL_HEALTH.value or
        data["type"] == ItemType.ULTRA_HEALTH.value
    ))
}
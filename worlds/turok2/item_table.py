from enum import Enum
from BaseClasses import  ItemClassification
from .client.ap_memory_constants import APMessageType

class ItemType(Enum):
    """
    Types used to filter the item table.
    """
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
    TRAP = 14,
    PROGRESSIVE_WARP = 15
    
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
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Life Force 10": {
        "id": 100001, 
        "actor_id": 1706, 
        "type": ItemType.LIFE_FORCE_10.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    
    "Silver Health": {
        "id": 100002,
        "actor_id": 1701,
        "type": ItemType.SILVER_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Blue Health": {
        "id": 100003,
        "actor_id": 1702,
        "type": ItemType.BLUE_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Full Health": {
        "id": 100004,
        "actor_id": 1703,
        "type": ItemType.FULL_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Ultra Health": {
        "id": 100005,
        "actor_id": 1704,
        "type": ItemType.ULTRA_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler
    },
    "Silver Health (L)": {
        "id": 100102,
        "actor_id": 1701,
        "type": ItemType.SILVER_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Blue Health (L)": {
        "id": 100103,
        "actor_id": 1702,
        "type": ItemType.BLUE_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Full Health (L)": {
        "id": 100104,
        "actor_id": 1703,
        "type": ItemType.FULL_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    "Ultra Health (L)": {
        "id": 100105,
        "actor_id": 1704,
        "type": ItemType.ULTRA_HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "is_local": True
    },
    
    # Ammo (and local ammo)
    "Random Ammo Pack": {
        "id": 400000,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_AMMO.value,
        "class": ItemClassification.filler
    },
    "Random Ammo Pack (L)": {
        "id": 400100,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
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
    "Beacon Power Cell": {
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
        "class": ItemClassification.useful,
        "count": 1,
        "groups": []
    },
    "Tek Bow": {
        "id": 300001,
        "actor_id": 2002,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon"]
    },
    "Pistol": {
        "id": 300002,
        "actor_id": 2004,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon"]
    },
    "Mag 60": {
        "id": 300003,
        "actor_id": 2005,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "Tranquilizer Gun": {
        "id": 300004,
        "actor_id": 2006,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": []
    },
    "Charge Dart Rifle": {
        "id": 300005,
        "actor_id": 2007,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "Shotgun": {
        "id": 300006,
        "actor_id": 2008,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon", "Good Weapon"]
    },
    "Shredder": {
        "id": 300007,
        "actor_id": 2009,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "Plasma Rifle": {
        "id": 300008,
        "actor_id": 2010,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon", "Good Weapon"]
    },
    "Firestorm Cannon": {
        "id": 300009,
        "actor_id": 2011,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "Sunfire Pod": {
        "id": 300010,
        "actor_id": 2012,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": []
    },
    "Cerebral Bore": {
        "id": 300011,
        "actor_id": 2014,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "P.F.M. Layer": {
        "id": 300012,
        "actor_id": 2015,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": []
    },
    "Grenade Launcher": {
        "id": 300013,
        "actor_id": 2016,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon", "Good Weapon"]
    },
    "Scorpion Launcher": {
        "id": 300014,
        "actor_id": 2017,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Good Weapon"]
    },
    "Flame Thrower": {
        "id": 300015,
        "actor_id": 2110,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon", "Good Weapon"]
    },
    "Razor Wind": {
        "id": 300016,
        "actor_id": 2111,
        "type": ItemType.WEAPON.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_WEAPON.value,
        "class": ItemClassification.useful,
        "count": 1,
        "groups": ["Early Weapon", "Good Weapon"]
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
        "groups": []
    },

    # Traps
    "Enemy Trap": {
        "id": 900000,
        "actor_id": 900000,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.ENEMY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    },
    "Damage Trap": {
        "id": 900010,
        "actor_id": 900010,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.DAMAGE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    },
    "Spam Trap": {
        "id": 900020,
        "actor_id": 900020,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.SPAM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap
    }
}

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
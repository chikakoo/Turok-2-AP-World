from enum import Enum
from BaseClasses import  ItemClassification
from .client.ap_memory_constants import APMessageType

class ItemType(Enum):
    """
    Types used to filter the item table.
    """
    LIFE_FORCE = 0
    HEALTH = 1
    AMMO = 2
    LEVEL_KEY = 3
    PRIMAGEN_KEY = 4
    EAGLE_FEATHER = 5
    TALISMAN = 6
    NUKE_PART = 7
    MISSION_ITEM = 8
    WEAPON = 9
    TRAP = 10
    
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
        "type": ItemType.LIFE_FORCE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 95
    },
    "Life Force 10": {
        "id": 100001, 
        "actor_id": 1706, 
        "type": ItemType.LIFE_FORCE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 5
    },
    
    "Silver Health": {
        "id": 100002,
        "actor_id": 1701,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 25
    },
    "Blue Health": {
        "id": 100003,
        "actor_id": 1702,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 65
    },
    "Full Health": {
        "id": 100004,
        "actor_id": 1703,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 7
    },
    "Ultra Health": {
        "id": 100005,
        "actor_id": 1704,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 3
    },
    "Silver Health (L)": {
        "id": 100102,
        "actor_id": 1701,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 25,
        "is_local": True
    },
    "Blue Health (L)": {
        "id": 100103,
        "actor_id": 1702,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 65,
        "is_local": True
    },
    "Full Health (L)": {
        "id": 100104,
        "actor_id": 1703,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 7,
        "is_local": True
    },
    "Ultra Health (L)": {
        "id": 100105,
        "actor_id": 1704,
        "type": ItemType.HEALTH.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_PICKUP.value,
        "class": ItemClassification.filler,
        "weight": 3,
        "is_local": True
    },
    
    # Ammo (and local ammo)
    "Random Ammo Pack": {
        "id": 400000,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_AMMO.value,
        "class": ItemClassification.filler,
        "weight": 4
    },
    "Random Ammo Pack (L)": {
        "id": 400100,
        "actor_id": 30000, # This is limited to an int16 in-game
        "type": ItemType.AMMO.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_AMMO.value,
        "class": ItemClassification.filler,
        "weight": 4,
        "is_local": True
    },

    # Inventory items
    "Level 2 Key": {
        "id": 200001,
        "actor_id": 4310,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3
    },
    "Level 3 Key": {
        "id": 200002,
        "actor_id": 4320,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3
    },
    "Level 4 Key": {
        "id": 200003,
        "actor_id": 4330,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3
    },
    "Level 5 Key": {
        "id": 200004,
        "actor_id": 4340,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3
    },
    "Level 6 Key": {
        "id": 200005,
        "actor_id": 4350,
        "type": ItemType.LEVEL_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 6
    },
    
    "Primagen Key 1": {
        "id": 200006,
        "actor_id": 4360,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 2": {
        "id": 200007,
        "actor_id": 4361,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 3": {
        "id": 200008,
        "actor_id": 4362,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 4": {
        "id": 200009,
        "actor_id": 4363,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 5": {
        "id": 200010,
        "actor_id": 4364,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    "Primagen Key 6": {
        "id": 200011,
        "actor_id": 4365,
        "type": ItemType.PRIMAGEN_KEY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression_skip_balancing,
        "count": 1,
        "groups": ["Primagen Key"]
    },
    
    "Level 2 Eagle Feather": {
        "id": 200012,
        "actor_id": 4402,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Level 3 Eagle Feather": {
        "id": 200013,
        "actor_id": 4400,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Level 4 Eagle Feather": {
        "id": 200014,
        "actor_id": 4404,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Level 5 Eagle Feather": {
        "id": 200015,
        "actor_id": 4403,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Level 6 Eagle Feather": {
        "id": 200016,
        "actor_id": 4401,
        "type": ItemType.EAGLE_FEATHER.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    
    "Leap of Faith": {
        "id": 200017,
        "actor_id": 4382,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Breath of Life": {
        "id": 200018,
        "actor_id": 4380,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Heart of Fire": {
        "id": 200019,
        "actor_id": 4384,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Whispers": {
        "id": 200020,
        "actor_id": 4383,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
    },
    "Eye of Truth": {
        "id": 200021,
        "actor_id": 4381,
        "type": ItemType.TALISMAN.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 1
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
        "count": 3
    },
    "Gate Key": {
        "id": 200200,
        "actor_id": 4030,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 2
    },
    "Graveyard Key": {
        "id": 200201,
        "actor_id": 4025,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 2
    },
    "L3 Satchel Charge": {
        "id": 200300,
        "actor_id": 4100,
        "type": ItemType.MISSION_ITEM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_INVENTORY_ITEM.value,
        "class": ItemClassification.progression,
        "count": 3
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
    "Enemy Trap (Silver Health)": {
        "id": 900000,
        "actor_id": 900000,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.ENEMY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 25
    },
    "Enemy Trap (Blue Health)": {
        "id": 900001,
        "actor_id": 900001,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.ENEMY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 65
    },
    "Enemy Trap (Full Health)": {
        "id": 900002,
        "actor_id": 900002,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.ENEMY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 7
    },
    "Enemy Trap (Ultra Health)": {
        "id": 900003,
        "actor_id": 900003,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.ENEMY.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 3
    },
    
    "Damage Trap (Silver Health)": {
        "id": 900010,
        "actor_id": 900010,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.DAMAGE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 25
    },
    "Damage Trap (Blue Health)": {
        "id": 900011,
        "actor_id": 900011,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.DAMAGE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 65
    },
    "Damage Trap (Full Health)": {
        "id": 900012,
        "actor_id": 900012,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.DAMAGE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 7
    },
    "Damage Trap (Ultra Health)": {
        "id": 900013,
        "actor_id": 900013,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.DAMAGE.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 3
    },
    
    "Spam Trap (Silver Health)": {
        "id": 900020,
        "actor_id": 900020,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.SPAM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 25
    },
    "Spam Trap (Blue Health)": {
        "id": 900021,
        "actor_id": 900021,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.SPAM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 65
    },
    "Spam Trap (Full Health)": {
        "id": 900022,
        "actor_id": 900022,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.SPAM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 7
    },
    "Spam Trap (Ultra Health)": {
        "id": 900023,
        "actor_id": 900023,
        "type": ItemType.TRAP.value,
        "trap_type": TrapType.SPAM.value,
        "msg_type": APMessageType.AP_IN_MSGTYPE_GET_TRAP.value,
        "class": ItemClassification.trap,
        "weight": 3
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
    if data["type"] == ItemType.LIFE_FORCE.value
}

HEALTH_PICKUPS = {
    name: data
    for name, data in ITEM_TABLE.items()
    if data["type"] == ItemType.HEALTH.value and not data.get("is_local")
}
from enum import Enum

class APStatus(Enum):
    """
    Status types indicating whether the client or game is ready for new
    input, or if it's currently processing.
    
    Incoming means incoming TO the game (from the game's perspective).
    Outgoing means coming FROM the game
    """
    AP_READY = 0
    """	
    Incoming: Ready to receive messages from the client
	Outgoing: The game can set data for the client to read
    """
    AP_PROCESSING = 1
    """
    Incoming: The game is processing, so the client CANNOT send it messages.
	Outgoing: The client is processing, so the game CANNOT send it messages.
    """
    
class APMessageType(Enum):
    """
    Lets the game know what kind of data is being sent to it.
    IN are values the game receives, OUT are values the client receives.
    """
    AP_MSGTYPE_NONE = 0
    """The game will see this and log that it didn't process anything."""

    AP_IN_LAST_PROCESSED_ITEM_IDX = 1
    """
    The last processed index of the item to sent to the game.
    VERY IMPORTANT to set this before sending any check!
    The game will use this for its save data to stay in sync.
    """
    
    AP_IN_MSGTYPE_GET_PICKUP = 2
    AP_IN_MSGTYPE_GET_WEAPON = 3
    AP_IN_MSGTYPE_GET_INVENTORY_ITEM = 4
    AP_IN_MSGTYPE_GET_AMMO = 5
    AP_IN_MSGTYPE_GET_TRAP = 6

class APDeathType(Enum):
    """The set of death types that the game can send out."""
    AP_DEATH_NONE = 0
    AP_DEATH_GENERIC = 1
    AP_DEATH_PLAYER_GENERIC = 2
    AP_DEATH_ENEMY_MELEE = 3
    AP_DEATH_ENEMY_SHOT = 4
    AP_DEATH_TURRET = 5
    AP_DEATH_VOID = 6
    AP_DEATH_WATER = 7
    AP_DEATH_SWAMP = 8
    AP_DEATH_LAVA = 9
    AP_DEATH_EMBER = 10
    AP_DEATH_ROCK = 11

DEATH_TYPE_MESSAGES = {
    APDeathType.AP_DEATH_NONE: "died somehow...",
    APDeathType.AP_DEATH_GENERIC: "died from some unknown source.",
    APDeathType.AP_DEATH_PLAYER_GENERIC: "died from their own actions.",
    APDeathType.AP_DEATH_ENEMY_MELEE: "was mauled to death.",
    APDeathType.AP_DEATH_ENEMY_SHOT: "was blasted to death.",
    APDeathType.AP_DEATH_TURRET: "was sniped by a turret.",
    APDeathType.AP_DEATH_VOID: "tumbled into the void.",
    APDeathType.AP_DEATH_WATER: "met with a watery grave.",
    APDeathType.AP_DEATH_SWAMP: "sunk into a swamp.",
    APDeathType.AP_DEATH_LAVA: "took a lava bath.",
    APDeathType.AP_DEATH_EMBER: "was singed by an ember.",
    APDeathType.AP_DEATH_ROCK: "was crushed by a rock.",
}
"""
What message should be displayed when the player does in a certain way.
Should be used like: "{player_name} {message}"
"""

class APMemoryOffset(Enum):
    """
    The memory offsets of each block of data.
    Each property is an int, so they are all 4 bytes.
    
    MAGIC, VERSION, and SIGNATUREs are used to locate the memory block.
    """
    MAGIC = 0
    VERSION = 4
    SIGNATURE1 = 8
    SIGNATURE2 = 12

    IN_STATUS = 16
    IN_TYPE = 20
    IN_DATA = 24
    IN_LAST_PROCESSED_ITEM_IDX = 28

    OUT_STATUS = 32
    OUT_DATA = 36
    OUT_LAST_PROCESSED_ITEM_IDX = 40
    OUT_GOAL_REACHED = 44

    CURRENT_MAP_ID = 48

    VALIDATION_SEED = 52
    PING_PENDING = 56

    SEND_DEATH_TYPE = 60
    RECEIVED_DEATH = 64
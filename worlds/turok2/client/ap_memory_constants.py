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
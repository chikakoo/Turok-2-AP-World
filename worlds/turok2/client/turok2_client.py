import asyncio
import pymem
import logging
from .ap_memory_constants import APStatus, APMemoryOffset
from argparse import Namespace
from CommonClient import CommonContext, server_loop, gui_enabled
from ..items import map_ap_item_to_game
from NetUtils import ClientStatus

logger = logging.getLogger("Client")

MAP_ID_TO_MAP_DATA = {
    # Hub
    6000: { "level": "Hub", "map": "", "section": "" },

    # Level 1
    5100: { "level": "Level 1", "map": "1-1", "section": "" },
    5200: { "level": "Level 1", "map": "1-2a", "section": "" },
    5300: { "level": "Level 1", "map": "1-3", "section": "Front" },
    5201: { "level": "Level 1", "map": "1-2b", "section": "" },
    5301: { "level": "Level 1", "map": "1-3", "section": "Back" },
    5500: { "level": "Level 1", "map": "1-4", "section": "" },
    5400: { "level": "Level 1", "map": "1-5", "section": "" },
    5600: { "level": "Level 1", "map": "1-6", "section": "" },
    5700: { "level": "Level 1", "map": "1-7", "section": "" },
    5800: { "level": "Level 1", "map": "1-8", "section": "" },
    5900: { "level": "Level 1", "map": "1-9", "section": "Catwalks" },
    5901: { "level": "Level 1", "map": "1-9", "section": "End" },

    # Level 2
    12500: { "level": "Level 2", "map": "2-1", "section": "" },
    12600: { "level": "Level 2", "map": "2-2", "section": "" },
    12700: { "level": "Level 2", "map": "2-3", "section": "" },
    12800: { "level": "Level 2", "map": "2-4", "section": "" },
    12900: { "level": "Level 2", "map": "2-5", "section": "Main" },
    12901: { "level": "Level 2", "map": "2-5", "section": "River" },
    13000: { "level": "Level 2", "map": "2-6a", "section": "" },
    13001: { "level": "Level 2", "map": "2-6b", "section": "" },
    13300: { "level": "Level 2", "map": "2-GY1", "section": "" },
    13002: { "level": "Level 2", "map": "2-6c", "section": "" },
    13100: { "level": "Level 2", "map": "2-7", "section": "" },
    13400: { "level": "Level 2", "map": "2-GY2", "section": "" },
    13200: { "level": "Level 2", "map": "2-8", "section": "" },
    13500: { "level": "Level 2", "map": "2-GY3", "section": "" },

    # Level 3
    # Level 4
    # Level 5
    # Level 6

    # Oblivion
    7800: { "level": "Level 1", "map": "1-O", "section": "" },
    7900: { "level": "Level 2", "map": "2-O", "section": "" },
    8000: { "level": "Level 3", "map": "3-O", "section": "" },
    8100: { "level": "Level 4", "map": "4-O", "section": "" },
    8200: { "level": "Level 5", "map": "5-O", "section": "" },
    8300: { "level": "Level 6", "map": "6-O", "section": "" },

    #TODO: finish this!
}

class Turok2Context(CommonContext):
    game = "Turok 2"
    
    # 0: Our starting inventory is handled locally
    # 0: We do NOT get sent items from our own world (as we'd get dups)
    # 1: We get items sent to us from other worlds
    items_handling = 0b001
    
    highest_processed_index = 0
    current_map_id: int  # Server state set by the client

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.current_map_id = ""
        
    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)
        
    # ======================
    # Game integration below
    # ======================

    # Currently on version 6
    pattern = (b"\x4B\x52\x50\x41" + 
        b"\x06\x00\x00\x00" + 
        b"\xAD\x0D\x11\x43" +
        b"\xEF\xBE\x37\x13")
        
    ap_base = None
    game_connected = False # Really, it's when AP Base isn't found
    pm = None
        
    async def connect_to_game_async(self):
        """
        Connects to the exe_name. If it fails, it sleeps for
        5 seconds before trying again.
        """
        # When this is called, it means the game isn't connected
        self.game_connected = False

        logger.info(f"Connecting to Turok 2...")
        while True:
            try:
                self.pm = pymem.Pymem(self.exe_name)
                logger.info(f"Found Turok 2 process...")
                return
            except Exception:
                await asyncio.sleep(5)
                
    async def scan_for_ap_base_async(self):
        """
        Scans the process for the AP memory block.
        
        If there is an ap_base defined, it will see if it's still valid and will use that instead.
        
        Otherwise, does the scan. If it fails more than 5 times, it will attempt to reconnect
        to the game to prevent a scenerio where it's connected to a non-existent process.
        """
        # When this is called, it means the game isn't connected
        self.game_connected = False

        # Try last known address first
        if self.ap_base is not None and self.is_ap_block_valid():
            print(f"Reusing AP block at {hex(self.ap_base)}")
            self.game_connected = True
            return self.ap_base
            
        attempt = 0
        while True:
            try:            
                self.ap_base = pymem.pattern.pattern_scan_all(
                    self.pm.process_handle,
                    self.pattern
                )
                
                if not self.ap_base or not self.is_ap_block_valid():
                    raise
                
                self.game_connected = True
                print(f"Found AP block at {hex(self.ap_base)}")
                logger.info("Connected!")
                
                return self.ap_base
                    
            except Exception:
                attempt += 1
                if attempt > 5:
                    logger.warning("Connected to the exe, but didn't find the AP memory block. This can happen if the intro cutscene plays uninterrupted. Retrying...")
                    await self.connect_to_game_async()
                    attempt = 0
                
                await asyncio.sleep(5)
                
    def is_ap_block_valid(self):
        """
        Checks that the AP block is valid by validating our header, and status values.
        
        If they are not valid, we need to connect and scan again because the struct may 
        have moved or the game may have closed.
        """
        try:
            return (self.read_int(APMemoryOffset.MAGIC) == 0x4150524B and
                self.read_int(APMemoryOffset.VERSION) == 6 and
                self.read_int(APMemoryOffset.SIGNATURE1) == 0x43110DAD and
                self.read_int(APMemoryOffset.SIGNATURE2) == 0x1337BEEF and
                self.read_int(APMemoryOffset.IN_STATUS) in (
                    APStatus.AP_READY.value,
                    APStatus.AP_PROCESSING.value
                ) and 
                self.read_int(APMemoryOffset.OUT_STATUS) in (
                    APStatus.AP_READY.value,
                    APStatus.AP_PROCESSING.value
                )
            )
        except Exception:
            return False

    def read_int(self, offset: APMemoryOffset):
        """
        Helper to read the int for the given offset.
        """
        return self.pm.read_int(self.ap_base + getattr(offset, "value", offset))

    def write_int(self, offset: APMemoryOffset, value):
        """
        Helper to write an int to the given offset.
        """
        offset = getattr(offset, "value", offset)
        value = getattr(value, "value", value)
        self.pm.write_int(self.ap_base + offset, value)
        
    async def bridge_loop_async(self):
        """
        This is the main execution loop.
        Each loop, checks if the AP block is not valid, throw an exception and try to connect again.
        Tries to process outgoing messages, as well as console commands.
        """
        await self.connect_to_game_async()
        self.ap_base = await self.scan_for_ap_base_async()
        
        while True:
            try:
                if not self.is_ap_block_valid():
                    self.game_connected = False
                    raise Exception("AP block disappeared")
                    
                await self.check_goal()
                await self.process_incoming() # Send the game pending items
                await self.process_outgoing() # Game sending us checks
                await self.process_current_map() # Send current map to trackers

                await asyncio.sleep(0.1)

            except Exception:
                logger.warning("Lost connection to game. Reconnecting...")
                await asyncio.sleep(5) # If the game was closed, let it close completely

                while True:
                    try:
                        await self.connect_to_game_async()
                        self.ap_base = await self.scan_for_ap_base_async()
                        logger.info("Reconnected successfully.")
                        break
                    except Exception:
                        print("Reconnect failed, retrying...")
                        await asyncio.sleep(3)
                        
    async def check_goal(self) -> None:
        """
        The game will keep track of the goal and set it when reached.
        """
        if not self.finished_game and self.read_int(APMemoryOffset.OUT_GOAL_REACHED) > 0:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True
        
    async def process_incoming(self):
        """
        The client will have every item received in the order it's received in self.items_received.
        Here, we use the highest processed index to get all the new items we need to get, and
        process them one at a time, incrementing the index for each one.
        """
        # Clamp it so we can't accidently go out of range
        self.highest_processed_index = min(
            self.read_int(APMemoryOffset.OUT_LAST_PROCESSED_ITEM_IDX),
            len(self.items_received)
)
        new_items = self.items_received[self.highest_processed_index:]
        for item in new_items:
            # If we're suddenly not connected, exit out
            if not self.game_connected:
                raise Exception("Game not connected")

            msg_type, msg_data = map_ap_item_to_game(item.item)
            if not await self.send_next_item_async(msg_type, msg_data):
                break
            
            print(f"Processed index: {self.highest_processed_index}")
            
    async def send_next_item_async(self, msg_type: int, data: int) -> bool:
        """
        Sends a message to the game by:
        - Checking the IN_STATUS - if not AP_READY, do nothing, as the game is currently processing one
        - Writing the IN_TYPE and IN_DATA, so the game knows the type and what value to use
        - Writing the highest processed index to IN_LAST_PROCESSED_ITEM_IDX so the game can update its index
        - Writing the IN_STATUS to AP_PROCESSING so the game knows to process what we just gave it
        """
        if self.read_int(APMemoryOffset.IN_STATUS) != APStatus.AP_READY.value:
            return False

        self.highest_processed_index += 1
        self.write_int(APMemoryOffset.IN_TYPE, msg_type)
        self.write_int(APMemoryOffset.IN_DATA, data)
        self.write_int(APMemoryOffset.IN_LAST_PROCESSED_ITEM_IDX, self.highest_processed_index)
        self.write_int(APMemoryOffset.IN_STATUS, APStatus.AP_PROCESSING)
        
        return True
        
    async def process_outgoing(self):
        """
        Process a message from the game by:
        - Checking the OUT_STATUS - if not AP_PROCESSING, do nothing, as the game hasn't sent anything.
        - Writing the OUT_DATA so we have the data the game sent us.
        - Doing something based on the type
          - This will eventually send the info to AP that the check was received.
        - Setting AP_READY to OUT_STATUS to let the game know it can send something else.
        """
        if self.read_int(APMemoryOffset.OUT_STATUS) != APStatus.AP_PROCESSING.value:
            return
        
        msg_data = self.read_int(APMemoryOffset.OUT_DATA)
        self.locations_checked.add(msg_data)
        await self.check_locations([msg_data])
            
        # Mark block ready for next message
        self.write_int(APMemoryOffset.OUT_STATUS, APStatus.AP_READY)

    async def process_current_map(self):
        """
        Grabs the current map id and sends a message to trackers with the matching level name if it changed.
        """
        current_map_id = self.read_int(APMemoryOffset.CURRENT_MAP_ID)
        if self.current_map_id != current_map_id:
            self.current_map_id = current_map_id

            current_map_data = MAP_ID_TO_MAP_DATA.get(current_map_id)
            if current_map_data:
                # Send a Bounced message to all trackers connected to the current slot
                message = {
                    "cmd": "Bounce",
                    "slots": [self.slot],
                    "tags": ["Tracker"],
                    "data": {
                        "type": "MapUpdate",
                        "level": current_map_data.get("level"),
                        "map": current_map_data.get("map"),
                        "section": current_map_data.get("section")
                    }
                }
                await self.send_msgs([message])
    
async def main(args: Namespace, exe_name) -> None:
    ctx = Turok2Context(args.url, None)
    ctx.auth = args.name
    ctx.exe_name = exe_name

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    asyncio.create_task(ctx.bridge_loop_async(), name="bridge loop")
    
    await ctx.exit_event.wait()
    await ctx.shutdown()
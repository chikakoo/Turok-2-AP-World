# Patch File
The Turok 2 patch file (extension _.apturok2_). It can be downloaded from the room, or extracted out of the generated seed when generated locally.

**Failure to install this will result in the game throwing an error when opening!** Or, if you played a previous seed, it will use that seed's randomization. There are checks to prevent playing with the wrong patch file, but if you do see the client telling you that you picked up something that you didn't, make sure you installed the correct one!

## Installing
In either case, you will need to create a _mods_ folder **(case-sensitive)** in the same directory as your Turok 2 executable. Download the randomizer files and put them in this folder.

### Via Archipelago
Open the file with Archipelago. This will move the seed-specific data (_rando.kpf_) into the _mods_ folder that you created above. It will also open the client with the connection info from the patch file already populated.

The client will show any errors if the patch file could not be moved for any reason (usually mod-mismatch reasons).

### Manually
Extract the _.apturok2_ patch file (it is an archive). Move the _rando.kpf_ into the _mods_ folder that you created above.

## Editing
The _rando.kpf_ file contains seed-specific data. Some of this data should **not** be modified, as this will change the mod's logic, making some checks impossible.

### randoReplacements.as
This is an AngelScript file with the data that the mod uses to replace/send items. It is not meant to be modified.

### apSettings.as
This contains the settings that the mod needs to know about. Some of these can be safely modified.

Below is a list of what each option does. See the yaml comments on the appropriate settings for details where applicable. For anything that accepts an _actor id_, please refer to *item_table.py* in the AP World.

#### Safe to Modify
- **OPTION_DEATH_LINK_SEVERITY**: What happens when a death link is received.
  - Set to 0-100 to set a % of health that you should lose
  - Set to -1 to receive a random amount of damage
  - Set to -2 to receive a random non-lethal amount of damage
- **OPTION_MARK_PICKUPS**: Whether to show the (!) indicator in-game for pickups. May not do anything if modified in-game.
- **OPTION_MARK_ENEMIES**: Whether to show the (!) indicator in-game for enemies. May not do anything if modified in-game.
- **OPTION_AMMO_TYPE_XXX**: XXX represents the type of ammo that each weapon should use. Valid values are:
  - "Ammo_Arrow"
  - "Ammo_TekArrow"
  - "Ammo_Bullet"
  - "Ammo_Dart"
  - "Ammo_ChargeDart"
  - "Ammo_Shell"
  - "Ammo_ExpShells"
  - "Ammo_Plasma"
  - "Ammo_SunfirePod"
  - "Ammo_Bore"
  - "Ammo_Mine"
  - "Ammo_Grenades"
  - "Ammo_Rockets"
  - "Ammo_Spears"
  - "Ammo_Torpedos"
  - "Ammo_Fuel"
  - "Ammo_Nuke"
- **OPTION_RANDOM_AMMO_MIN**: The minimum percentage of ammo that a random ammo pack gives.
- **OPTION_RANDOM_AMMO_MAX**: The maximum percentage of ammo that a random ammo pack gives.
- **OPTION_ENEMIZER**: The enemizer setting.
  - 1: Same Level
  - 2: Same Level Include Oblivion
  - 3: Similar Difficulty
  - 4: Scale to Weapons
  - 5: Chaos
- **OPTION_ENEMIZER_SPAWNERS**: The enemizer spawner setting.
  - 0: Vanilla
  - 1: Use Randomize Enemies Setting
  - 2: Easy Only
- **OPTION_ENEMY_SOULS**: The enemy souls setting.
  - 0: Off
  - 1: Off Include Checks
  - 2: No Spawns
  - 3: No Triggers
- **OPTION_ENEMY_TRAP_POOL**: The enemy trap pool.
  - 0: Same Level
  - 1: Same Level Include Oblivion
  - 2: Similar Difficulty
  - 3: Scale to Weapons
  - 4: Chaos
- **OPTION_RANDOMIZE_ENEMY_SIZES**: How to scale enemies.
  - 0: Off
  - 1: Proportional
  - 2: Disproportionate
- **OPTION_ENEMY_SIZE_MAX_PERCENTAGE**: The max percentage to scale enemies. Intended range is from 0-99.
- **OPTION_MAX_XXX**: The max ammo count for XXX. Can be any positive integer value.

### Sometimes Safe to Modify
- **OPTION_OFFLINE_MODE**: Safe to modify before starting a new game.
  - Set to false to skip pinging the client, and to not receive starting inventory from the server
  - If modified on a new game, you will receive starting inventory a second time
- **OPTION_DISABLE_PICKUPS_OVER_RIVER**: Whether the mod should prevent collection of pickups over poisoned water without the _Breath of Life_.
  - Safe to modify if changing from _true_ to _false_ if you wish to get them out of logic.
- **OPTION_DISABLE_PICKUPS_OVER_LAVA**: Whether the mod should prevent collection of pickups over lava without the _Heart of Fire_.
  - Safe to modify if changing from _true_ to _false_ if you wish to get them out of logic.

### Never Safe to Modify
- **AP_VALIDATION_SEED**: Used to validate that a save file matches the expected seed on the client. Also used in-game to check that the correct save file was loaded.
- **AP_SLOT_NAME**: Used to validate that a save file matches the expected seed on the client.
- **OPTION_GOAL_PRIMAGEN_LAIR**: Whether the goal requires visiting the Primagen.
- **OPTION_GOAL_DEFEAT_PRIMAGEN**: Whether the goal requires defeating the Primagen.
- **OPTION_GOAL_LEVELS**: How many levels the goal requires.
- **OPTION_GOAL_LEVELS_GIVE_PRIMAGEN_KEYS**: Whether completing the level goal will give all Primagen Keys.
- **OPTION_RANDOMIZE_WEAPONS**: Whether weapons are randomized.
- **OPTION_PROGRESSIVE_WARPS**: The strength of progressive warps.
- **OPTION_EXCLUDED_LEVELS**: A comma delimited list of excluded levels (e.g. 1, 3, 4).
- **OPTION_STARTING_INVENTORY_ITEMS**: A comma-delimited list of actor ids that you will start with if _OPTION_OFFLINE_MODE_ is _true_ (e.g. 4300, 4300, 4300).
- **OPTION_STARTING_WEAPONS**: A comma-delimited list of weapon pickup ids that you will start with if _OPTION_OFFLINE_MODE_ is _true_ (e.g. 2005, 2006).
- **OPTION_UNLOCK_METHOD_ONE_KEY**: Whether receiving the first level key will give all of them.
- **OPTION_UNLOCK_METHOD_ONE_WARP**: Whether the first progressive warp will grant all level keys.
- **OPTION_WEAPON_BARRIERS**: Whether weapon barriers are used.
- **OPTION_WEAPON_BARRIER_XXX**: The number of weapons needed to get past barrier XXX.
- **OPTION_PROGRESSIVE_AMMO_COUNT**: The number of progressive weapon ammo upgrades.
- **OPTION_INFINITE_AMMO_UPGRADES**: Whether the last weapon grants infinite ammo.
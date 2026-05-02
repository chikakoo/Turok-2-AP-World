# Changelog
This includes changes in both the mod and AP world, in reverse order of releases.

## v0.3.X

### v0.3.0
- Hub changes
  - Core gameplay change so that the player always starts in the hub with starting level keys
  - Added health/ammo spawns by the checkpoint station
  - Level 1 now requires 3 Level 1 Keys to enter
- Added inventory progress UI with a way to warp back to the hub checkpoint station
- Significant new options
  - Progressive warps are included by default, to limit your progress through levels until you get the progressive warp items
    - Options exist to control the starting number of them, and how far each item lets you go into each level
    - This is very important for balanced multiworlds
  - Switches can now be checks
    - Includes switches you can touch and shoot, as well as the portal and force field generators in level 5
    - This just sends a check, it doesn't actually prevent the switch from being activated
  - Mission objectives can now be checks
    - This just sends a check, it doesn't actually prevent the objective from being completed
- Other option changes
  - General renames for consistency/clarity
  - Options to start with and/or exclude sets of levels to control the size of the seed
  - Options to choose what to do with various randomized items if the level they are normally in is excluded
  - Options to choose a % of randomized Ammo/Health/Life Force pickups rather than doing all of them
  - Option to only randomize full/ultra healths when randomizing health pickups
  - Options to only randomize red or yellow Life Forces when randomizing Life Forces
  - Option to define a list of weapons you can receive when entering one of the late-game bosses
  - Option to turn level keys into "Level Key Packs", which give you all of them in one item
  - Options to configure how much ammo the Random Ammo Pack can give
  - Options to further configure filler item distrubution, including making it put all randomized vanilla items back into the pool
  - Removed the Open Hub setting, as you always start there now
  - Removed the level key randomization setting, as they will always be randomized
- Location name changes
  - Each location is prefixed by the map it's on for easier Universal Tracker visuals
  - Spawning into a map now shows the progress count automatically to help track progress/where you are
- Added a "Useful" AP model to use for off-world useful items
- Removed the jank extra level warp portals, since the UI can be used instead
- Support the Start Inventory setting
- Bug fixes
  - Issues with syncing items with AP...
     - If you collect some before connecting to the client
     - If you disconnect from the client, collect some, then reconnect

## v0.2.X

### v0.2.2:
- Removed impossible to send location "LBO Lava Caves - Plasma Rounds by Lava"
- Fixed Level 6 Oblivion portal being logically accessible without the two Blue Laser Cells
- Fixed generation failures if guarantee_torpedo_launcher is on, but weapons are not randomized

### v0.2.1:
- Fixed enemy traps from Leap of Faith jumps potentially knocking you down, causing softlocks
- Fixed non-collected items not sent to AP during Leap of Faith jumps
- Fixed some items not showing the map progress message
- If there is a level goal, totem missions will restart if unsuccessful to prevent softlocks
- Updated description of the "Get to Lair" setting to be clearer what it is

### v0.2.0:
- All levels are now included
- Ability to open the hub from the beginning (so Level 1 doesn't need to be completed)
- Options reworked to be clearer in general
- Options to weigh health pickups and life force pickups
- Options to choose whether or not to randomize various locations
- Options to choose level and Primagen goals separately (or at the same time)

## v0.1.X
Initial release. This version does work with AP, but with limited options.

### v0.1.0
- Randomizes weapon pickups, ammo pickups, health pickups, and Life Forces
- No options to configure what can be randomized
- Only level 1 is supported
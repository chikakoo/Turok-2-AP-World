# Turok 2: Seeds of Evil Remastered

## IMPORTANT

**If "Auto-Switch New Weapon" is on and you receive a new weapon while on the Riding Gun in Level 2, you will be softlocked! Turn off that setting for this map! If you DO get softlocked in this way, press "_~_" to open the console, then type "_warp 125_" to reload the map.**

## Where is the options page?

Archipelago uses yaml files for game options. You will need to get and edit the yaml with your desired options. Either download from [the release](https://github.com/chikakoo/Turok-2-Randomizer/releases), or generate it from the Archipelago Launcher.

To generate it, install the AP world by downloading it and double-clicking it (or by putting it in your Archipelago's "custom worlds" directory). In the launcher, run "Generate Template Option" to generate the yaml.

## What items and locations get randomized?

Static pickups (those not spawned from destructibles):
- Health
- Ammo and weapons (combined in a single setting for now)
- Life Forces
- Level Keys
- Eagle Feathers
- Talismans
- Nuke Parts
- Mission Items
  - (L1) Power Cells
  - (L2) Gate Keys; Graveyard Keys
  - (L3) Satchel Charges
  - (L4) Satchel Charges; Cave Door Keys
  - (L5) Satchel Charges
  - (L6) Ion Capacitors; Blue Laser Cell; Red Laser Cell

## What does randomization mean?

If randomized, weapons have a single copy in the item pool. Once found, it is unlocked like in the vanilla game. See the ammo explanation later on for how ammo is changed.

Life force tiles, health, and ammo are not actually shuffled, but are generated from the junk item pool based on yaml settings. Weights of specific health and Life Forces can be configured.

## What core changes have been made?

### Collection status displays

When picking up an item, it will show you how many checks are left on the map. There are two menus you can use to track progress as well:
- Holding your **zoom in + zoom out buttons** at the same time for a bit will show the current collection progress for the current level
- Holding **jump + zoom in + zoom out** at the same time will show the current collection progress for the current level

These are important, because **the randomizer breaks the in-game inventory screen.** It will not accurately show your progress.

### Pickup indicators

All checks will use the in-game "important" item exclamation point to make them easier to find. This is not yet a togglable setting.

They won't show up like this if the in-game option is off, though.

### Ammo

Randomized ammo is now "Random Ammo" to avoid ammo starvation. When received, it grants between 20-75% of your ammo back in a random weapon (including alt ammo). It will roll to (not 100% of the time) give ammo back in weapons with no ammo first, then ones missing ammo. Otherwise, it will choose from your entire weapon list. 

Random Ammo looks like 6 shotgun shells in the Archipelago colors.

Ammo from destructables, most generators, and enemy drops are unchanged.

### New Portals

To allow access to the hub before completing levels 2-6, additional portals have been added near the start of the level. Use them if you need to return but you haven't completed the mission objectives.

### Why is my Flare Gun weird/not accessible?

Due to modding limitations, the Flare Gun now requires you to have explosive shells to use (it does not consume them). It otherwise behaves normally.

This was a workaround so that explosive shells could be given from the random ammo pickups.

## Which items can be in another player's world?

Anything that can be randomized.

## What does another world's item look like in Turok 2?

Items belonging to other worlds are represented by an Archipelago model. Progression items have a gold border, and all others have a gray one.

## When the player receives an item, what happens?

All pickups will be collected with the usual sound effects/voice lines. If the in-game setting is on, the auto-weapon switch will occur for new weapons. **See the note on the top about this setting!**

Due to modding limitations, Life Forces will spawn where the player is. They will be instantly picked up when the player moves. If left uncollected before saving, they will be lost.

## Hey! This pickup isn't randomized!

A select few pickups aren't randomized because they only exist in lower difficulties. This was done to keep the seeds difficulty-agnostic. These locations are:
- Three Blue Healths in the River of Souls' Life Force Leap of Faith room
- The four Ultra Healths after completing each wing in the Primagen's Lightship

Other exceptions include:
- The Death Marshes red Life Forces in the cages by the talisman portal switch. These aren't included because they aren't pickups until the cages fall. For simplicity, replacements are only done on a map load, so these get excluded.
- Two yellow Life Forces in the Primagen's Lightship wing 1, in the catwalks room. These are actually sets of two Life Forces on the exact same spot. This makes it difficult to safely do the replacement, so they're excluded for now.

Generators and spawns from destructable objects are not randomized at this time.

Any others may be a mistake, so feel free to ask.

## My server is messed up! How do I resync?

This mod will listen for when the client has acknowledged that it has processed a check. It will save the list of unsent locations when you save your game, and resync any unsent locations when you load. However, in the unlikely case that the server doesn't know that you got a check, you'll need to resync.

To do this manually, load into your save file and **press the tilde (~) key**. This will open the console. Run the following command to resync: **call Resync**.

Note that **this is not optimized for speed**, and will take a bit to run (it will process about 10 checks per second, due to the client's tick rate). It's not expected that this will ever be needed.

## Help! I'm softlocked!

If something is messed up with the randomizer/Archipelago and you didn't get an item you were supposed to, please post on Discord so it can be fixed. All debug console commands are included with the mod, so you should be able to give yourself any item you need to get yourself unstuck. To see the list of commands, do the following:
- Press "_~_" to open the console.
- Type "_call Help_" to display a list of commands. In general, giving yourself any item will be "_call ItemNameHere_".
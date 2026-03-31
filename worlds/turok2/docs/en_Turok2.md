# Turok 2: Seeds of Evil Remastered

## Where is the options page?

Archipelago uses yaml files for game options. You will need to get and edit the yaml with your desired options. Either download from [the release](https://github.com/chikakoo/Turok-2-Randomizer/releases), or generate it from the Archipelago Launcher.

To generate it, install the AP world by downloading it and double-clicking it (or by putting it in your Archipelago's "custom worlds" directory). In the launcher, run "Generate Template Option" to generate the yaml.

## What items and locations get randomized?

All pickups, including life forces, health, ammo, and weapons have been randomized. This also includes key items such as mission-required pickups such as the beacon power cells. Level keys, primagen keys, eagle feathers, and talismans are also included.

## What does randomization mean?

Weapons now have a single copy in the item pool. Once found, it is unlocked like in the vanilla game.

Life force tiles, health, and ammo are not actually shuffled, but are instead randomly generated based on yaml settings. Weights of the specific health and ammo are not yet configurable.

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

Random Ammo looks like a small box of bullets.

Ammo from destructables, depots, and enemy drops are unchanged.

### Why is my Flare Gun weird/not accessible?

Due to modding limitations, the Flare Gun now requires you to have explosive shells to use (it not consume them). It otherwise behaves normally.

This was a workaround so that explosive shells could be given from the random ammo pickups.

## Which items can be in another player's world?

All of what was mentioned above.

## What does another world's item look like in Turok 2?

Items belonging to other worlds are represented by the blue baby-faced life force tile.

## When the player receives an item, what happens?

Health/ammo/weapons will be collected with the usual sound effects. If the in-game setting is on, the auto-weapon switch will occur for new weapons.

Due to modding limitations, life tiles will spawn where the player is. They will be instantly picked up when the player moves. If left uncollected before saving, they will be lost.

## My server is messed up! How do I resync?

This mod will listen for when the client has acknowledged that it has processed a check. It will the list of unsent locations when you save your game, and resync any unsent locations when you load. However, in the unlikely case that the server doesn't know that you got a check, you'll need to resync.

To do this manually, load into your save file and **press the tilde (~) key**. This will open the console. Run the following command to resync: **call Resync**.

Note that **this is not optimized for speed**, and will take a bit to run (it will process about 10 checks per second, due to the client's tick rate). It's not expected that this will ever be needed.
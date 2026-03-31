# Turok 2 Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- The 2017 Turok 2: Seeds of Evil Remastered by Nightdive Studios for the PC. Only tested with the Steam version, but should work with any.
- [The Turok 2 apworld and mod](https://github.com/chikakoo/Turok-2-Randomizer/releases)

## How to play

First, you need a room to connect to. For this, you or someone you know has to generate a game. Check the [Archipelago Setup Guide](/tutorial/Archipelago/setup_en#generating-a-game) for how to do this.

You also need to have [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest) installed and the [The Turok 2 apworld](https://github.com/chikakoo/Turok-2-Randomizer/releases) installed into Archipelago.

## Installing the mod

Installing the mod is very simple. First, locate your Turok 2 installation folder. The typical Steam location is _C:\Program Files (x86)\Steam\steamapps\common\Turok 2 - Seeds of Evil_.

Once there, create a _mods_ folder. Extract the files from the mod zip (the _.kpf_ files) you downloaded from the [Required Software](#required-software) section into this folder. You should have a few files like: **mods/FileNameHere.kpf**.

**Test that it worked before playing. You will see a custom title screen if it worked.**

## Patch files

Turok 2 uses a patch file to do its randomization and apply the game-specific yaml settings to the game.

When your seed is generated, acquire your patch file like you normally would _(downloaded from the room, or extracted from the generated seed zip)_. Extract the files from the patch - you should see one called _rando.kpf_. Place _rando.kpf_ with the other mod files.

**Failure to install this will result in local items not being randomized!** Or, if you played a previous seed, it will use that seed's randomization. If you see the client telling you that you picked up something that you didn't, make sure you installed the correct patch!

## Connecting to the client

In _ArchipelagoLauncher.exe_, open the _Turok 2 Client_. If your Turok 2 executable isn't in the typical spot, it will prompt you to select it. **Selecting the wrong one will result in the client being unable to hook into the game.**

Connect to your room and slot. Launch your game. When you get to the title screen, ensure that the client says it connected.

This can be done in any order (i.e. you can start your game first if you'd like).

## Switching Rooms

If you are starting a new seed, you will need to **close your game completely before installing the patch.**

The client shoudn't need to be restarted, but be sure that you disconnect and reconnect to the appropriate slot.

## But I want to play solo!

That's fine! You don't actually need to use the Turok 2 client in this case. Generate your seed through Archipelago and apply the patch as instructed.

You're now good to play the game without Archipelago!
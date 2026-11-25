# Turok 2 Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- The 2017 Turok 2: Seeds of Evil Remastered by Nightdive Studios for the PC. Only tested with the Steam version, but should work with any.
- [The Turok 2 apworld and mod](https://github.com/chikakoo/Turok-2-AP-World/releases)

## How to play

First, you need a room to connect to. For this, you or someone you know has to generate a game. Check the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup_en) for how to do this.

You also need to have [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest) installed and the [Turok 2 apworld](https://github.com/chikakoo/Turok-2-AP-World/releases) installed into Archipelago. You can do this by double clicking the apworld, or putting it in your "custom_worlds" folder.

See the [Linux setup](#linux-setup) for how to get this to work in Linux. This setup may also be relevant for Mac (please let me know if it is).

## Installing the mod

Installing the mod is very simple. First, locate your Turok 2 installation folder. The typical Steam location is _C:\Program Files (x86)\Steam\steamapps\common\Turok 2 - Seeds of Evil_.

Once there, create a _mods_ folder. Extract the files from the mod zip (the _.kpf_ files) you downloaded from the [Required Software](#required-software) section into this folder. You should have a few files like: **mods/FileNameHere.kpf**.

Follow the steps in the [Patch Files](https://github.com/chikakoo/Turok-2-AP-World/blob/main/worlds/turok2/docs/patch_file.md) instructions (either through AP or manually) to install the _rando.kpf_ file here. **The game will fail to run if you don't do this!**

**Test that it worked before playing. You will see a custom title screen if it worked.**

## Connecting to the client

In _ArchipelagoLauncher.exe_, open the _Turok 2 Client_. If your Turok 2 executable isn't in the typical spot, it will prompt you to select it. **Selecting the wrong one will result in the client being unable to hook into the game.**

Connect to your room and slot. Launch your game. When you get to the title screen, ensure that the client says it connected.

This can be done in any order (i.e. you can start your game first if you'd like).

_Note that if you are using a mod version that is not compatible with the AP World, it will not connect._

## Switching Rooms

If you are starting a new seed, you will need to **close your game completely before installing the patch.**

The client shoudn't need to be restarted, but be sure that you disconnect and reconnect to the appropriate slot.

## But I want to play solo!

That's fine! You don't actually need to use the Turok 2 client in this case. Generate your seed through Archipelago and apply the patch as instructed.

You're now good to play the game without Archipelago!

## Linux Setup
Modified from [this Discord post](https://discord.com/channels/731205301247803413/1238135254947074129/1544566143203676180). Please refer to this and post there if you need help.

- Set Turok 2 to a Proton compatibility tool
  - _This'll install the Windows version. If you have the mods in the folder it shouldn't touch them._
- Boot Turok 2 to generate the Wine prefix and close it
- Open the Archipelago installer through Protontricks and install it
- Open the launcher through Protontricks in the Turok 2 prefix to install the APWorld, then close it
  - For example: `protontricks-launch --appid 405830 '~/.local/share/Steam/steamapps/compatdata/405830/pfx/drive_c/ProgramData/Archipelago/ArchipelagoLauncher.exe'` as seen in the _.desktop_ file attached
- Open the game first, then open the launcher
  - _If you close out of the game it shuts down everything in the prefix and the launcher gets force closed as well_
- Find the actual location of the Turok 2 executable
  - It'll be in `Z:\home\[username]\.local\share\Steam\steamapps\[so on and so forth]`
    - The `S: drive` may better for this purpose
  - If you don't see this open up Protontricks itself on your prefix, open up winecfg, and in the "drives" area there should be a "show dot files" toggle you can toggle on
- At this point you should be able to send and receive items
import re
from dataclasses import dataclass
from Options import Choice, OptionGroup, OptionList, OptionSet, OptionDict, \
    ItemSet, PerGameCommonOptions, Range, NamedRange, Toggle
from schema import Schema, And
from typing import List

# TODO:
# death link

class LevelGoal(Range):
    """
    The number of levels you need to complete for your goal.

    If the Primagen goal is None, it will fail to generate if this is not set to at least 1.
    """
    display_name = "Levels Goal"
    range_start = 0
    range_end = 6
    default = 2

class PrimagenGoal(Choice):
    """
    Sets the Primagen goal. See the RandomizePrimagenKeys setting for options on how to get to the lair.
    - None: The Primagen is not part of the goal. Primagen Keys are not in the item pool.
    - Defeat: Defeat the Primagen and view the ending cutscene.
    - Get to Lair: Arriving at the Primagen's lair will complete the goal. Use this if you
                   want Primagen Keys to be part of the goal, but don't want to fight the boss.
    """
    display_name = "Primagen Goal"
    option_none = 0
    option_defeat = 1
    option_get_to_lair = 2
    default = option_defeat

class RandomizePrimagenKeys(Choice):
    """
    If the Primagen goal is not None, sets how you get the Primagen Keys.
    - Vanilla In Pool If level Excluded: 
         Primagen Keys are in their vanilla locations. 
         If that level is excluded, it will be in the item pool.
    - Vanilla Start With If Level Excluded: 
         Primagen Keys are in their vanilla loactions.
         If that level is excluded, you will start with it.
    - In Pool: The Primagen keys will be in the item pool to find.
    - Levels: The Primagen keys will be given to you after you complete the number of levels 
              specified in the LevelGoal setting.
    """
    display_name = "Randomize Primagen Keys"
    option_vanilla_in_pool_if_level_excluded = 0
    option_vanilla_start_with_if_level_excluded = 1
    option_in_pool = 2
    option_levels = 3
    default = option_in_pool

class RandomizeWeapons(Toggle):
    """
    Whether to include static weapon pickups in the list of locations to check.
    Each weapon will have one entry in the item pool.

    Any ammo in the item pool will be random ammo pickups, granting ammo in a random owned
    weapon (favoring those lacking ammo). This is to ensure that you can always get ammo
    for the randomly rolled weapons.
    """
    display_name = "Randomize Weapons"
    default = True

class StartingWeapons(OptionList):
    """
    The list of weapons to start with. Include them multiple times in the list if you wish to
    start with multiple ProgressiveWeaponAmmoUpgrades.

    Will not be included if in the ExcludedWeapon list.

    Valid weapons: [
        "War Blade", "Tek Bow", "Pistol", "Mag 60", "Tranquilizer Gun",
        "Charge Dart Rifle", "Shotgun", "Shredder", "Plasma Rifle", "Firestorm Cannon",
        "Sunfire Pod", "Cerebral Bore", "P.F.M. Layer", "Grenade Launcher", "Scorpion Launcher",
        "Flame Thrower", "Razor Wind", "Harpoon Gun", "Torpedo Launcher", "Nuke"
    ]
    """
    display_name = "Starting Weapons"
    valid_keys = {
        "War Blade",
        "Tek Bow",
        "Pistol",
        "Mag 60",
        "Tranquilizer Gun",
        "Charge Dart Rifle",
        "Shotgun",
        "Shredder",
        "Plasma Rifle",
        "Firestorm Cannon",
        "Sunfire Pod",
        "Cerebral Bore",
        "P.F.M. Layer",
        "Grenade Launcher",
        "Scorpion Launcher",
        "Flame Thrower",
        "Razor Wind",
        "Harpoon Gun",
        "Torpedo Launcher",
        "Nuke"
    }
    default = []

class ExcludedWeapons(ItemSet):
    """
    The set of weapons to exclude from the item pool, meaning you won't see them in your seed.
    Does not affect the ones in the BossWeaponList.

    Valid weapons: [
        "War Blade", "Tek Bow", "Pistol", "Mag 60", "Tranquilizer Gun",
        "Charge Dart Rifle", "Shotgun", "Shredder", "Plasma Rifle", "Firestorm Cannon",
        "Sunfire Pod", "Cerebral Bore", "P.F.M. Layer", "Grenade Launcher", "Scorpion Launcher",
        "Flame Thrower", "Razor Wind", "Harpoon Gun", "Torpedo Launcher"
    ]
    """
    display_name = "Excluded Weapons"
    valid_keys = {
        "War Blade",
        "Tek Bow",
        "Pistol",
        "Mag 60",
        "Tranquilizer Gun",
        "Charge Dart Rifle",
        "Shotgun",
        "Shredder",
        "Plasma Rifle",
        "Firestorm Cannon",
        "Sunfire Pod",
        "Cerebral Bore",
        "P.F.M. Layer",
        "Grenade Launcher",
        "Scorpion Launcher",
        "Flame Thrower",
        "Razor Wind",
        "Harpoon Gun",
        "Torpedo Launcher"
    }
    default = []

class UseWeaponBarriers(Toggle):
    """
    Cannot be used unless playing with randomized weapons.

    Places green warp barriers at the start, middle, and/or end of each level that you cannot pass until you obtain
    a certain number of unique weapons. These include all weapons in the game, excluding the Talon, Bow, Flare Gun,
    Nuke, Harpoon Gun, and Torpedo Launcher.

    It's recommended to use this if you want to avoid potentially using the bow for longer periods of time.
    
    The specific settings are configured in WeaponBarrierSettings. 
    """
    display_name = "Use Weapon Barriers"
    default = True

class WeaponBarrierSettings(OptionDict):
    """
    Controls when weapon barriers appear (see UseWeaponBarriers for more details).
    Must contain the keys "Level X Start", "Level X Mid", and "Level X End" for levels 1-6.
    - Start places a barrier on the second warp of each level
    - Mid places a barrier on the map of the second checkpoint station of each level
      - Level 6 is the exception, which places it on the portal to Wing 3
    - End places a barrier leading to the final map of each level

    Note that the max number of progressive weapons is 17.
    """
    display_name = "Weapon Barrier Settings"
    default = {
        "Level 1 Start": 1,
        "Level 1 Mid": 2,
        "Level 1 End": 3,
        "Level 2 Start": 2,
        "Level 2 Mid": 3,
        "Level 2 End": 4,
        "Level 3 Start": 2,
        "Level 3 Mid": 4,
        "Level 3 End": 4,
        "Level 4 Start": 3,
        "Level 4 Mid": 5,
        "Level 4 End": 6,
        "Level 5 Start": 4,
        "Level 5 Mid": 5,
        "Level 5 End": 7,
        "Level 6 Start": 4,
        "Level 6 Mid": 6,
        "Level 6 End": 8
    }
    required_keys = [
        "Level 1 Start",
        "Level 1 Mid",
        "Level 1 End",
        "Level 2 Start",
        "Level 2 Mid",
        "Level 2 End",
        "Level 3 Start",
        "Level 3 Mid",
        "Level 3 End",
        "Level 4 Start",
        "Level 4 Mid",
        "Level 4 End",
        "Level 5 Start",
        "Level 5 Mid",
        "Level 5 End",
        "Level 6 Start",
        "Level 6 Mid",
        "Level 6 End"
    ]
    schema = Schema(
        {
            key: And(
                int,
                lambda n: 0 <= n <= 17,
                error=f"{key} must be an integer between 0 and 17"
            )
            for key in required_keys
        },
        ignore_extra_keys=False
    )

class RandomizeAmmoPickups(NamedRange):
    """
    Whether to include ammo pickups in the list of locations to check.

    Set this to the percentage of all ammo pickups you wish to include.
    Each 1% adds approximately 7 locations.
    """
    display_name = "Randomize Ammo Pickups"
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "none": 0,
        "all": 100
    }

class ProgressiveWeaponAmmoUpgrades(Range):
    """
    Only used if randomizing weapons. Standard arrows are not affected for balance reasons.
    Does not include weapons with no ammo.
    
    Places multiple of each weapon in the item pool.
    For each of the same progressive weapon found, less ammo will be consumed.
    Use this in combination with the max ammo multipliers to nerf/buff weapons as the seed progresses.

    Example with the Mag 60: if set to 3, the first Mag 60 will consume 3x the normal ammo per shot (9).
    The second will comsume 2x (6). All three will be vanilla behavior (3).
    """
    display_name = "Progressive Ammo Upgrades"
    range_start = 1
    range_end = 5
    default = 1

SPECIAL_AMMO_NAMES = {
    "quarter": 25,
    "half": 50,
    "vanilla": 100,
    "double": 200,
    "triple": 300,
    "quadruple": 400
}

def validate_ammo_multiplier(value):
    """
    Validates that the given value...
    - is between 1 and 400, inclusive, or...
    - is one of the SPECIAL_AMMO_NAMES, or...
    - is of the format "low-high", where low <= high and both are between 1 and 400
    """
    if isinstance(value, int):
        return 1 <= value <= 400

    if isinstance(value, str):
        if value in SPECIAL_AMMO_NAMES:
            return True

        match = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", value)
        if match:
            low = int(match.group(1))
            high = int(match.group(2))

            return (
                1 <= low <= 400 and
                1 <= high <= 400 and
                low <= high
            )

    return False

@dataclass(frozen=True)
class AmmoData:
    vanilla_max: int
    macro_suffix: str

class MaxAmmoSettings(OptionDict):
    """
    Defines the max ammo percentages for the various ammo types.
    For example, 100 would be vanilla, 200 would be double vanilla, etc.

    Be careful with setting these to low values, as it will severely limit your shot count.
    
    Inputs accepted:
    - Any number between 1 and 400
    - A range in the format "low-high"
      - e.g. "Bullets": "50-150" would generate a value between 50-150, inclusive
    - "quarter": Equal to 25
    - "half": Equal to 50
    - "vanilla": Equal to 100
    - "double": Equal to 200
    - "triple": Equal to 300
    - "quadruple": Equal to 400

    Vanilla ammo counts, for reference:
    - Bullets: 50
    - Shotgun Shells: 20
    - Explosive Shotgun Shells: 10
    - Tek Arrows: 10
    - Tranquilizer Darts: 15
    - Charge Darts: 30
    - Plasma Rounds: 150
    - Sunfire Pods: 6
    - Bores: 10
    - Mines: 10
    - Grenades: 10
    - Scorpion Missiles: 12
    - Flame Thrower Fuel: 50
    - Nuke Ammo: 5
    - Spears: 12
    - Torpedoes: 3
    """
    display_name = "Max Ammo Settings"

    ammo_data = {
        "Bullets": AmmoData(vanilla_max=50, macro_suffix="BULLET"),
        "Shotgun Shells": AmmoData(vanilla_max=20, macro_suffix="SHOTGUN_SHELL"),
        "Explosive Shotgun Shells": AmmoData(vanilla_max=10, macro_suffix="EXPLOSIVE_SHOTGUN_SHELL"),
        "Tek Arrows": AmmoData(vanilla_max=10, macro_suffix="TEK_ARROW"),
        "Tranquilizer Darts": AmmoData(vanilla_max=15, macro_suffix="TRANQUILIZER_DART"),
        "Charge Darts": AmmoData(vanilla_max=30, macro_suffix="CHARGE_DART"),
        "Plasma Rounds": AmmoData(vanilla_max=150, macro_suffix="PLASMA_ROUND"),
        "Sunfire Pods": AmmoData(vanilla_max=6, macro_suffix="SUNFIRE_POD"),
        "Bores": AmmoData(vanilla_max=10, macro_suffix="BORE"),
        "Mines": AmmoData(vanilla_max=10, macro_suffix="MINE"),
        "Grenades": AmmoData(vanilla_max=10, macro_suffix="GRENADE"),
        "Scorpion Missiles": AmmoData(vanilla_max=12, macro_suffix="SCORPION_MISSILE"),
        "Flame Thrower Fuel": AmmoData(vanilla_max=50, macro_suffix="FLAME_THROWER"),
        "Nuke Ammo": AmmoData(vanilla_max=5, macro_suffix="NUKE_AMMO"),
        "Spears": AmmoData(vanilla_max=12, macro_suffix="SPEAR"),
        "Torpedoes": AmmoData(vanilla_max=3, macro_suffix="TORPEDO")
    }
    default = {
        key: "vanilla"
        for key in ammo_data.keys()
    }

    schema = Schema(
        {
            key: And(
                validate_ammo_multiplier,
                error=f"{key} must be an integer, special name, or range (values between 1-400)."
            )
            for key in ammo_data.keys()
        },
        ignore_extra_keys=False
    )

class RandomizeHealthPickups(NamedRange):
    """
    Whether to include static health pickups in the list of locations to check.

    Note that the four ultra healths in the Level 6 hub are excluded, as these
    only exist in lower difficulties.

    Set this to the percentage of all life forces you wish to include.
    Each 1% adds approximately 8 locations.

    - None: No health pickup locations will be included
    - All: All health pickup locations will be included
    - Full And Ultra Only (value of -1): Only full and ultra health locations will be included.
    """
    display_name = "Randomize Health Pickups"
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "none": 0,
        "all": 100,
        "full_and_ultra_only": -1
    }
    
class RandomizeLifeForces(NamedRange):
    """
    Whether to include Life Forces in the list of locations to check.

    Set this to the percentage of all life forces you wish to include.
    Each 1% adds approximately 13 locations.

    - None: No Life Force locations will be included
    - All: Both yellow and red Life Forces will be included
    - Yellow Only (value of -1): Only yellow Life Forces will be included
    - Red Only (value of -2): Only red Life Forces will be included
    """
    display_name = "Randomize Life Forces"
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "none": 0,
        "all": 100,
        "yellow_only": -1,
        "red_only": -2
    }

class RandomizeEagleFeathers(Toggle):
    """
    Whether to include eagle feathers in the list of locations to check.
    Setting this to False will place them in their vanilla locations.
    """
    display_name = "Randomize Eagle Feathers"
    default = True

class RandomizeTalismans(Choice):
    """
    Whether to include talismans in the list of locations to check.
    Setting this to False will place them in their vanilla locations.
    - Vanilla In Pool If level Excluded: 
         Talismans are in their vanilla locations. 
         If that level is excluded, it will be in the item pool.
    - Vanilla Start With If Level Excluded:
         Talismans are in their vanilla loactions.
         If that level is excluded, you will start with it.
    - In Pool: The talisman will be in the item pool.
    """
    display_name = "Randomize Talismans"
    option_vanilla_in_pool_if_level_excluded = 0
    option_vanilla_start_with_if_level_excluded = 1
    option_in_pool = 2
    default = option_in_pool
    
class RandomizeMissionItems(Toggle):
    """
    Whether to include items needed to finish the level. For example, the beacon power cells
    in level 1 or the graveyard keys in level 2.
    """
    display_name = "Randomize Mission Items"
    default = True

class RandomizeSwitches(Toggle):
    """
    Each switch triggered will be a check. Includes switches you touch and shoot.
    Talisman/Oblivion portal switches as well as the level 5 force field generators are included here.
    
    This will put one filler item into the item pool per switch.
    """
    display_name = "Randomize Switches"
    default = True

class RandomizeMissionObjectives(Toggle):
    """
    Each mission objective task will be a check. For example, each rescued child is one check.
    
    This will put one filler item into the item pool per mission objective task.
    """
    display_name = "Randomize Mission Objectives"
    default = True

class ForceEarlyWeapon(Toggle):
    """
    Forces an early weapon so you have more than just the bow.
    """
    display_name = "Force Early Weapon"
    default = True

class BossWeaponList(OptionSet):
    """
    A pool of weapons from which one will be received when starting the boss for level 4, 5, or 6.
    This is separate from the Archipelago item pool.

    Due to technical limitations, these bossescannot be warped out of (but the Primagen can be).
    They can technically be defeated with only the bow, but it's extremely painful. It is very highly
    recommended that at least one good weapon is in this list.

    The defaults are weapons that are usually helpful enough on these bosses. The other choices are either
    difficult to use, not that great, or can't always do damage. Only clear out/modify this list if you 
    know what you're doing.

    All valid weapons for this setting are:
    ["Tek Bow", "Pistol", "Mag 60", "Shotgun", "Shredder", "Plasma Rifle", "Firestorm Cannon", 
    "P.F.M. Layer", "Grenade Launcher", "Scorpion Launcher", "Flame Thrower", "Razor Wind"]
    """
    display_name = "Boss Weapon List"
    valid_keys = frozenset({
        "Tek Bow",
        "Pistol",
        "Mag 60",
        "Shotgun",
        "Shredder",
        "Plasma Rifle",
        "Firestorm Cannon",
        "P.F.M. Layer",
        "Grenade Launcher",
        "Scorpion Launcher",
        "Flame Thrower",
        "Razor Wind"
    })
    default = frozenset({
        "Mag 60",
        "Shotgun",
        "Shredder",
        "Plasma Rifle",
        "Firestorm Cannon",
        "Grenade Launcher",
        "Flame Thrower"
    })
    
class NukeBehavior(Choice):
    """
    Defines how to get the Nuke weapon.
    - Disabled: There is no Nuke. Oblivion portals will have a random check.
    - Vanilla In Pool If level Excluded: 
         The 6 Nuke Parts are in their vanilla locations. 
         If that level is excluded, it will be in the item pool.
    - Vanilla Start With If Level Excluded: 
         The 6 Nuke Parts are in their vanilla loactions.
         If that level is excluded, you will start with it.
    - Nuke Part Hunt: The 6 Nuke Parts will be shuffled into the pool. Oblivion portals will have a random check.
    - Weapon Pickup: The Nuke will be obtaned as a single item. Oblivion portals will have a random check.
    """
    display_name = "Nuke Behavior"
    option_disabled = 0
    option_vanilla_in_pool_if_level_excluded = 1
    option_vanilla_start_with_if_level_excluded = 2
    option_nuke_part_hunt = 3
    option_weapon_pickup = 4
    default = option_nuke_part_hunt

class LevelKeyPacks(Toggle):
    """
    When receiving a level key, you get all of them.
    There will be only one level key in the pool for each included level.
    """
    display_name = "level Key Packs"
    default = False

class ProgressiveWarps(Toggle):
    """
    Progressive Warp items for each level will be added to the item pool. Warp portals will now be 
    blocked by a barrier if you do not have the required number of these items.
    
    Highly recommended for this to be on if on a multiworld, as it splits up levels into logical sections.
    """
    display_name = "Progressive Warps"
    default = True

class ProgressiveWarpStrength(NamedRange):
    """
    Used if Progressive Warps are on.
    The number of warps each Progressive Warp item allows you to travel through.
    - Low: Each Progressive Warp advances through one warp
    - Quarter: Each Progressive Warp advances through roughly a quarter of the level
    - Half: Each Progressive Warp advances through roughly half of the level
    - Most: Each Progressive Warp advances through most of the level
    """
    display_name = "Progressive Warp Strength"
    range_start = 1
    range_end = 15
    default = 1
    special_range_names = {
        "low": 1,
        "quarter": 3,
        "half": 5,
        "most": 8
    }

class StartingProgressiveWarps(Range):
    """
    Used if Progressive Warps are on.

    The number of Progressive Warp items you will start with.

    If set too low, this could cause generation failures for solo worlds if not a lot of item types are
    included in the item pool, depending on your starting levels.

    If set too high, your sphere 1 will be really big.
    """
    display_name = "Starting Progressive Warps"
    range_start = 0
    range_end = 20
    default = 1

class StartingLevels(OptionList):
    """
    The set of levels that will be unlocked at the start of the seed.

    You can add multiples of the following entries:
    - Random: Will pick from any non-excluded level
    - RandomEarly: Will pick from any non-excluded level, prioritizing levels 1-3
    - RandomLate: Will pick from any non-excluded level, prioritizing levels 4-6

    Be careful with this, as there's no soft logic yet to guarantee good weapons for higher levels.

    Valid levels: ["Random", "RandomEarly", "RandomLate", "Port of Adia", "River of Souls", "Death Marshes", "Lair of the Blind Ones", "Hive of the Mantids", "Primagen's Lightship"]
    """
    display_name = "Starting Levels"
    valid_keys = {
        "Random",
        "RandomEarly",
        "RandomLate",
        "Port of Adia",
        "River of Souls",
        "Death Marshes",
        "Lair of the Blind Ones",
        "Hive of the Mantids",
        "Primagen's Lightship"
    }
    default = [ "Port of Adia" ]

class ExcludedLevels(OptionList):
    """
    The set of levels that will never be unlocked.

    You can add multiples of the following entries:
    - Random: Will pick from any non-excluded level
    - RandomEarly: Will pick from any non-excluded level, prioritizing levels 1-3
    - RandomLate: Will pick from any non-excluded level, prioritizing levels 4-6
    
    Valid levels: ["Random", "RandomEarly", "RandomLate", "Port of Adia", "River of Souls", "Death Marshes", "Lair of the Blind Ones", "Hive of the Mantids", "Primagen's Lightship"]
    """
    display_name = "Excluded Levels"
    valid_keys = {
        "Random",
        "RandomEarly",
        "RandomLate",
        "Port of Adia",
        "River of Souls",
        "Death Marshes",
        "Lair of the Blind Ones",
        "Hive of the Mantids",
        "Primagen's Lightship"
    }
    default = []

class GuaranteeTorpedoLauncher(Toggle):
    """
    Whether the Torpedo Launcher is in logic for the last part of the water maze in Level 4.
    The two switches before you can drop back down to the start are always in logic.
    """
    display_name = "Guarantee Torpedo Launcher"
    default = True

class MinRandomAmmoPercent(Range):
    """
    When receiving a random ammo, the minimum percentage of ammo you can get
    in a random weapon.

    If greater than MaxRandomAmmoPercent, this becomes the max.
    """
    display_name = "Min Random Ammo Percent"
    range_start = 0
    range_end = 100
    default = 20
    
class MaxRandomAmmoPercent(Range):
    """
    When receiving a random ammo, the maximum percentage of ammo you can get
    in a random weapon.

    If less than MinRandomAmmoPercent, this becomes the min.
    """
    display_name = "Max Random Ammo Percent"
    range_start = 0
    range_end = 100
    default = 75
    
class RandomizeEnemies(Choice):
    """
    Randomizes most enemies in the game. Every time an area is loaded, each enemy is replaced with one from a pool
    based on the option set here.

    Areas can be reloaded to see a different set of enemies if enemy-activated doors cannot be triggered (or if it's
    generally too hard).

	- Vanilla: Enemies are not randomized
	- Same Level: Uses a pool of enemies from the current level, excluding oblivion enemies.
                  Oblivion portals will only contain oblivion enemies.
	- Same Level Include Oblivion: Uses a pool of enemies from the current level including all oblivion enemies.
                                   Oblivion portals can also include enemies from that level.
                                   This is generally harder than the "Same Level" setting.
    - Similar Difficulty: Uses a pool of enemies of similar difficulty to the current level.
    - Scale to Weapons: Uses pools from increasingly higher levels the more weapons you own (excludes underwater only ones).
    - Chaos: Any enemy from the game can be anywhere. This is generally be the hardest setting.
    """
    display_name = "Randomize Enemies"
    option_vanilla = 0
    option_same_level = 1
    option_same_level_include_oblivion = 2
    option_similar_difficulty = 3
    options_scale_to_weapons = 4
    option_chaos = 5
    default = option_vanilla

class RandomizeEnemySpawners(Choice):
    """
    Only used if RandomizeEnemies is not set to Vanilla.

    Randomizes what enemies will be spawed by most enemy spawners. This will be a potentially different enemy for every spawn.
    Be careful, as this could poentially make some areas VERY difficult.

    Spawners affected include undead spawners, Sisters of Despair (who spawn the undead), wasp nests, spiders, and hives.
    Totem spawns will be determined by the RandomizeEnemies setting, despite them technically spawning in.

    Boss spawners for level 4, 5 and 6 will spawn from the "easy only" pool if set to the enemizer setting,
    Other settings can make it way too difficult. Primagen boss spawns will always be vanilla.

    - Vanilla: Enemy spawners are not randomized
    - Use Randomize Enemies Setting: Uses the same pool as RandomizeEnemies
    - Easy Only: Uses a pool containing low health, easy to kill enemies
    """
    display_name = "Randomize Enemy Spawners"
    option_vanilla = 0
    option_use_randomize_enemies_setting = 1
    option_easy_only = 2
    default = option_vanilla

class LocalHealthPercentage(Range):
    """
    The percentage of filler health pickups forced to your local world.
    
    Make sure to set this higher if you are playing in a big multiworld
    so you can actually get health when you need it.
    
    Setting this too high could result in generation failures.
    """
    display_name = "Local Health Percentage"
    range_start = 0
    range_end = 100
    default = 40
    
class LocalAmmoPercentage(Range):
    """
    The percentage of filler ammo forced to your local world.
    This includes the ammo fill percentages and those as generated filler items.
    
    Make sure to set this higher if you are playing in a big multiworld
    so you can actually get ammo when you need it.
    
    Setting this too high could result in generation failures.
    """
    display_name = "Local Ammo Percentage"
    range_start = 0
    range_end = 100
    default = 40
    
class LocalWeaponPercentage(Range):
    """
    The percentage of weapons forced to your local world.
    
    Make sure to set this higher if you are playing in a big multiworld
    so you can actually get new weapons.
    """
    display_name = "Local Weapon Percentage"
    range_start = 0
    range_end = 100
    default = 50

class FillerDistribution(Choice):
    """
    How the filler item pool will be calculated. In all options, traps will take up the
    given percentage of the item pool.

    Filler items are Life Forces, Health, Ammo pickups, and traps.

    In all cases, if more locations need to be filled, the weights defined in the 
    Filler<Type>Weight and <Type>Weight settings will be used.

    - Vanilla: Randomized vanilla items will be added to the pool. 
    - Vanilla Custom Weights:
         Randomized vanilla items will be added to the pool, but health and life forces 
         will use the weights specified in the <Silver/Blue/Full/Ultra>HealthWeight 
         and LifeForce<1/10>Weight settings.
    - Custom: Uses the weights defined in the Filler<Type>Weight and <Type>Weight settings.
    """
    display_name = "Filler Distribution"
    option_vanilla = 0
    option_vanilla_custom_weights = 1
    option_custom = 2
    default = option_vanilla
    
class FillerHealthWeight(Range):
    """
    The weight of non-vanilla health pickups in the non-progressive item pool.
    Consider setting this to none if not including health pickup locations.
    """
    display_name = "Filler Health Weight"
    range_start = 0
    range_end = 1000
    default = 25
    
class FillerAmmoWeight(Range):
    """
    The weight of non-vanilla ammo pickups in the non-progressive item pool.
    Consider setting this to none if not including weapons and ammo locations.
    """
    display_name = "Filler Ammo Weight"
    range_start = 0
    range_end = 1000
    default = 25
    
class FillerLifeForceWeight(Range):
    """
    The weight of non-vanilla life forces in the non-progressive item pool.
    Consider setting this to none if not including Life Force locations.
    """
    display_name = "Filler Life Force Weight"
    range_start = 0
    range_end = 1000
    default = 50

class SilverHealthWeight(Range):
    """
    The weight of a silver health when a non-vanilla or custom weighted health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Silver Health Weight"
    range_start = 0
    range_end = 1000
    default = 28

class BlueHealthWeight(Range):
    """
    The weight of a blue health when a non-vanilla or custom weighted health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Blue Health Weight"
    range_start = 0
    range_end = 1000
    default = 65

class FullHealthWeight(Range):
    """
    The weight of a full health when a non-vanilla or custom weighted health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Full Health Weight"
    range_start = 0
    range_end = 1000
    default = 5

class UltraHealthWeight(Range):
    """
    The weight of an ultra health when a non-vanilla or custom weighted health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Ultra Health Weight"
    range_start = 0
    range_end = 1000
    default = 2

class LifeForce1Weight(Range):
    """
    Only used if FillerDistribution is set to Vanilla Custom Weights or Custom.

    The weight of a Life Force 1 when non-vanilla or custom weighted Life Forces are rolled.
    Weighed against all Life Force pickups.
    """
    display_name = "Life Force 1 Weight"
    range_start = 0
    range_end = 1000
    default = 92

class LifeForce10Weight(Range):
    """
    Only used if FillerDistribution is set to Vanilla Custom Weights or Custom.

    The weight of a Life Force 10 when non-vanilla or custom weighted Life Forces are rolled.
    Weighed against all Life Force pickups.
    """
    display_name = "Life Force 10 Weight"
    range_start = 0
    range_end = 1000
    default = 8

class TrapPercentage(Range):
    """
    The percentage of traps in the filler item pool.

    Generally, more locations means more traps, so be careful when including a ton of item types
    (such as all Life Forces).
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0

class EnemyTrapPool(Choice):
    """
    The pool of enemies that enemy traps will pull from.
    If using a level setting and you aren't in a level, it will choose from the pool of all enemies.

	- Same Level: Uses a pool of enemies from the current level, excluding oblivion enemies.
                  Oblivion portals will only contain oblivion enemies.
	- Same Level Include Oblivion: Uses a pool of enemies from the current level including all oblivion enemies.
                                   Oblivion portals can also include enemies from that level.
    - Similar Difficulty: Uses a pool of enemies of similar difficulty to the current level.
    - Scale to Weapons: Uses pools from increasingly higher levels the more weapons you own (excludes underwater only ones).
    - Chaos: Uses a pool of all enemies.
    """
    display_name = "Enemy Trap Pool"
    option_same_level = 0
    option_same_level_include_oblivion = 1
    option_similar_difficulty = 2
    options_scale_to_weapons = 3
    option_chaos = 4
    default = option_same_level

class EnemyTrapWeight(Range):
    """
    Likelihood of receiving a trap that spawns 1-3 random enemies near you.
    """
    display_name = "Enemy Trap"
    range_start = 0
    range_end = 1000
    default = 50
    
class DamageTrapWeight(Range):
    """
    Likelihood of receiving a trap that does damage to you depending on your difficulty.
    It will never bring your health to 0.

    The damage this will do based on your difficulty level is:
    - Easy: 5% of your current health
    - Normal: 10%
    - Hard+: 20%
    """
    display_name = "Damage Trap"
    range_start = 0
    range_end = 1000
    default = 25
    
class SpamTrapWeight(Range):
    """
    Likelihood of receiving a trap that spams your screen with useless messages.
    """
    display_name = "Spam Trap"
    range_start = 0
    range_end = 1000
    default = 25
    
@dataclass
class Turok2Options(PerGameCommonOptions):
    level_goal: LevelGoal
    primagen_goal: PrimagenGoal
    randomize_primagen_keys: RandomizePrimagenKeys
    
    randomize_weapons: RandomizeWeapons
    starting_weapons: StartingWeapons
    excluded_weapons: ExcludedWeapons
    use_weapon_barriers: UseWeaponBarriers
    weapon_barrier_settings: WeaponBarrierSettings

    randomize_ammo_pickups: RandomizeAmmoPickups
    progressive_weapon_ammo_upgrades: ProgressiveWeaponAmmoUpgrades
    max_ammo_settings: MaxAmmoSettings

    randomize_health_pickups: RandomizeHealthPickups
    randomize_life_forces: RandomizeLifeForces
    randomize_eagle_feathers: RandomizeEagleFeathers
    randomize_talismans: RandomizeTalismans
    randomize_mission_items: RandomizeMissionItems
    randomize_switches: RandomizeSwitches
    randomize_mission_objectives: RandomizeMissionObjectives
    
    starting_levels: StartingLevels
    excluded_levels: ExcludedLevels
    force_early_weapon: ForceEarlyWeapon
    boss_weapon_list: BossWeaponList
    nuke_behavior: NukeBehavior
    level_key_packs: LevelKeyPacks
    progressive_warps: ProgressiveWarps
    progressive_warp_strength: ProgressiveWarpStrength
    starting_progressive_warps: StartingProgressiveWarps
    guarantee_torpedo_launcher: GuaranteeTorpedoLauncher

    min_random_ammo_percent: MinRandomAmmoPercent
    max_random_ammo_percent: MaxRandomAmmoPercent
    randomize_enemies: RandomizeEnemies
    randomize_enemy_spawners: RandomizeEnemySpawners

    local_weapon_percentage: LocalWeaponPercentage
    local_health_percentage: LocalHealthPercentage
    local_ammo_percentage: LocalAmmoPercentage
    
    filler_distribution: FillerDistribution
    filler_health_weight: FillerHealthWeight
    filler_ammo_weight: FillerAmmoWeight
    filler_life_force_weight: FillerLifeForceWeight
    
    silver_health_weight: SilverHealthWeight
    blue_health_weight: BlueHealthWeight
    full_health_weight: FullHealthWeight
    ultra_health_weight: UltraHealthWeight
    life_force_1_weight: LifeForce1Weight
    life_force_10_weight: LifeForce10Weight

    trap_percentage: TrapPercentage
    enemy_trap_pool: EnemyTrapPool
    enemy_trap_weight: EnemyTrapWeight
    damage_trap_weight: DamageTrapWeight
    spam_trap_weight: SpamTrapWeight
    
option_groups: List[OptionGroup] = [
    OptionGroup("Goal", [
        LevelGoal,
        PrimagenGoal,
        RandomizePrimagenKeys
    ]),
    OptionGroup("Weapon Options", [
        RandomizeWeapons,
        StartingWeapons,
        ExcludedWeapons,
        UseWeaponBarriers,
        WeaponBarrierSettings
    ]),
    OptionGroup("Ammo Options", [
        RandomizeAmmoPickups,
        ProgressiveWeaponAmmoUpgrades,
        MaxAmmoSettings
    ]),
    OptionGroup("Item Pool Options", [
        RandomizeHealthPickups,
        RandomizeLifeForces,
        RandomizeEagleFeathers,
        RandomizeTalismans,
        RandomizeMissionItems,
        RandomizeSwitches,
        RandomizeMissionObjectives
    ]),
    OptionGroup("Progression Options", [
        StartingLevels,
        ExcludedLevels,
        ForceEarlyWeapon,
        BossWeaponList,
        NukeBehavior,
        LevelKeyPacks,
        ProgressiveWarps,
        ProgressiveWarpStrength,
        StartingProgressiveWarps,
        GuaranteeTorpedoLauncher
    ]),
    OptionGroup("Gameplay Options", [
        MinRandomAmmoPercent,
        MaxRandomAmmoPercent,
        RandomizeEnemies,
        RandomizeEnemySpawners
    ]),
    OptionGroup("Local Item Pool", [
        LocalWeaponPercentage,
        LocalHealthPercentage,
        LocalAmmoPercentage,
    ]),
    OptionGroup("Filler Item Pool", [
        FillerDistribution,

        FillerHealthWeight,
        FillerAmmoWeight,
        FillerLifeForceWeight,
        
        SilverHealthWeight,
        BlueHealthWeight,
        FullHealthWeight,
        UltraHealthWeight,
        LifeForce1Weight,
        LifeForce10Weight,
    ]),
    OptionGroup("Traps", [
        TrapPercentage,
        EnemyTrapPool,
        EnemyTrapWeight,
        DamageTrapWeight,
        SpamTrapWeight
    ])
]

option_presets = {
    "casual": {
        "force_early_weapon": True
    },
    "advanced": {
        "force_early_weapon": False,
        "guarantee_torpedo_launcher": False
    }
}
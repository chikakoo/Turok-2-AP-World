from dataclasses import dataclass
from Options import Choice, OptionGroup, OptionList, OptionSet, OptionDict, \
    ItemSet, PerGameCommonOptions, Range, NamedRange, Toggle
from schema import Schema, And

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
    Places green warp barriers at the start, middle, and/or end of each level that you cannot pass until you obtain
    a certain number of unique progressive weapons. These include all weapons in the game, excluding the Talon, Bow,
    Flare Gun, Nuke, Harpoon Gun, and Torpedo Launcher.

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

class AmmoMultiplierBase(NamedRange):
    """Base values for ammo multipliers."""
    range_start = 1
    range_end = 400
    default = 100
    special_range_names = {
        "quarter": 25,
        "half": 50,
        "vanilla": 100,
        "double": 200,
        "triple": 300,
        "quadruple": 400
    }

class MaxBulletMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of bullets you can carry.
    Affects both the Pistol and the Mag 60.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 50.
    """
    display_name = "Max Bullet Multiplier"

class MaxShotgunShellMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of normal shotgun shells you can carry.
    Affects both the Shotgun and the Shredder.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 20.
    """
    display_name = "Max Shotgun Shell Multiplier"

class MaxExplosiveShotgunShellMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of explosive shotgun shells you can carry.
    Affects both the Shotgun and the Shredder.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 10.
    """
    display_name = "Max Explosive Shotgun Shell Multiplier"

class MaxTekArrowMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of tek arrows you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 10.
    """
    display_name = "Max Tek Arrow Multiplier"

class MaxTranquilizerDartMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of tranquilizer darts you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 15.
    """
    display_name = "Max Tranquilizer Dart Multiplier"

class MaxChargeDartMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of charge darts you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 30.
    """
    display_name = "Max Charge Dart Multiplier"

class MaxPlasmaRoundMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of plasma rounds you can carry.
    Affects both the Plasma Rifle and the Firestorm Cannon.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 150.
    """
    display_name = "Max Plasma Rounds Multiplier"

class MaxSunfirePodMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of sunfire pods you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 6.
    """
    display_name = "Max Sunfire Pod Multiplier"

class MaxBoreMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of bores you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 10.
    """
    display_name = "Max Sunfire Pod Multiplier"

class MaxMineMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of mines (PFMs) you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 10.
    """
    display_name = "Max Mine Multiplier"

class MaxGrenadeMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of grenades you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 10.
    """
    display_name = "Max Grenade Multiplier"

class MaxScorpionMissileMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of scorpion missiles you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 12.
    """
    display_name = "Max Scorpion Missile Multiplier"

class MaxFlameThrowerFuelMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max amount of Flame Thrower fuel you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 50.
    """
    display_name = "Max Flame Thrower Fuel Multiplier"

class MaxNukeAmmoMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of Nuke ammo you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 5.
    """
    display_name = "Max Nuke Ammo Multiplier"

class MaxSpearMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of spears (for the harpoon gun) you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 12.
    """
    display_name = "Max Spear Multiplier"

class MaxTorpedoMultiplier(AmmoMultiplierBase):
    """
    A percentage multiplier for the max number of torpedos you can carry.
    Be careful with setting this to low values, as it will severely limit your shot count.

    Vanilla max capacity is 3.
    """
    display_name = "Max Torpedo Multiplier"
    
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
    randomize_health_pickups: RandomizeHealthPickups
    randomize_life_forces: RandomizeLifeForces
    randomize_eagle_feathers: RandomizeEagleFeathers
    randomize_talismans: RandomizeTalismans
    randomize_mission_items: RandomizeMissionItems
    randomize_switches: RandomizeSwitches
    randomize_mission_objectives: RandomizeMissionObjectives

    progressive_weapon_ammo_upgrades: ProgressiveWeaponAmmoUpgrades
    max_tek_arrow_multiplier: MaxTekArrowMultiplier
    max_bullet_multiplier: MaxBulletMultiplier
    max_shotgun_shell_multiplier: MaxShotgunShellMultiplier
    max_explosive_shotgun_shell_multiplier: MaxExplosiveShotgunShellMultiplier
    max_tranquilizer_dart_multiplier: MaxTranquilizerDartMultiplier
    max_charge_dart_multiplier: MaxChargeDartMultiplier
    max_plasma_round_multiplier: MaxPlasmaRoundMultiplier
    max_sunfire_pod_multiplier: MaxSunfirePodMultiplier
    max_bore_multiplier: MaxBoreMultiplier
    max_mine_multiplier: MaxMineMultiplier
    max_grenade_multiplier: MaxGrenadeMultiplier
    max_scorpion_missile_multiplier: MaxScorpionMissileMultiplier
    max_flame_thrower_multiplier: MaxFlameThrowerFuelMultiplier
    max_nuke_ammo_multiplier: MaxNukeAmmoMultiplier
    max_spear_multiplier: MaxSpearMultiplier
    max_torpedo_multiplier: MaxTorpedoMultiplier
    
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
    enemy_trap_weight: EnemyTrapWeight
    damage_trap_weight: DamageTrapWeight
    spam_trap_weight: SpamTrapWeight
    
option_groups = [
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
    OptionGroup("Item Pool Options", [
        RandomizeAmmoPickups,
        RandomizeHealthPickups,
        RandomizeLifeForces,
        RandomizeEagleFeathers,
        RandomizeTalismans,
        RandomizeMissionItems,
        RandomizeSwitches,
        RandomizeMissionObjectives
    ]),
    OptionGroup("Ammo Options", [
        ProgressiveWeaponAmmoUpgrades,
        MaxBulletMultiplier,
        MaxShotgunShellMultiplier,
        MaxExplosiveShotgunShellMultiplier,
        MaxTekArrowMultiplier,
        MaxTranquilizerDartMultiplier,
        MaxChargeDartMultiplier,
        MaxPlasmaRoundMultiplier,
        MaxSunfirePodMultiplier,
        MaxBoreMultiplier,
        MaxMineMultiplier,
        MaxGrenadeMultiplier,
        MaxScorpionMissileMultiplier,
        MaxFlameThrowerFuelMultiplier,
        MaxNukeAmmoMultiplier,
        MaxSpearMultiplier,
        MaxTorpedoMultiplier
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
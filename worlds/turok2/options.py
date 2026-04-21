from dataclasses import dataclass
from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# TODO:
# death link
# split weapons/ammo

class LevelGoal(Range):
    """
    The number of levels you need to complete for your goal.

    If the Primagen goal is None, the minimum value is 1.
    """
    display_name = "Levels Goal"
    range_start = 0
    range_end = 6
    default = 6

class PrimagenGoal(Choice):
    """
    Sets the Primagen goal. See the PrimagenKeys setting for options on how to get to the lair.
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

class PrimagenKeys(Choice):
    """
    If the Primagen goal is not None, sets how you get the Primagen Keys.
    - Vanilla: The Primagen keys will be in their vanilla locations.
    - In Pool: The Primagen keys will be in the item pool to find.
    - Levels: The Primagen keys will be given to you after you complete the number of levels 
              specified in the LevelGoal setting
    """
    display_name = "Primagen Keys"
    option_vanilla = 0
    option_in_pool = 1
    option_levels = 2
    default = option_in_pool
    
class HealthSanity(Choice):
    """
    Whether to include static health pickups in the list of locations to check.
    Use the JunkItemPoolHealthWeight setting to affect how many will be in the item pool.
    - None: No health pickup locations will be included
    - All: All health pickup locations will be included
    - Full And Ultra Only: Only full and ultra health locations will be included.
                           Note that the four ultra healths in the Level 6 hub are excluded.
    """
    display_name = "Health Sanity"
    option_none = 0
    option_all = 1
    option_full_and_ultra_only = 2
    default = option_all
    
class IncludeWeaponAndAmmoLocations(Toggle):
    """
    Whether to include static weapon and ammo pickups in the list of locations to check.

    Any ammo in the item pool will be random ammo pickups, granting ammo in a random owned
    weapon (favoring those lacking ammo). This is to ensure that you can always get ammo
    for the randomly rolled weapons.

    Use the JunkItemPoolAmmoWeight setting to affect how much ammo will be in the item pool.
    """
    display_name = "Include Weapon and Ammo Locations"
    default = True
    
class LifeForceSanity(Choice):
    """
    Whether to include life forces in the list of locations to check.
    - None: No Life Force locations will be included
    - All: Both yellow and red Life Forces will be included
    - Yellow Only: Only yellow Life Forces will be included
    - Red Only: Only red Life Forces will be included
    """
    display_name = "Life Force Sanity"
    option_none = 0
    option_all = 1
    option_yellow_only = 2
    option_red_only = 3
    default = option_all

class IncludeLevelKeyLocations(Toggle):
    """
    Whether to include level keys in the list of locations to check.
    Setting this to False will place them in their vanilla locations.
    """
    display_name = "Include Level Keys"
    default = True

class IncludeEagleFeatherLocations(Toggle):
    """
    Whether to include eagle feathers in the list of locations to check.
    Setting this to False will place them in their vanilla locations.
    """
    display_name = "Include Eagle Feathers"
    default = True

class IncludeTalismanLocations(Toggle):
    """
    Whether to include talismans in the list of locations to check.
    Setting this to False will place them in their vanilla locations.
    """
    display_name = "Include Talismans"
    default = True
    
class IncludeMissionItemLocations(Toggle):
    """
    Whether to include items needed to finish the level. For example, the beacon power cells
    in level 1 or the graveyard keys in level 2.
    """
    display_name = "Include Mission Item Locations"
    default = True
    
class ForceEarlyWeapon(Toggle):
    """
    Forces an early progression weapon in the starting map so you have more than just the bow.
    """
    display_name = "Force Early Weapon"
    default = True
    
class NukeBehavior(Choice):
    """
    Defines how to get the Nuke weapon.
    - Disabled: There is no Nuke. Oblivion portals will have a random check.
    - Vanilla: The 6 Nuke Parts are in their vanilla locations.
    - Nuke Part Hunt: The 6 Nuke Parts will be shuffled into the pool. Oblivion portals will have a random check.
    - Weapon Pickup: The Nuke will be obtaned as a single items. Oblivion portals will have a random check.
    """
    display_name = "Nuke Behavior"
    option_disabled = 0
    option_vanilla = 1
    option_nuke_part_hunt = 2
    option_weapon_pickup = 3
    default = option_nuke_part_hunt

class ProgressiveWarps(Toggle):
    """
    Each progressive map will require a Progressive Warp item to advance further.
    Highly recommended for this to be on if on a multiworld, as it splits up the game.
    """
    display_name = "Progressive Warps"
    default = True

class ProgressiveWarpStrength(Range):
    """
    Used if Progressive Warps are on.
    The number of warps each Progressive Warp item allows you to travel through.
    """
    display_name = "Progressive Warp Strength"
    range_start = 1
    range_end = 10
    default = 1

class OpenHub(Toggle):
    """
    Whether the Level 1 door to the hub should be opened without completing the level,
    allowing access to other levels when you obtain their level keys.

    Remember to go through it to activate the hub's checkpoint station for convenience.

    Highly recommended for this to be on if using progressive warps.
    """
    display_name = "Open Hub"
    default = True

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
    
class JunkItemPoolHealthWeight(Range):
    """
    The weight of health pickups in the non-progressive item pool.
    Consider setting this to none if not including health pickup locations.
    """
    display_name = "Junk Item Pool Health Weight"
    range_start = 0
    range_end = 100
    default = 40
    
class JunkItemPoolAmmoWeight(Range):
    """
    The weight of ammo pickups in the non-progressive item pool.
    Consider setting this to none if not including weapons and ammo locations.
    """
    display_name = "Junk Item Pool Ammo Weight"
    range_start = 0
    range_end = 100
    default = 40
    
class JunkItemPoolLifeForceWeight(Range):
    """
    The weight of life forces in the non-progressive item pool.
    Consider setting this to none if not including Life Force locations.
    """
    display_name = "Junk Item Pool Ammo Weight"
    range_start = 0
    range_end = 100
    default = 80

class JunkItemPoolTrapWeight(Range):
    """
    The weight of traps in the junk item pool.
    """
    display_name = "Junk Item Pool Trap Weight"
    range_start = 0
    range_end = 100
    default = 0

class SilverHealthWeight(Range):
    """
    The weight of a silver health when a health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Silver Health Weight"
    range_start = 0
    range_end = 100
    default = 28

class BlueHealthWeight(Range):
    """
    The weight of a blue health when a health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Blue Health Weight"
    range_start = 0
    range_end = 100
    default = 65

class FullHealthWeight(Range):
    """
    The weight of a full health when a health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Full Health Weight"
    range_start = 0
    range_end = 100
    default = 5

class UltraHealthWeight(Range):
    """
    The weight of an ultra health when a health pickup is rolled.
    Weighed against all other health pickups.
    """
    display_name = "Ultra Health Weight"
    range_start = 0
    range_end = 100
    default = 2

class LifeForce1Weight(Range):
    """
    The weight of a Life Force 1 when Life Forces are rolled.
    Weighed against all Life Force pickups.
    """
    display_name = "Life Force 1 Weight"
    range_start = 0
    range_end = 100
    default = 92

class LifeForce10Weight(Range):
    """
    The weight of a Life Force 10 when Life Forces are rolled.
    Weighed against all Life Force pickups.
    """
    display_name = "Life Force 10 Weight"
    range_start = 0
    range_end = 100
    default = 8

class EnemyTrapWeight(Range):
    """
    Likelihood of receiving a trap that spawns 1-3 random enemies near you.
    """
    display_name = "Enemy Trap"
    range_start = 0
    range_end = 100
    default = 40
    
class DamageTrapWeight(Range):
    """
    Likelihood of receiving a trap that does a small amount of damage to you.
    It will never bring your health to 0.
    """
    display_name = "Damage Trap"
    range_start = 0
    range_end = 100
    default = 40
    
class SpamTrapWeight(Range):
    """
    Likelihood of receiving a trap that spams your screen with useless messages.
    """
    display_name = "Spam Trap"
    range_start = 0
    range_end = 100
    default = 40
    
@dataclass
class Turok2Options(PerGameCommonOptions):
    level_goal: LevelGoal
    primagen_goal: PrimagenGoal
    primagen_keys: PrimagenKeys
    
    health_sanity: HealthSanity
    include_weapon_and_ammo_locations: IncludeWeaponAndAmmoLocations
    life_force_sanity: LifeForceSanity
    include_level_key_locations: IncludeLevelKeyLocations
    include_eagle_feather_locations: IncludeEagleFeatherLocations
    include_talisman_locations: IncludeTalismanLocations
    include_mission_item_locations: IncludeMissionItemLocations
    
    force_early_weapon: ForceEarlyWeapon
    nuke_behavior: NukeBehavior
    progressive_warps: ProgressiveWarps
    progressive_warp_strength: ProgressiveWarpStrength
    open_hub: OpenHub
    guarantee_torpedo_launcher: GuaranteeTorpedoLauncher

    min_random_ammo_percent: MinRandomAmmoPercent
    max_random_ammo_percent: MaxRandomAmmoPercent

    local_weapon_percentage: LocalWeaponPercentage
    local_health_percentage: LocalHealthPercentage
    local_ammo_percentage: LocalAmmoPercentage
    
    junk_item_pool_health_weight: JunkItemPoolHealthWeight
    junk_item_pool_ammo_weight: JunkItemPoolAmmoWeight
    junk_item_pool_life_force_weight: JunkItemPoolLifeForceWeight
    junk_item_pool_trap_weight: JunkItemPoolTrapWeight

    silver_health_weight: SilverHealthWeight
    blue_health_weight: BlueHealthWeight
    full_health_weight: FullHealthWeight
    ultra_health_weight: UltraHealthWeight
    life_force_1_weight: LifeForce1Weight
    life_force_10_weight: LifeForce10Weight
    enemy_trap_weight: EnemyTrapWeight
    damage_trap_weight: DamageTrapWeight
    spam_trap_weight: SpamTrapWeight
    
option_groups = [
    OptionGroup("Goal", [
        LevelGoal,
        PrimagenGoal,
        PrimagenKeys
    ]),
    OptionGroup("Item Pool Options", [
        HealthSanity,
        IncludeWeaponAndAmmoLocations,
        LifeForceSanity,
        IncludeLevelKeyLocations,
        IncludeEagleFeatherLocations,
        IncludeTalismanLocations,
        IncludeMissionItemLocations,
    ]),
    OptionGroup("Progression Options", [
        ForceEarlyWeapon,
        NukeBehavior,
        ProgressiveWarps,
        ProgressiveWarpStrength,
        OpenHub,
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
    OptionGroup("Junk Item Pool", [
        JunkItemPoolHealthWeight,
        JunkItemPoolAmmoWeight,
        JunkItemPoolLifeForceWeight,
        JunkItemPoolTrapWeight,
        
        SilverHealthWeight,
        BlueHealthWeight,
        FullHealthWeight,
        UltraHealthWeight,
        LifeForce1Weight,
        LifeForce10Weight,
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
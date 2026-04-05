from dataclasses import dataclass
from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle
#todo:
# settings for... level keys, feathers, talismans
# death link
# whether to mark the pickups as important in the game
# individual settings for LF10/Full + Ultra Healths in pool

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
    - Get to Lair: Arriving at the lair will complete the goal.
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
    
class IncludeHealthLocations(Toggle):
    """
    Whether to include static health pickups in the list of locations to check.
    Use the JunkItemPoolHealthWeight setting to affect how many will be in the item pool.
    """
    display_name = "Include Health Locations"
    default = True
    
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
    
class IncludeLifeForceLocations(Toggle):
    """
    Whether to include life forces in the list of locations to check.
    Use the JunkItemPoolLifeForceWeight setting to affect how many will be in the item pool.
    """
    display_name = "Include Life Force Locations"
    default = True
    
class IncludeMissionItemLocations(Toggle):
    """
    Whether to include items needed to finish the level. For example, the beacon power cells
    in level 1 or the graveyard keys in level 2.

    Also includes level keys (for now). See the PrimagenKey setting for how Primagen keys work.
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

class OpenHub(Toggle):
    """
    Whether the Level 1 door to the hub should be opened without completing the level,
    allowing access to other levels when you obtain their level keys.

    Remember to go through it to activate the hub's checkpoint station for convenience.
    """
    display_name = "Open Hub"
    default = False

class GuaranteeTorpedoLauncher(Toggle):
    """
    Whether the Torpedo Launcher is in logic for the last part of the water maze in Level 4.
    The two switches before you can drop back down to the start are always in logic.
    """
    display_name = "Guarantee Torpedo Launcher"
    default = True
    
class BaseWeight(Choice):
    """
    Base class for all junk item weights.
    """
    option_none = 0
    option_very_low = 1
    option_low = 2
    option_medium = 4
    option_high = 8
    option_very_high = 10
    default = 4
    
class JunkItemPoolHealthWeight(BaseWeight):
    """
    The weight of health pickups in the non-progressive item pool.
    Consider setting this to none if not including health pickup locations.
    """
    display_name = "Junk Item Pool Health Weight"
    default = 4

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
    
class JunkItemPoolAmmoWeight(BaseWeight):
    """
    The weight of ammo pickups in the non-progressive item pool.
    Consider setting this to none if not including weapons and ammo locations.
    """
    display_name = "Junk Item Pool Ammo Weight"
    default = 4
    
class JunkItemPoolLifeForceWeight(BaseWeight):
    """
    The weight of life forces in the non-progressive item pool.
    Consider setting this to none if not including Life Force locations.
    """
    display_name = "Junk Item Pool Ammo Weight"
    default = 8

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
    
class JunkItemPoolTrapWeight(BaseWeight):
    """
    The weight of traps in the junk item pool.
    """
    display_name = "Junk Item Pool Trap Weight"
    default = 0

class EnemyTrapWeight(BaseWeight):
    """
    Likelihood of receiving a trap that spawns 1-3 random enemies near you.
    """
    display_name = "Enemy Trap"
    
class DamageTrapWeight(BaseWeight):
    """
    Likelihood of receiving a trap that does a small amount of damage to you.
    It will never bring your health to 0.
    """
    display_name = "Damage Trap"
    
class SpamTrapWeight(BaseWeight):
    """
    Likelihood of receiving a trap that spams your screen with useless messages.
    """
    display_name = "Spam Trap"
    
@dataclass
class Turok2Options(PerGameCommonOptions):
    level_goal: LevelGoal
    primagen_goal: PrimagenGoal
    primagen_keys: PrimagenKeys
    
    include_health_locations: IncludeHealthLocations
    include_weapon_and_ammo_locations: IncludeWeaponAndAmmoLocations
    include_life_force_locations: IncludeLifeForceLocations
    include_mission_item_locations: IncludeMissionItemLocations
    
    local_weapon_percentage: LocalWeaponPercentage
    local_health_percentage: LocalHealthPercentage
    local_ammo_percentage: LocalAmmoPercentage
    
    force_early_weapon: ForceEarlyWeapon
    nuke_behavior: NukeBehavior
    open_hub: OpenHub
    guarantee_torpedo_launcher: GuaranteeTorpedoLauncher
    
    junk_item_pool_health_weight: JunkItemPoolHealthWeight
    silver_health_weight: SilverHealthWeight
    blue_health_weight: BlueHealthWeight
    full_health_weight: FullHealthWeight
    ultra_health_weight: UltraHealthWeight

    junk_item_pool_ammo_weight: JunkItemPoolAmmoWeight

    junk_item_pool_life_force_weight: JunkItemPoolLifeForceWeight
    life_force_1_weight: LifeForce1Weight
    life_force_10_weight: LifeForce10Weight

    junk_item_pool_trap_weight: JunkItemPoolTrapWeight

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
        IncludeHealthLocations,
        IncludeWeaponAndAmmoLocations,
        IncludeLifeForceLocations,
        IncludeMissionItemLocations,
    ]),
    OptionGroup("Progression Options", [
        ForceEarlyWeapon,
        NukeBehavior,
        OpenHub
    ]),
    OptionGroup("Junk Item Pool", [
        JunkItemPoolHealthWeight,
        SilverHealthWeight,
        BlueHealthWeight,
        FullHealthWeight,
        UltraHealthWeight,

        JunkItemPoolAmmoWeight,

        JunkItemPoolLifeForceWeight,
        LifeForce1Weight,
        LifeForce10Weight,
        
        LocalWeaponPercentage,
        LocalHealthPercentage,
        LocalAmmoPercentage,
        
        JunkItemPoolTrapWeight,
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
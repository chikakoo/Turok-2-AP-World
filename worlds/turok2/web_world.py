from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

# when we do options
#from .options import option_groups, option_presets


class Turok2WebWorld(WebWorld):
    '''
    Defines how the game will display on the website.
    '''
    game = "APQuest"
    theme = "stone"
    
    #setup_en = Tutorial(
    #    "Multiworld Setup Guide",
    #    "A guide to setting up Turok 2 for MultiWorld.",
    #    "English",
    #    "setup_en.md",
    #    "setup/en",
    #    ["Chikakoo"],
    #)
    
    #tutorials = [setup_en]
    
    
    # If these exist in options
    #option_groups = option_groups
    #options_presets = option_presets